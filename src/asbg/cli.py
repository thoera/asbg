"""This module defines the commands available after installing the package."""

import os

import click

from asbg.interclubs import Interclubs


@click.group()
def cli() -> None:
    pass


@cli.command(
    short_help="Gets the results of the Interclubs and saves them into a database."
)
def get_interclubs_results() -> None:
    """Gets the results of the Interclubs and saves them into a database."""
    Interclubs().parse()


@cli.command(short_help="Visualizes the results of the Interclubs in your browser.")
def streamlit() -> None:
    """Visualizes the results of the Interclubs in your browser."""
    dirname = os.path.dirname(__file__)
    filename = os.path.join(dirname, "app.py")
    os.system(f"streamlit run {filename}")
