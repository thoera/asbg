"""This module defines the subcommands related to the Interclubs."""

import click

from asbg.interclubs.interclubs import Interclubs


@click.group(short_help="Subcommands for the Interclubs.")
def interclubs() -> None:
    pass


@click.command(short_help="Fetch the results of the Interclubs and saves them into a database.")
def fetch() -> None:
    """Fetch the results of the Interclubs and saves them into a database."""
    Interclubs().parse()


interclubs.add_command(fetch)
