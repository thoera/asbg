import dash
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
from dash import dash_table, dcc, html
from plotly.graph_objects import Figure

from asbg.interclubs.results import FormatResults
from asbg.utils.database import connect, fetch_results


con = connect()
results = fetch_results(con)

res = FormatResults()

results_aggregated = res.aggregate_results(results).reset_index()

results_mixed = res.filter_results(results, competition="Interclubs Comité 75 D1")
results_mixed = res.aggregate_results(results_mixed).reset_index()

results_men = res.filter_results(results, competition="Interclubs Comité 75 D1 Masculin")
results_men = res.aggregate_results(results_men).reset_index()

results_women = res.filter_results(results, competition="Interclubs Comité 75 D1 Féminin")
results_women = res.aggregate_results(results_women).reset_index()

results_veterans = res.filter_results(results, competition="Interclubs Comité 75 D1 Vétérans")
results_veterans = res.aggregate_results(results_veterans).reset_index()

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("2023-2024", href="#")),
        dbc.DropdownMenu(
            children=[dbc.DropdownMenuItem("2022-2023", href="#")],
            nav=True,
            in_navbar=True,
            label="Saisons précédentes",
        ),
    ],
    brand="Association Sportive des Badistes Givrés",
    brand_href="https://asbg75.fr",
    color="light",
    fluid=True,
)

percentage = dash_table.FormatTemplate.percentage(decimals=1)


def format_table(data: pd.DataFrame, title: str, width: int = 6, offset: int = 0) -> dbc.Col:
    table = dbc.Col(
        [
            html.Br(),
            dash_table.DataTable(
                data.to_dict("records"),
                columns=[
                    {"id": "discipline", "name": "Discipline"},
                    {"id": "wins", "name": "Nombre de victoires"},
                    {"id": "losses", "name": "Nombre de défaites"},
                    {
                        "id": "win_percentage",
                        "name": "Pourcentage de victoires (%)",
                        "type": "numeric",
                        "format": percentage,
                    },
                ],
                style_as_list_view=True,
                style_cell_conditional=[{"if": {"column_id": "discipline"}, "textAlign": "left"}],
                style_header={"backgroundColor": "white", "fontSize": 14},
                style_cell={"fontSize": 14},
            ),
            html.P(
                [
                    "Source : ",
                    html.A("https://icbad.ffbad.org", href="https://icbad.ffbad.org"),
                ],
                style={"margin-top": "1rem", "font-size": "0.9rem"},
            ),
        ],
        width={"size": width, "offset": offset},
    )

    fig = format_barplot(data)
    fig = dbc.Col(dcc.Graph(figure=fig), width={"size": 5, "offset": 1})

    return [
        html.Br(),
        dbc.Col(html.H3(title), width={"size": 11, "offset": 1}),
        dbc.Row([table, fig]),
    ]


def format_barplot(data: pd.DataFrame) -> Figure:
    fig = px.bar(
        data,
        x="discipline",
        y="win_percentage",
        width=600,
        height=400,
        template="simple_white",
        title="Pourcentage de victoires par discipline (%)",
    )

    fig.update_xaxes(ticks="")
    fig.update_yaxes(range=[0, 1], tickformat=",.0%")
    fig.update_layout(xaxis_title=None, yaxis_title=None)
    fig.add_shape(
        type="line",
        line_color="salmon",
        line_width=3,
        opacity=1,
        line_dash="dot",
        x0=0,
        x1=1,
        xref="paper",
        y0=0.5,
        y1=0.5,
        yref="y",
    )
    fig.update_traces(hovertemplate=None, hoverinfo="skip")

    return fig


layout = [
    navbar,
    html.Br(),
    dbc.Row(
        [
            dbc.Col(
                [
                    html.H1("Résultats des joueuses et joueurs de l'ASBG lors des Interclubs 🏅"),
                    html.Hr(),
                    html.P("""
                        Les résultats sont ceux de l'ensemble de l'année 2023-2024
                        au moment où les données ont été collectées,
                        il est donc possible que de nouveaux matchs se soient déroulés depuis.
                        Afin d'avoir les dernières données disponibles,
                        il est recommandé de relancer la collecte régulièrement.
                    """),
                ],
                width={"size": 10, "offset": 1},
            )
        ]
    ),
]

if len(results_aggregated):
    layout.extend(
        format_table(
            results_aggregated,
            "Résultats de l'ensemble des équipes",
            width=5,
            offset=1,
        )
    )

if len(results_mixed):
    layout.extend(format_table(results_mixed, "Résultats des équipes mixtes", width=5, offset=1))

if len(results_men):
    layout.extend(format_table(results_men, "Résultats des équipes masculines", width=5, offset=1))

if len(results_women):
    layout.extend(format_table(results_women, "Résultats des équipes féminines", width=5, offset=1))

if len(results_veterans):
    layout.extend(
        format_table(results_veterans, "Résultats des équipes vétérans", width=5, offset=1)
    )

app.layout = dbc.Container(layout, fluid=True)

if __name__ == "__main__":
    app.run()
