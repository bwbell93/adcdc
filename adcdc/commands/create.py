from io import TextIOWrapper
from typing import List, Dict, Any
import click
import os
from functools import partial
from copy import copy
import yaml


def recurse_list_apply(cfg_list: List[Any], fn, item_filter) -> List[Any]:
    """
    Applies the function to each list item if item_filter returns true.
    If encountering a dict, recurse with recurse_dict_apply
    Updates the list in place
    """
    # iterate items in the list to check if dict or item_filter
    for i, list_item in enumerate(cfg_list):
        # recurse on dictionary
        if isinstance(list_item, dict):
            recurse_dict_apply(list_item, fn, item_filter)
        elif isinstance(list_item, list):
            recurse_list_apply(list_item, fn, item_filter)
        # otherwise regular types
        elif item_filter(list_item):
            cfg_list[i] = fn(list_item)
    return cfg_list


def recurse_dict_apply(cfg: Dict[str, Any], fn, item_filter):
    """
    Applies the function to each default container (dict, list) in the cfg dict 
    if the item_filter returns true.
    Updates the dictionary in place
    """
    for key, value in cfg.items():
        if isinstance(value, dict):
            recurse_dict_apply(value, fn, item_filter)
        elif isinstance(value, list):
            recurse_list_apply(value, fn, item_filter)
        # otherwise regular type
        elif item_filter(value):
            cfg[key] = fn(value)
    return cfg


def _possible_replace_keywords_in_config(cfg: Dict[str, Any]) -> Dict[str, Any]:
    """
    Replaces any keywords in the adcdc_config
    """
    return recurse_dict_apply(copy(cfg), partial(_possible_replace_keywords, cfg), lambda x: isinstance(x, str))


def _possible_replace_keywords(adcdc_config, item: str) -> str:
    """
    If keywords are found in the string they are replaced
    """
    if "${DOCKERUSER}" in item:
        return item.replace("${DOCKERUSER}", adcdc_config["docker-user"])
    return item


def create_docker_from_template(adcdc_config, original_image: str, docker_template: List[str], original_dockerfile_path: str=None) -> List[str]:
    """
    Creates a Dockerfile (consisting of a list of lines) from an original Dockerfile filepath and template.
    The original_dockerfile path is only needed if we can't determine the user or workdir from the adcdc_config
    """

    # TODO: if auto parse the original dockerfile to determine the user
    if adcdc_config["docker-user"] == "auto":
        raise NotImplementedError("TODO")
    if adcdc_config["workdir"] == "auto":
        raise NotImplementedError("TODO")

    # take our template & add the FROM command and WORKDIR command
    docker_template.insert(0, f"FROM {original_image}")
    docker_template.append(f"USER {adcdc_config['docker-user']}")
    docker_template.append(f"WORKDIR {adcdc_config['workdir']}")

    return docker_template


def add_dev_compose_yaml(compose_yml, target_service: str, target_dockerfile: str, adcdc_config):
    """
    Adds a dev for the target service given a yaml docker-compose config.
    NOTE: this is an inplace operation & updates the compose_yml arg
    """
    if target_service not in compose_yml["services"]:
        raise AttributeError(f"Can't find the target service {target_service} in the yaml config.")
    service_config = compose_yml["services"][target_service]

    # add the dev service
    dev_service = copy(service_config)
    
    # overwrite build 
    dev_service["build"] = {
        # NOTE: this is hardcoded to assume .devcontainer folder, see TODO item in create()
        "context": "../",
        "dockerfile": target_dockerfile
    }
    # remove image
    del dev_service["image"]

    # add stdin, tty, command, and user
    dev_service["tty"] = True
    dev_service["stdin_open"] = True
    dev_service["command"] = adcdc_config["command"]
    dev_service["user"] = "${UID}:${GID}"

    # add a volume from cwd to target code path
    if "volumes" not in dev_service:
        dev_service["volumes"] = []
    volume_str = f".:{adcdc_config['code-mount']}"
    # if user is already mounting their code don't re-add
    if volume_str not in dev_service["volumes"]:
        dev_service["volumes"].append(adcdc_config["code-mount"])
    # add any extra volumes
    for v in adcdc_config["volumes"]:
        dev_service["volumes"].append(v)

    # add named volumes to the top level docker-compose yaml
    # these are a dict
    if "volumes" not in compose_yml:
        compose_yml["volumes"] = {}
    if "named-volumes" in adcdc_config:
        for name, vol_args in adcdc_config["named-volumes"].items():
            compose_yml["volumes"][name] = vol_args

    # add any additional user configs if they exist
    if "docker-compose-configs" in adcdc_config:
        for key, value in adcdc_config["docker-compose-configs"].items():
            dev_service[key] = value

    compose_yml["services"][f"{target_service}-dev"] = dev_service

    # remove the service that we created from -dev.
    # this prevents confusion if trying to use the adcdc build command for the main container
    # which is unsupported
    del compose_yml["services"][target_service]
    return compose_yml


