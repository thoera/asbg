"""This module ranks the players based on their official ranking and a set of criteria."""

import importlib.resources as pkg_resources
from enum import Enum, unique
from os import PathLike
from typing import NamedTuple

import polars as pl

from asbg.utils.logger import get_logger


class Player(NamedTuple):
    licence: str
    nom: str
    prenom: str
    genre: str
    simple: str
    double: str
    mixte: str
    ranking: str
    score: float


@unique
class Rankings(Enum):
    """Represents the possible rankings for a player.

    The highest ranking is voluntarily limited to "D7" to better represent the current players.
    """

    NC = 0
    P12 = 1
    P11 = 2
    P10 = 3
    D9 = 4
    D8 = 5
    D7 = 6


class RankPlayers:
    """Ranks the players based on their official ranking and a set of criteria."""

    def __init__(
        self,
        ranking_filepath: str | PathLike | None = None,
        criteria_filepath: str | PathLike | None = None,
    ) -> None:
        self.ranking_filepath = ranking_filepath
        self.criteria_filepath = criteria_filepath
        self.logger = get_logger(__name__)

    def rank_players(self) -> list[Player]:
        self.logger.info("Ranking the players...")

        rankings = self.load_rankings()
        rankings = self.compute_ranking(rankings)

        criteria = self.load_criteria()
        criteria = self.compute_score_from_criteria()

        rankings = rankings.join(criteria, on="licence")

        breakpoint()

    def compute_ranking(self, rankings: pl.DataFrame) -> pl.DataFrame:
        self.logger.debug("Computing the ranking from the simple, double and mixed rankings...")

        # Map the rankings of a player to integers to be able to do some basic computations.
        mapping = {rank.name: rank.value for rank in Rankings}
        rankings = rankings.with_columns(
            pl.col("simple").replace(mapping).alias("simple_int"),
            pl.col("double").replace(mapping).alias("double_int"),
            pl.col("mixte").replace(mapping).alias("mixte_int"),
        )

        # The unique ranking is computed as the maximum of the three rankings of a player.
        rankings = rankings.select(
            pl.exclude("simple_int", "double_int", "mixte_int"),
            pl.max_horizontal("simple_int", "double_int", "mixte_int").alias("ranking"),
        )

        return rankings

    def compute_score_from_criteria(self) -> pl.DataFrame:
        self.logger.debug("Computing the scores from the criteria...")

        # Normalize the score per criteria x subcriteria across all players.
        # Compute the weighted score per criteria.
        # Compute the weighted score across all criteria.

        pass

    def load_rankings(self) -> pl.DataFrame:
        if self.ranking_filepath is None:
            ressource = pkg_resources.files("asbg.teams.data").joinpath("example-rankings.csv")
            with pkg_resources.as_file(ressource) as filename:
                self.ranking_filepath = filename

        self.logger.debug(f"Loading the rankings from `{self.ranking_filepath}`...")

        return pl.read_csv(self.ranking_filepath, separator=";")

    def load_criteria(self) -> pl.DataFrame:
        if self.criteria_filepath is None:
            ressource = pkg_resources.files("asbg.teams.data").joinpath("example-criteria.csv")
            with pkg_resources.as_file(ressource) as filename:
                self.criteria_filepath = filename

        self.logger.debug(f"Loading the criteria from `{self.criteria_filepath}`...")

        return pl.read_csv(self.criteria_filepath, separator=";")


if __name__ == "__main__":
    rank_players = RankPlayers()
    rank_players.rank_players()
