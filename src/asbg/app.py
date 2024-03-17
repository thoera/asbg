"""This module builds the streamlit app to visualize the results of the Interclubs."""

import streamlit as st

from asbg.results import FormatResults

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


def app():
    res = FormatResults()
    results = res.get_results()

    st.set_page_config(
        page_title="Résultats ASBG75",
        layout="wide",
    )

    st.title("Résultats des joueuses et joueurs de l'ASBG 75 lors des Interclubs")

    st.caption(
        "Les résultats sont ceux de l'ensemble de l'année 2023-2024 "
        "au moment où les données ont été collectées, "
        "il est donc possible que de nouveaux matchs se soient déroulés depuis. "
        "Afin d'avoir les dernières données disponibles, "
        "il est souhaitable de relancer la collecte régulièrement."
    )

    col1, col2 = st.columns(2)

    with st.container():
        col1.subheader("Résultats de l'ensemble des équipes")
        results_aggregated = res.aggregate_results(results)
        col1.dataframe(results_aggregated, column_config=COLUMN_CONFIG)

    with st.container():
        col1.subheader("Résultats des équipes mixtes")
        results_mixed = res.filter_results(
            results, competition="Interclubs Comité 75 D1"
        )
        results_mixed = res.aggregate_results(results_mixed)
        col1.dataframe(results_mixed, column_config=COLUMN_CONFIG)

        col2.subheader("Résultats des équipes vétérans")
        results_veterans = res.filter_results(
            results, competition="Interclubs Comité 75 D1 Vétérans"
        )
        results_veterans = res.aggregate_results(results_veterans)
        col2.dataframe(results_veterans, column_config=COLUMN_CONFIG)

    with st.container():
        col1.subheader("Résultats des équipes masculines")
        results_men = res.filter_results(
            results, competition="Interclubs Comité 75 D1 Masculin"
        )
        results_men = res.aggregate_results(results_men)
        col1.dataframe(results_men, column_config=COLUMN_CONFIG)

        col2.subheader("Résultats des équipes féminines")
        results_women = res.filter_results(
            results, competition="Interclubs Comité 75 D1 Féminin"
        )
        results_women = res.aggregate_results(results_women)
        col2.dataframe(results_women, column_config=COLUMN_CONFIG)


if __name__ == "__main__":
    app()
