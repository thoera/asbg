"""This module defines the subcommands related to the drawing of Interclubs teams."""

import click

import asbg.teams.utils.generate_players_criteria as criteria
import asbg.teams.utils.generate_players_rankings as rankings
from asbg.teams.drawing import DrawPlayers
from asbg.teams.ranking import RankPlayers
from asbg.teams.utils.reshape_players_criteria import ReshapeToWide


@click.group(short_help="Subcommands for the drawing of Interclubs teams.")
def teams() -> None:
    pass


@click.command(short_help="Rank the players based on their official ranking and a set of criteria.")
def rank_players() -> None:
    """Rank the players based on their official ranking and a set of criteria."""
    RankPlayers().rank_players()


@click.command(
    short_help="Draw the players for the teams based on their ranking and a set of criteria."
)
def draw_players() -> None:
    """Draw the players for the teams based on their ranking and a set of criteria."""
    DrawPlayers().draw_players()


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


teams.add_command(rank_players)
teams.add_command(draw_players)
teams.add_command(generate_players_rankings)
teams.add_command(generate_players_criteria)
teams.add_command(reshape_criteria)
