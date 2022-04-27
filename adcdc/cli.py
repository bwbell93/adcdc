"""
Aggregates all commands into one CLI
"""

import click
from adcdc.commands import build, create, run


# create click cli group
@click.group()
def cli():
    """
    For a new project use commands in the following order:

    \b
    adcdc create <service-name> <adcdc_config_yaml>
    adcdc build <service-name>-dev
    adcdc run <service-name>-dev
    """
    pass


cli.add_command(build, name="build")  # type: ignore
cli.add_command(create, name="create")  # type: ignore
cli.add_command(run, name="run")  # type: ignore


if __name__ == "__main__":
    cli()
