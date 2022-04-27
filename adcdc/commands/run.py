"""
NOTE: this is largely copied from the build commmand, maybe generalize later
"""
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
@click.option("-s", "--silent", default=False, is_flag=True, help="Don't print the command being run.")
def run(target_service: str, silent: bool):
    """
    Runs the dev service specified in TARGET_SERVICE.
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
        # DISPLAY is required for GUI based devcontainers
        "DISPLAY": env["DISPLAY"],
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
        ".devcontainer/docker-compose.yaml",
        # we are running the target service
        "run",
        # we want to remove the container after exit
        "--rm",
        f"{target_service}"
    ]
    # print the command so user knows what we're doing
    if not silent:
        cmd_str = " ".join(compose_args)
        print(cmd_str)

    # run the command & kill Python process
    os.execvpe("docker-compose", compose_args, env_plus_uid_gid)


if __name__ == "__main__":
    run()  # type: ignore
