"""This module draws the players to constitute different Interclubs teams."""

import importlib.resources as pkg_resources
import sys
from typing import Any

import polars as pl
import yaml
from tabulate import tabulate

from asbg.utils.logger import get_logger


class DrawPlayers:
    def __init__(self) -> None:
        self.logger = get_logger(__name__)

    def draw_players(self) -> None:
        """Validates the number of teams and draws the players for each one."""
        cfg = self.load_config_file()
        ranked_players = self.load_ranked_players()
        self.validate_number_of_teams(cfg, ranked_players)
        self.draw_players_per_team(cfg, ranked_players)

    def draw_players_per_team(
        self, cfg: dict[str, Any], ranked_players: dict[str, pl.DataFrame]
    ) -> None:
        """Draws the players for each team and logs the results.

        Args:
            cfg: The config to use to determine the number of teams and number of players needed.
            ranked_players: The ranked players by gender.
        """
        ranked_players_women = ranked_players["women"].to_dicts()
        ranked_players_men = ranked_players["men"].to_dicts()

        for team, composition in cfg.items():
            n_teams = composition["number"]
            for i in range(1, n_teams + 1):
                self.logger.info(f"The players selected for the {team} team #{i} are:")

                women = composition.get("women", 0)
                if women > 0:
                    women_selected = ranked_players_women[:women]
                    del ranked_players_women[:women]
                    print(
                        tabulate(
                            women_selected,
                            headers="keys",
                            showindex=False,
                            tablefmt="rounded_outline",
                        )
                    )

                men = composition.get("men", 0)
                if men > 0:
                    men_selected = ranked_players_men[:men]
                    del ranked_players_men[:men]
                    print(
                        tabulate(
                            men_selected,
                            headers="keys",
                            showindex=False,
                            tablefmt="rounded_outline",
                        )
                    )

    def validate_number_of_teams(
        self, cfg: dict[str, Any], ranked_players: dict[str, pl.DataFrame]
    ) -> None:
        """Validates if it's possible to fill the number of teams configured.

        Args:
            cfg: The config to use to determine the number of teams and number of players needed.
            ranked_players: The ranked players by gender.
        """
        number_of_women_needed = 0
        number_of_men_needed = 0

        for team, composition in cfg.items():
            n_teams = composition["number"]
            self.logger.debug(f"Number of {team} team(s) configured: {n_teams}")

            women = composition.get("women", 0)
            if women > 0:
                self.logger.debug(f"The number of women needed for each {team} team is: {women}")
            number_of_women_needed += n_teams * women

            men = composition.get("men", 0)
            if men > 0:
                self.logger.debug(f"The number of men needed for each {team} team is: {men}")
            number_of_men_needed += n_teams * men

        self.logger.debug(f"The total number of women needed is: {number_of_women_needed}")
        self.logger.debug(f"The total number of men needed is: {number_of_men_needed}")

        error = 0

        ranked_players_women = len(ranked_players["women"])
        if ranked_players_women < number_of_women_needed:
            self.logger.error(
                f"There is not enough women available ({ranked_players_women}) "
                f"for the number of teams configured. Try to decrease the number of teams."
            )
            error += 1

        ranked_players_men = len(ranked_players["men"])
        if ranked_players_men < number_of_men_needed:
            self.logger.error(
                f"There is not enough men available ({ranked_players_men}) "
                f"for the number of teams configured. Try to decrease the number of teams."
            )
            error += 1

        if error > 0:
            sys.exit(1)

        self.logger.info(
            f"There is enough players available ({ranked_players_men} men "
            f"and {ranked_players_women} women) for the number of teams configured"
        )

    def load_ranked_players(self) -> dict[str, pl.DataFrame]:
        """Loads the ranked players."""
        ranked = {}

        ressource = pkg_resources.files("asbg.teams.data").joinpath("rankings-femme.csv")
        with pkg_resources.as_file(ressource) as filename:
            self.logger.debug(f"Loading the ranked women from `{filename}`...")
            ranked["women"] = pl.read_csv(filename, separator=";")

        ressource = pkg_resources.files("asbg.teams.data").joinpath("rankings-homme.csv")
        with pkg_resources.as_file(ressource) as filename:
            self.logger.debug(f"Loading the ranked men from `{filename}`...")
            ranked["men"] = pl.read_csv(filename, separator=";")

        return ranked

    def load_config_file(self) -> dict[str, Any]:
        """Loads the config file."""
        ressource = pkg_resources.files("asbg.config").joinpath("teams.yaml")
        with pkg_resources.as_file(ressource) as filename:
            self.logger.debug(f"Loading the config file from `{filename}`...")
            with open(filename, "r") as f:
                return yaml.safe_load(f.read())["teams"]
