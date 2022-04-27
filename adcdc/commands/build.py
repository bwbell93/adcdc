from typing import List, Tuple

import click
import os
import subprocess


def _run_cmd_get_output(cmd: List[str]) -> str:
    """ run the command & get output in a one liner from https://stackoverflow.com/a/4760517. """
    return subprocess.run(cmd, stdout=subprocess.PIPE).stdout.decode('utf-8').strip('\n')


def get_uid_gid() -> Tuple[str, str]:
    """
    Fetches the UID and GID for the current user with:
    UID = `id -u`
    GID = `id -g`
    """
    UID = _run_cmd_get_output(["id", "-u"])
    GID = _run_cmd_get_output(["id", "-g"])
    return UID, GID


@click.command()
@click.argument("target_service")
@click.option("-f", "--file", type=str, default=".devcontainer/docker-compose.yaml", 
              help="Specify an alternate compose file.                      (default: .devcontainer/docker-compose.yaml)")
@click.option("-s", "--silent", default=False, is_flag=True, help="Don't print the command being run.")
def build(target_service: str, file: str, silent: bool):
    """
    Builds the dev service specified in TARGET_SERVICE.
    """
    # get the uid & gid for the user
    UID, GID = get_uid_gid()

    # TODO:
    # optionally build the main container

    # create the command to build the devcontainer
    env = os.environ
    env_plus_uid_gid = {
        # PATH is required so we can get docker-compose from wherever it is
        "PATH": env["PATH"],
        # TODO: are there other env vars we need?
        "UID": UID,
        "GID": GID
    }
    compose_args = [
        # NOTE: this is very odd, but the first arg must be "docker-compose"
        # otherwise it errors with something unrelated/random
        "docker-compose",
        # need to specify .devcontainer
        "-f",
        file,
        # we are building the target service
        "build",
        f"{target_service}"
    ]
    # print the command so user knows what we're doing
    if not silent:
        cmd_str = " ".join(compose_args)
        print(cmd_str)

    # run the command & kill Python process
    os.execvpe("docker-compose", compose_args, env_plus_uid_gid)


if __name__ == "__main__":
    build()  # type: ignore
