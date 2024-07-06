"""This module ranks the players based on their official ranking and a set of criteria."""

import importlib.resources as pkg_resources
from enum import Enum, unique
from os import PathLike
from typing import Any

import polars as pl
import yaml

from asbg.utils.logger import get_logger


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
    """Ranks the players based on their official ranking and a set of criteria.

    Args:
        src_ranking: The file with the ranking of the players. Defaults to None.
            If None, The example ranking file will be used.
        src_criteria: The file with the criteria for the players. Defaults to None.
            If None, The example criteria file will be used.
    """

    def __init__(
        self,
        src_ranking: str | PathLike | None = None,
        src_criteria: str | PathLike | None = None,
    ) -> None:
        self.src_ranking = src_ranking
        self.src_criteria = src_criteria
        self.logger = get_logger(__name__)

    def rank_players(self) -> dict[str, pl.DataFrame]:
        """Ranks the players by gender using their official rankings and some specific criteria."""
        rankings = self.load_rankings()
        rankings = self.compute_unique_ranking(rankings)

        criteria = self.load_criteria()
        criteria = self.compute_score(criteria)

        rankings = rankings.join(criteria, on="licence")
        rankings = self.rank_by_gender(rankings)

        self.save_rankings(rankings)

        return rankings

    def rank_by_gender(self, rankings: pl.DataFrame) -> dict[str, pl.DataFrame]:
        """Ranks the players by gender.

        Args:
            rankings: The DataFrame with the ranking by player and the score computed
                from the criteria to use to rank the players by gender.

        Returns:
            The ranking by gender.
        """
        self.logger.info("Ranking the players by gender...")

        rankings_by_gender = {
            gender[0]: dataframe
            for gender, dataframe in rankings.filter(pl.col("participation"))
            .sort(["ranking", "score"], descending=True)
            .partition_by("genre", as_dict=True, maintain_order=True)
            .items()
        }

        return rankings_by_gender

    def compute_unique_ranking(self, rankings: pl.DataFrame) -> pl.DataFrame:
        """Computes a unique ranking by player from the simple, double and mixed rankings.

        Args:
            rankings: A DataFrame with the simple, double and mixed rankings.

        Returns:
            A DataFrame with a unique ranking by player.
        """
        self.logger.debug(
            "Computing a unique ranking by player from the simple, double and mixed rankings..."
        )

        # Map the rankings of a player to integers to be able to do some basic computations.
        mapping = {rank.name: rank.value for rank in Rankings}
        rankings = rankings.with_columns(
            pl.col("simple").replace_strict(mapping).alias("simple_int"),
            pl.col("double").replace_strict(mapping).alias("double_int"),
            pl.col("mixte").replace_strict(mapping).alias("mixte_int"),
        )

        # The unique ranking is computed as the maximum of the three rankings of a player.
        rankings = rankings.select(
            pl.exclude("simple_int", "double_int", "mixte_int"),
            pl.max_horizontal("simple_int", "double_int", "mixte_int").alias("ranking"),
        )

        return rankings

    def compute_score(self, criteria: pl.DataFrame) -> pl.DataFrame:
        """Computes a score for each player from some specific criteria.

        Args:
            criteria: A DataFrame with the criteria for each player.

        Returns:
            A DataFrame with a score computed from the criteria for each player.
        """
        self.logger.debug("Computing a score by player from the criteria...")

        cfg = self.load_config_file()

        # Normalize the score for each subcriterion across all players.
        subcriteria = self.get_subcriteria_names(cfg)
        cols = pl.col(subcriteria)
        criteria = criteria.with_columns((cols - cols.min()) / (cols.max() - cols.min()))

        # Compute the weighted score for each subcriterion.
        weights = self.get_subcriteria_weights(cfg)

        for subcriterion, weight in weights.items():
            criteria = criteria.with_columns(pl.col(subcriterion) * weight)

        # Compute the score as the sum of the weighted criteria.
        criteria = criteria.select(
            pl.col("licence"),
            pl.col("genre"),
            pl.col("participation"),
            score=pl.sum_horizontal(cols),
        )

        return criteria

    def load_rankings(self) -> pl.DataFrame:
        """Loads the rankings of the players as a DataFrame."""
        if self.src_ranking is None:
            ressource = pkg_resources.files("asbg.teams.data").joinpath("example-rankings.csv")
            with pkg_resources.as_file(ressource) as filename:
                self.src_ranking = filename

        self.logger.debug(f"Loading the rankings from `{self.src_ranking}`...")

        return pl.read_csv(self.src_ranking, separator=";")

    def load_criteria(self) -> pl.DataFrame:
        """Loads the criteria of the players as a DataFrame."""
        if self.src_criteria is None:
            ressource = pkg_resources.files("asbg.teams.data").joinpath("example-criteria-wide.csv")
            with pkg_resources.as_file(ressource) as filename:
                self.src_criteria = filename

        self.logger.debug(f"Loading the criteria from `{self.src_criteria}`...")

        return pl.read_csv(self.src_criteria, separator=";")

    def load_config_file(self) -> dict[str, Any]:
        """Loads the config file."""
        ressource = pkg_resources.files("asbg.config").joinpath("teams.yaml")
        with pkg_resources.as_file(ressource) as filename:
            self.logger.debug(f"Loading the config file from `{filename}`...")
            with open(filename, "r") as f:
                return yaml.safe_load(f.read())["criteria"]

    def get_subcriteria_names(self, cfg: dict[str, Any]) -> list[str]:
        """Gets the subcriteria names from the config.

        Args:
            cfg: The config from which to parse the subcriteria names.

        Returns:
            The subcriteria names parsed from the config.
        """
        self.logger.debug("Getting the subcriteria names from the config...")

        subcriteria = []

        for _, values in cfg.items():
            subcriteria.extend(values["subcriteria"])

        return subcriteria

    def get_subcriteria_weights(self, cfg: dict[str, Any]) -> dict[str, float]:
        """Gets the weights of the subcriteria from the config.

        Args:
            cfg: The config from which to parse the subcriteria weights.

        Returns:
            The subcriteria weights parsed from the config.
        """
        self.logger.debug("Computing the weight of each subcriterion...")

        weights = {}

        for _, values in cfg.items():
            criteria_weight = values["weight"]
            for subcriterion, weight in values["subcriteria"].items():
                weights[subcriterion] = criteria_weight * weight

        if sum(weights.values()) != 1:
            raise ValueError("The weights of the subcriteria do not sum to one.")

        return weights

    def save_rankings(self, rankings: dict[str, pl.DataFrame]) -> None:
        """Saves the rankings by gender.

        Args:
            rankings: The rankings by gender.
        """
        cols = ["licence", "nom", "prenom", "genre", "ranking", "score"]

        for gender, ranking in rankings.items():
            gender = gender.casefold()
            ressource = pkg_resources.files("asbg.teams.data").joinpath(f"rankings-{gender}.csv")

            with pkg_resources.as_file(ressource) as filename:
                self.logger.debug(f"Writing the rankings to `{filename}`")
                ranking.select(cols).write_csv(filename, separator=";")
