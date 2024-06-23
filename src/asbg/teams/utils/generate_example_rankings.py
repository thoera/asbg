"""This module generates an example of a ranking file to use when drawing the Interclubs teams."""

import csv
import importlib.resources as pkg_resources
from enum import Enum, unique
from random import choice
from string import ascii_lowercase
from typing import NamedTuple

from asbg.utils.logger import get_logger


logger = get_logger(__name__)


@unique
class Ranking(Enum):
    """Reprensents the possible rankings for a player.

    The highest ranking is voluntarily limited to "D7" to better represent the current players.
    """

    NC = 0
    P12 = 1
    P11 = 2
    P10 = 3
    D9 = 4
    D8 = 5
    D7 = 6


class Player(NamedTuple):
    """Defines a player with the mandatory fields."""

    licence: int
    nom: str
    prenom: str
    simple: str
    double: str
    mixte: str


def clip(n: int, lower_bound: int = 0, upper_bound: int = 6) -> int:
    """Clips a number between a lower and an upper bound.

    Args:
        n: The number to clip.
        lower_bound: The lower bound to use when clipping.
        upper_bound: The upper bound to use when clipping.
    """
    if lower_bound > upper_bound:
        raise ValueError("The lower bound should be smaller or equal to the upper bound")
    return max(lower_bound, min(n, upper_bound))


def generate_players_rankings(n: int = 50, save: bool = True) -> list[Player]:
    """Generates random players with a license number, a firstanme, a lastname and the rankings.

    Args:
        n: The number of players to generate. Defaults to 50.
        save: Whether to save or not the results to a file. Defaults to True.

    Returns:
        A list of players with their respective rankings.
    """
    logger.info(f"Generating {n} random players with their rankings...")

    PLAYERS = []

    for license_number in range(n):
        nom = (
            choice(ascii_lowercase).upper()
            + choice(ascii_lowercase).upper()
            + choice(ascii_lowercase).upper()
        )
        prenom = choice(ascii_lowercase) + choice(ascii_lowercase) + choice(ascii_lowercase)

        ranking = choice(list(Ranking)).value

        simple = Ranking(clip(choice(range(ranking - 1, ranking + 2)))).name
        double = Ranking(clip(choice(range(ranking - 1, ranking + 2)))).name
        mixte = Ranking(clip(choice(range(ranking - 1, ranking + 2)))).name

        PLAYERS.append(Player(license_number, nom, prenom, simple, double, mixte))

    if save:
        ressource = pkg_resources.files("asbg.teams.data").joinpath("example-rankings.csv")

        with pkg_resources.as_file(ressource) as filename:
            logger.debug(f"Writing the example file to `{filename}`")
            with open(filename, "w", newline="") as f:
                writer = csv.writer(f, delimiter=";", lineterminator="\n")
                writer.writerow(Player._fields)
                writer.writerows(PLAYERS)

    return PLAYERS
