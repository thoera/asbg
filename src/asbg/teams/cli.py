"""This module defines the subcommands related to the drawing of Interclubs teams."""

import click

import asbg.teams.utils.generate_players_criteria as criteria
import asbg.teams.utils.generate_players_rankings as rankings
from asbg.teams.utils.reshape_players_criteria import ReshapeToWide


@click.group(short_help="Subcommands for the drawing of Interclubs teams.")
def teams() -> None:
    pass


@click.command(short_help="Generate random players with their respective rankings.")
@click.option(
    "--players",
    required=False,
    default=50,
    show_default=True,
    type=int,
    help="The number of players to generate.",
)
def generate_players_rankings(players: int) -> None:
    """Generate random players with their respective rankings.

    Args:
        players: The number of players to generate.
    """
    rankings.generate_players_rankings(n=players)


@click.command(short_help="Generate random players with their respective criteria.")
@click.option(
    "--players",
    required=False,
    default=50,
    show_default=True,
    type=int,
    help="The number of players to generate.",
)
def generate_players_criteria(players: int) -> None:
    """Generate random players with their respective criteria.

    Args:
        players: The number of players to generate.
    """
    criteria.generate_players_criteria(n=players)


@click.command(short_help="Reshape a criteria file in a long format to a wide one.")
def reshape_criteria() -> None:
    """Reshape a criteria file in a long format to a wide one."""
    ReshapeToWide().reshape()


teams.add_command(generate_players_rankings)
teams.add_command(generate_players_criteria)
teams.add_command(reshape_criteria)
