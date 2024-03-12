"""This module defines the commands available after installing the library."""

import click

from asbg.interclubs import Interclubs


@click.group()
def cli() -> None:
    """Finds all the available commands below."""
    pass


@cli.command()
def get_interclubs_results() -> None:
    """Gets the results of the Interclubs."""
    Interclubs().parse()
