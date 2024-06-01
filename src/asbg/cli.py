"""This module defines the commands available after installing the package."""

import click

from asbg import __version__
from asbg.interclubs.cli import interclubs


CONTEXT_SETTINGS = dict(help_option_names=["-h", "--help"])


@click.group(context_settings=CONTEXT_SETTINGS)
def cli() -> None:
    pass


@click.command(short_help="Show the version of the application.")
def version() -> None:
    """Show the version of the application."""
    click.echo(__version__)


cli.add_command(version)
cli.add_command(interclubs)
