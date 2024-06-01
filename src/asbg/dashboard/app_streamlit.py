"""This module builds the streamlit app to visualize the results of the Interclubs."""

import streamlit as st

from asbg.interclubs.constants import COMPETITIONS, HEADERS
from asbg.interclubs.database import connect, fetch_results
from asbg.interclubs.results import FormatResults


COLUMN_CONFIG = {
    "discipline": st.column_config.Column(HEADERS["discipline"]),
    "wins": st.column_config.Column(HEADERS["wins"]),
    "losses": st.column_config.Column(HEADERS["losses"]),
    "win_percentage": st.column_config.ProgressColumn(
        HEADERS["win_percentage"],
        min_value=0,
        max_value=1,
    ),
}


def app() -> None:
    """Creates the streamlit app."""
    st.set_page_config(page_title="Résultats ASBG", layout="wide")

    con = connect()
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
        results_mixed = res.filter_results(results, competition=COMPETITIONS["mixed"])
        results_mixed = res.aggregate_results(results_mixed)
        col2.dataframe(results_mixed, column_config=COLUMN_CONFIG)

    with st.container():
        col1.subheader("Résultats des équipes masculines")
        results_men = res.filter_results(results, competition=COMPETITIONS["men"])
        results_men = res.aggregate_results(results_men)
        col1.dataframe(results_men, column_config=COLUMN_CONFIG)

        col2.subheader("Résultats des équipes féminines")
        results_women = res.filter_results(results, competition=COMPETITIONS["women"])
        results_women = res.aggregate_results(results_women)
        col2.dataframe(results_women, column_config=COLUMN_CONFIG)

    with st.container():
        col1.subheader("Résultats des équipes vétérans")
        results_veterans = res.filter_results(results, competition=COMPETITIONS["veterans"])
        results_veterans = res.aggregate_results(results_veterans)
        col1.dataframe(results_veterans, column_config=COLUMN_CONFIG)


if __name__ == "__main__":
    app()
