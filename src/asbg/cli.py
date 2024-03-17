"""This module defines the commands available after installing the package."""

import click

from asbg.interclubs import Interclubs


@click.group()
def cli() -> None:
    """Finds all the available commands below."""
    pass


@cli.command()
def get_interclubs_results() -> None:
    """Gets the results of the Interclubs and saves them into a database."""
    Interclubs().parse()
