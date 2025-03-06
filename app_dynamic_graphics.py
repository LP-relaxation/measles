# These functions/components CHANGE based on callbacks
#   -- contains results from simulations based on user inputs

from dash import Dash, html, dcc, callback, Output, Input, State
import dash_bootstrap_components as dbc

from app_styles import BASE_FONT_FAMILY_STR, SELECTOR_NOTE_STYLE, RESULTS_HEADER_STYLE


def results_header():
    return dbc.Row(
        [
            # Chance of an Outbreak
            dbc.Col(
                dbc.Card(
                    dbc.CardBody(
                        [
                            html.Div(
                                [
                                    dcc.Markdown(id='outbreak',
                                                 children='Chance of exceeding 20 new infections',
                                                 style={**RESULTS_HEADER_STYLE, 'fontWeight': '500'}
                                                 ),
                                    dcc.Markdown(id='prob_20plus_new_str',
                                                 style={**RESULTS_HEADER_STYLE, 'color': '#bf5700',
                                                        "font-size": "22pt", "font-weight": "800"}
                                                 ),
                                ],
                                style={
                                    'textAlign': 'center',
                                    'fontFamily': BASE_FONT_FAMILY_STR,
                                    'fontSize': '18pt',
                                    'border': 'none'
                                }
                            )
                        ]
                    ),
                    style={'border': 'none'}
                ),
            ),

            # Expected Outbreak Size
            dbc.Col(
                dbc.Card(
                    dbc.CardBody(
                        [
                            html.Div(
                                [
                                    dcc.Markdown(id='cases',
                                                 children='Likely outbreak size',
                                                 style={'color': '#black', 'fontWeight': '500',
                                                        'font-size': '20pt', 'margin': 'none'}
                                                 ),
                                    dcc.Markdown("*if exceeds 20 new infections*",
                                                 style={'font-size': '14pt', "margin": "none"}),
                                    dcc.Markdown(id='cases_expected_over_20_str',
                                                 style={'color': '#bf5700', 'fontWeight': '800',
                                                        'font-size': '22pt', 'margin-top': '0.5em'}
                                                 ),
                                ],
                                style={
                                    'textAlign': 'center',
                                    'fontFamily': BASE_FONT_FAMILY_STR,
                                    'fontSize': '18pt',
                                    'border': 'none'
                                }
                            )
                        ]
                    ),
                    style={'border': 'none'}
                ),
                style={'borderLeft': '3px solid #bf5700'}
            ),
        ],
    )


def spaghetti_plot_section():
    return dbc.Row([
                    dbc.Col(
                        dbc.Card(
                            dbc.CardBody([
                                html.H3("This graph shows 20 plausible school outbreak curves.",
                                        style={"text-align": "center", "margin-top": "1em", "margin-bottom": "1em",
                                               "margin-left": "1.8em",
                                               "font-family": BASE_FONT_FAMILY_STR,
                                               "font-size": "14pt", "font-weight": "400", "font-style": "italic"}),
                                dcc.Graph(id="spaghetti_plot"),
                            ]),
                            style={'border': 'none', 'padding': '0'},
                        ),
                    ),
                ], style={"border-top": "2px solid black", "border-left": "1em", "padding": "none", "height": "60%",
                          "width": "100%", "margin-top": "1em"})