@click.command()
@click.argument("target_service")
@click.argument("adcdc_config_yaml", type=click.File("r"))
@click.option("-f", "--file", type=str, default=None, 
              help="Specify an alternate compose file.          default: r\"(docker-)?compose.(yaml|yml)\"")
@click.option("-o", "--overwrite", default=False, is_flag=True, help="Overwrite existing dev docker-compose.yaml")
def create(target_service: str, adcdc_config_yaml: TextIOWrapper, file: str, overwrite: bool):
    """
    Creates .devcontainer files from an adcdc config yaml.
    """
    # TODO: making this configurable is really hard
    output_path = ".devcontainer"
    # load the adcdc_config and replace any keywords
    adcdc_config = yaml.safe_load(adcdc_config_yaml)
    adcdc_config = _possible_replace_keywords_in_config(adcdc_config)

    # load the docker-compose file from default locations
    docker_compose_file = None
    # try all valid variations in correct order, see https://docs.docker.com/compose/compose-file/
    variations = ["compose.yaml", "compose.yml", "docker-compose.yaml", "docker-compose.yml"]
    if file is None:
        for v in variations:
            if os.path.exists(v):
                docker_compose_file = v
                break
    # else manually entered compose file location
    else:
        docker_compose_file = file

    # check if found in valid variations
    if docker_compose_file is None:
        raise click.ClickException(f"Can't find a valid docker compose file. Tried {', '.join(variations)}")
    # check if manually entered path is a file
    if not os.path.exists(docker_compose_file) or not os.path.isfile(docker_compose_file):
        raise click.ClickException(f"Can't the docker compose file at '{docker_compose_file}'")
    # open compose file and read it in with yaml
    with open(docker_compose_file, "r") as in_file:
        docker_compose = yaml.safe_load(in_file)

    # load the adcdc docker template
    docker_template_pwd = os.path.split(adcdc_config_yaml.name)[0]
    docker_template_relative = os.path.join(docker_template_pwd, adcdc_config["adcdc-docker-template"])
    # first check if relative path
    if os.path.exists(docker_template_relative):
        docker_template_file = docker_template_relative
    # otherwise check absolute
    elif os.path.exists(adcdc_config["adcdc-docker-template"]):
        docker_template_file = adcdc_config["adcdc-docker-template"]
    # otherwise invalid path
    else:
        raise click.ClickException(f"Unable to find adcdc docker template at '{docker_template_relative}' or '{adcdc_config['adcdc-docker-template']}'")
    # read docker template
    with open(docker_template_file, "r") as in_docker_template:
        docker_template = in_docker_template.read().splitlines()

    # create the devdockerfile lines
    dev_dockerfile = create_docker_from_template(adcdc_config, docker_compose["services"][target_service]["image"], docker_template)

    # create output dir if not exists
    os.makedirs(output_path, exist_ok=True)

    # write out the dockerfile to outputpath/Dockerfile
    output_dockerfile_path = os.path.join(output_path, "Dockerfile")
    if os.path.exists(output_dockerfile_path) and not overwrite:
        raise click.ClickException(f"Output dockerfile '{output_dockerfile_path}' exists already. Use the -o flag to overwrite.")
    # write out to the dockerfile path
    with open(output_dockerfile_path, "w") as out_file:
        for line in dev_dockerfile:
            out_file.write(f"{line}\n")

    # now create the new docker-compose.yaml
    dev_compose_yml = add_dev_compose_yaml(docker_compose, target_service, output_dockerfile_path, adcdc_config)
    output_docker_compose_path = os.path.join(output_path, "docker-compose.yaml")
    if os.path.exists(output_docker_compose_path) and not overwrite:
        raise click.ClickException(f"Output docker-compose path '{output_docker_compose_path}' exists already. Use the -o flag to overwrite")
    # write out to the docker compose filepath
    with open(output_docker_compose_path, "w") as out_file:
        # don't sort keys so we can preserve order of the original file
        yaml.dump(dev_compose_yml, out_file, sort_keys=False)


if __name__ == "__main__":
    create()  # type: ignore
