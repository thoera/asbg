"""This module generates an example of a criteria file to use when drawing the Interclubs teams."""

import csv
import importlib.resources as pkg_resources
from random import choice, choices
from typing import NamedTuple

import yaml

from asbg.utils.logger import get_logger


logger = get_logger(__name__)

Subcriteria = dict[str, float] | None
Criteria = dict[str, dict[str, float | Subcriteria]]


class Criterion(NamedTuple):
    """Defines a player with the mandatory criteria fields."""

    licence: int
    genre: str
    participation: bool
    critere: str
    poids: float
    sous_critere: str
    sous_critere_poids: float
    score: float


def load_criteria_from_config() -> Criteria:
    """Loads the criteria and their weights from a yaml file."""
    ressource = pkg_resources.files("asbg.config").joinpath("teams.yaml")
    with pkg_resources.as_file(ressource) as filename:
        with open(filename, "r") as f:
            criteria = yaml.safe_load(f.read())

    return criteria["criteria"]


def generate_player_criteria(criteria: Criteria) -> list[list[str | float]]:
    """Generates the criteria for a player.

    Args:
        criteria: The criteria available and their weights.

    Returns:
        The criteria for a player.
    """
    player_criteria = []

    for criterion in criteria:
        weight = criteria[criterion]["weight"]

        subcriteria = criteria[criterion]["subcriteria"]

        if subcriteria is not None:
            for subcriterion in subcriteria:
                subcriterion_weight = subcriteria[subcriterion]

                score = choice(range(0, 101))
                player_criteria.append(
                    [criterion, weight, subcriterion, subcriterion_weight, score]
                )
        else:
            subcriterion = None
            subcriterion_weight = None
            score = choice(range(0, 101))
            player_criteria.append([criterion, weight, subcriterion, subcriterion_weight, score])

    return player_criteria


def generate_players_criteria(n: int = 50, save: bool = True) -> list[Criterion]:
    """Generates the criteria for multiple players.

    Args:
        n: The number of players for which to generate the criteria. Defaults to 50.
        save: Whether to save or not the results to a file. Defaults to True.

    Returns:
        A list of players with their respective criteria.
    """
    logger.info(f"Generating {n} random players with their criteria...")

    criteria = load_criteria_from_config()

    CRITERIA = []

    for license_number in range(n):
        player_criteria = generate_player_criteria(criteria)
        genre = choices(["Femme", "Homme"], [0.3, 0.7])[0]
        participation = choices([True, False], [0.8, 0.2])[0]

        for criteria_ in player_criteria:
            criteria_.insert(0, license_number)
            criteria_.insert(1, genre)
            criteria_.insert(2, participation)
            CRITERIA.append(Criterion(*criteria_))

    if save:
        ressource = pkg_resources.files("asbg.teams.data").joinpath("example-criteria.csv")

        with pkg_resources.as_file(ressource) as filename:
            logger.debug(f"Writing the example file to `{filename}`")
            with open(filename, "w", newline="") as f:
                writer = csv.writer(f, delimiter=";", lineterminator="\n")
                writer.writerow(Criterion._fields)
                writer.writerows(CRITERIA)

    return CRITERIA
