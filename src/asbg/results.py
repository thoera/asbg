"""This module formats the results to feed to the streamlit application."""

import importlib.resources as pkg_resources
import sqlite3

import pandas as pd

from asbg.logger import get_logger

logger = get_logger()

with pkg_resources.as_file(pkg_resources.files("asbg.data")) as dir:
    DATABASE_FILE = dir / "data.db"


DISCIPLINES = ["SH", "SD", "DH", "DD", "DX"]


class FormatResults:
    """Formats the results of the Interclubs to feed to the streamlit application."""

    @staticmethod
    def get_results() -> pd.DataFrame:
        """Gets the results of the Interclubs from the database."""
        logger.debug("Connecting to the database `data.db`")

        con = sqlite3.connect(DATABASE_FILE)

        query = """
            SELECT
                result.team_id,
                team.competition,
                result.discipline,
                result.wins,
                result.losses
            FROM result
            INNER JOIN team ON result.team_id = team.team_id
        """

        with con:
            res = con.execute(query)
            rows = res.fetchall()

        cols = ["team_id", "competition", "discipline", "wins", "losses"]

        return pd.DataFrame(data=rows, columns=cols)

    @staticmethod
    def filter_results(results: pd.DataFrame, competition: str) -> pd.DataFrame:
        """Filters the results to only keep those of the given competition.

        Args:
            results: The results of the Interclubs.
            competition: The competition for which to filter the results.

        Returns:
            The filtered results for the given competition.
        """
        return results.loc[results["competition"] == competition, :]

    def aggregate_results(self, results: pd.DataFrame) -> pd.DataFrame:
        """Aggregates the results to show them intelligibly.

        Args:
            results: The results to aggregate.

        Returns:
            The aggregated results.
        """
        results = (
            results.loc[:, ["discipline", "wins", "losses"]].groupby("discipline").sum()
        )

        results["win_percentage"] = results["wins"] / results.sum(axis="columns")

        results = results.reindex(DISCIPLINES)

        return self._remove_disciplines_not_played(results)

    @staticmethod
    def _remove_disciplines_not_played(results: pd.DataFrame) -> pd.DataFrame:
        """Removes from the results the disciplines which have not been played.

        Args:
            results: The results from which to remove the disciplines.

        Returns:
            The results without the disciplines which have not been played.
        """
        return results.loc[results.sum(axis=1) > 0, :]
