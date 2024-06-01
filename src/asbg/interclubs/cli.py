"""This module defines the subcommands related to the Interclubs."""

import os

import click
import pandas as pd
from tabulate import tabulate

from asbg.interclubs.constants import COMPETITIONS, HEADERS
from asbg.interclubs.database import connect, fetch_results
from asbg.interclubs.interclubs import Interclubs
from asbg.interclubs.results import FormatResults


@click.group(short_help="Subcommands for the Interclubs.")
def interclubs() -> None:
    pass


@click.command(short_help="Fetch the results of the Interclubs and saves them into a database.")
def fetch() -> None:
    """Fetch the results of the Interclubs and saves them into a database."""
    Interclubs().parse()


@click.command(short_help="Show the results of the Interclubs as table(s).")
@click.option(
    "--competition",
    required=False,
    show_default=True,
    type=click.Choice(list(COMPETITIONS.values())),
    help=(
        "The competition for which to show the results. "
        "Leave empty to show the results of all competitions."
    ),
)
def show(competition: str) -> None:
    """Show the result for the given competition.

    Args:
        competition: The competition for which to show the results.
    """
    con = connect()
    results = fetch_results(con)

    if competition is None:
        formatted_results = FormatResults().aggregate_results(results).reset_index()
        formatted_results["win_percentage"] = round(formatted_results["win_percentage"] * 100, 1)

        print("\nRésultats pour l'ensemble des équipes :\n")
        print(
            tabulate(
                formatted_results,
                headers=list(HEADERS.values()),
                showindex=False,
                tablefmt="rounded_outline",
            )
        )

        for _, competition_ in COMPETITIONS.items():
            print_results(results=results, competition=competition_)

    else:
        print_results(results=results, competition=competition)


@click.command(short_help="Display the results of the ASBG players.")
@click.option(
    "--frontend",
    default="streamlit",
    show_default=True,
    type=click.Choice(["dash", "streamlit"], case_sensitive=False),
    help="The frontend used to display the dashboard.",
)
def dashboard(frontend: str) -> None:
    """Display the results of the ASBG players."""
    dirname = os.path.dirname(__file__)

    if frontend == "streamlit":
        filename = os.path.join(dirname, "dashboard", "app_streamlit.py")
        os.system(f"streamlit run {filename}")

    if frontend == "dash":
        filename = os.path.join(dirname, "dashboard", "app.py")
        os.system(f"python {filename}")


def print_results(results: pd.DataFrame, competition: str) -> None:
    """Prints the results for the given competition.

    Args:
        results: The results to filter, aggregate and display.
        competition: The competition for which to print the results.
    """
    res = FormatResults()

    results = res.filter_results(results, competition=competition)
    fmt_competition = f"Résultats pour les {competition} :"

    formatted_results = res.aggregate_results(results).reset_index()
    formatted_results["win_percentage"] = round(formatted_results["win_percentage"] * 100, 1)

    print(f"\n{fmt_competition}\n")
    print(
        tabulate(
            formatted_results,
            headers=list(HEADERS.values()),
            showindex=False,
            tablefmt="rounded_outline",
        )
    )


interclubs.add_command(fetch)
interclubs.add_command(show)
interclubs.add_command(dashboard)
