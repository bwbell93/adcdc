from typing import List, Tuple

import click
import os
import subprocess


def _run_cmd_get_output(cmd: List[str]) -> str:
    """ run the command & get output in a one liner from https://stackoverflow.com/a/4760517. """
    return subprocess.run(cmd, stdout=subprocess.PIPE).stdout.decode('utf-8')


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
@click.argument("target_dev_service")
def build(target_dev_service: str):
    """
    Builds the dev service specified by the cli argument.
    """
    # get the uid & gid for the user
    UID, GID = get_uid_gid()

    # TODO:
    # optionally build the main container
    # create the command to run
    # print the command to show the user we're not doing anything weird

    # create the command to build the devcontainer
    uid_gid_env = {
        "UID": UID,
        "GID": GID
    }
    compose_args = [
        "build",
        f"{target_dev_service}"
    ]
    # TODO: should we tag the dev container?

    # run the command & kill Python process
    os.execlpe("docker-compose", *compose_args, uid_gid_env)


if __name__ == "__main__":
    build()  # type: ignore
