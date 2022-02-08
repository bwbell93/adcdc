from copy import copy
from yaml import load, dump, Loader


def add_dev_compose_yaml(yml, target_service: str, target_dockerfile: str, target_codepath: str):
    """
        Adds a dev for the target service given a yaml docker-compose config
    """
    if target_service not in yml["services"]:
        raise AttributeError(f"Can't find the target service {target_service} in the yaml config.")
    service_config = yml["services"][target_service]

    # add the dev service
    dev_service = copy(service_config)
    
    # overwrite build 
    dev_service["build"] = {
        "context": "./",
        "dockerfile": target_dockerfile
    }
    # remove image
    del dev_service["image"]

    # add stdin, tty, and command
    dev_service["tty"] = True
    dev_service["stdin_open"] = True
    dev_service["command"] = "/bin/bash"

    # add a volume from cwd to target code path
    if "volumes" not in dev_service:
        dev_service["volumes"] = []
    volume_str = f".:{target_codepath}"
    # if user is already mounting their code don't re-add
    if volume_str not in dev_service["volumes"]:
        dev_service["volumes"].append(
            f".:{target_codepath}"
        )

    yml["services"][f"{target_service}-dev"] = dev_service
    return yml


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("compose_file", type=str, help="Filepath to the docker-compose.yaml file")
    parser.add_argument("target_service", type=str, help="Service to add a dev-container for")
    parser.add_argument("target_dockerfile", type=str, help="Filepath to target dev Dockerfile")
    parser.add_argument("target_codepath", type=str, help="Filepath to code in dev container")

    args = parser.parse_args()

    with open(args.compose_file, "rb") as in_file:
        yml_config = load(in_file, Loader)

    new_config = add_dev_compose_yaml(yml_config, args.target_service, args.target_dockerfile, args.target_codepath)
    with open("dev-docker-compose.yaml", "w") as out_file:
        dump(new_config, out_file)
    
