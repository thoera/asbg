"""This module builds the streamlit app to visualize the results of the Interclubs."""

import importlib.resources as pkg_resources
import sqlite3

import pandas as pd
import streamlit as st

from asbg.interclubs.results import FormatResults
from asbg.utils.logger import get_logger


def establish_connection() -> sqlite3.Connection:
    """Establishes a connection to the database.

    Returns:
        A Connection object to the database.
    """
    with pkg_resources.as_file(pkg_resources.files("asbg.data")) as dir:
        DATABASE_FILE = dir / "data.db"

    return sqlite3.connect(DATABASE_FILE)


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


COLUMN_CONFIG = {
    "discipline": st.column_config.Column("Discipline"),
    "wins": st.column_config.Column("Nombre de victoires"),
    "losses": st.column_config.Column("Nombre de défaites"),
    "win_percentage": st.column_config.ProgressColumn(
        "Pourcentage de victoires (%)",
        min_value=0,
        max_value=1,
    ),
}


def app() -> None:
    """Creates the streamlit app."""
    st.set_page_config(page_title="Résultats ASBG", layout="wide")

    con = establish_connection()
    results = fetch_results(con)

    res = FormatResults()

    st.header(
        "Résultats des joueuses et joueurs de l'ASBG lors des Interclubs " ":sports_medal:",
        divider="rainbow",
    )

    st.caption(
        "Les résultats sont ceux de l'ensemble de l'année 2023-2024 "
        "au moment où les données ont été collectées, "
        "il est donc possible que de nouveaux matchs se soient déroulés depuis. "
        "Afin d'avoir les dernières données disponibles, "
        "il est recommandé de relancer la collecte régulièrement."
    )

    col1, col2 = st.columns(2)

    with st.container():
        col1.subheader("Résultats de l'ensemble des équipes")
        results_aggregated = res.aggregate_results(results)
        col1.dataframe(results_aggregated, column_config=COLUMN_CONFIG)

        col2.subheader("Résultats des équipes mixtes")
        results_mixed = res.filter_results(results, competition="Interclubs Comité 75 D1")
        results_mixed = res.aggregate_results(results_mixed)
        col2.dataframe(results_mixed, column_config=COLUMN_CONFIG)

    with st.container():
        col1.subheader("Résultats des équipes masculines")
        results_men = res.filter_results(results, competition="Interclubs Comité 75 D1 Masculin")
        results_men = res.aggregate_results(results_men)
        col1.dataframe(results_men, column_config=COLUMN_CONFIG)

        col2.subheader("Résultats des équipes féminines")
        results_women = res.filter_results(results, competition="Interclubs Comité 75 D1 Féminin")
        results_women = res.aggregate_results(results_women)
        col2.dataframe(results_women, column_config=COLUMN_CONFIG)

    with st.container():
        col1.subheader("Résultats des équipes vétérans")
        results_veterans = res.filter_results(
            results, competition="Interclubs Comité 75 D1 Vétérans"
        )
        results_veterans = res.aggregate_results(results_veterans)
        col1.dataframe(results_veterans, column_config=COLUMN_CONFIG)


if __name__ == "__main__":
    app()
