"""This module defines the subcommands related to the drawing of Interclubs teams."""

import click

import asbg.teams.utils.generate_example_rankings as rankings


@click.group(short_help="Subcommands for the drawing of Interclubs teams.")
def teams() -> None:
    pass


@click.command(short_help="Generate random players with their respective rankings.")
@click.option(
    "--players",
    required=False,
    default=26,
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


teams.add_command(generate_players_rankings)
