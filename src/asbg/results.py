"""This module formats the results to feed to the streamlit application."""

import importlib.resources as pkg_resources
import sqlite3

import pandas as pd
import streamlit as st

from asbg.logger import get_logger

logger = get_logger()


DISCIPLINES = ["SH", "SD", "DH", "DD", "DX"]


class FormatResults:
    """Formats the results of the Interclubs to feed to the streamlit application."""

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


@st.cache_resource()
def establish_connection() -> sqlite3.Connection:
    """Establishes a connection to the database.

    Returns:
        A Connection object to the database.
    """
    with pkg_resources.as_file(pkg_resources.files("asbg.data")) as dir:
        DATABASE_FILE = dir / "data.db"

    return sqlite3.connect(DATABASE_FILE)


@st.cache_data(ttl=3600)
def fetch_results(_con: sqlite3.Connection) -> pd.DataFrame:
    """Gets the results of the Interclubs from the database.

    Args:
        _con: A Connection object to the database.

    Returns:
        The results of the Interclubs fetched from the database.
    """
    logger = get_logger()
    logger.debug("Connecting to the database `data.db`")

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

    with _con:
        res = _con.execute(query)
        rows = res.fetchall()

    cols = ["team_id", "competition", "discipline", "wins", "losses"]

    return pd.DataFrame(data=rows, columns=cols)
