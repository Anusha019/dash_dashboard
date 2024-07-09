from dash import Dash,dcc, html,Input, Output,State
import dash_bootstrap_components as dbc
import dash_leaflet as dl
import pandas as pd
import plotly.express as px

df=pd.read_csv('D:/ML Apps/Dash/multipage/gapminderDataFiveYear.csv')

simulation_layout = html.Div([
    dl.Map(dl.TileLayer(),id="map_output",center=[20, 20],zoom=6,
           style={"height": 400,
                  "width": "95%",
                  "margin": "auto",
                  "marginTop": "30px"}),
    dbc.Row([
        dbc.Col([html.Div(children=[html.Div("User provided fields")],
                          style={"border": "2px solid #0074D9",
                                 "padding": "10px",
                                 "margin": "10px",
                                 "background-color": "blue",
                                 "color": "white",
                                 "text-align": "center"}),
                html.Div([dbc.Row([
                    html.Label("Latitude:",style={"width": "150px",
                                                  "display": "inline-block",
                                                  "text-align": "center"}),
                    html.Div(id="lat_display",style={"background-color": "lightgray","width": 300,
                                                     "display": "inline-block"})
                        ]),
                    html.Hr(),
                    dbc.Row([
                        html.Label("Longitude:",style={"width": "150px","display": "inline-block",
                                                       "text-align": "center"}),
                        html.Div(id="log_display",style={"width": "300px","display": "inline-block",
                                                         "background-color": "lightgray"}),
                    ]),
                    html.Hr(),
                    dbc.Row([
                        html.Label("State:",style={"width": "150px","display": "inline-block",
                                                       "text-align": "center"}),
                        html.Div(id="data_display",style={"width": "300px","display": "inline-block",
                                                         "background-color": "lightgray"}),
                    ]),
                    html.Hr(),
                    dbc.Row([
                        html.Label("Country:",style={"width": "150px","display": "inline-block",
                                                       "text-align": "center"}),
                        html.Div(id="country_display",style={"width": "300px","display": "inline-block",
                                                         "background-color": "lightgray"}),
                    ]),
                    html.Hr(),
                ]),
                ],style={"display": "inline-block","width": "49%"}),
        dbc.Col([
            html.Div(children=[html.Div("Country Data")],
                     style={"border": "2px solid #0074D9","padding": "10px","margin": "10px",
                            "background-color": "blue","color": "white","text-align": "center"}),
            html.Div([
                dbc.Row([
                    html.Label("Latest GDP",style={"width": "150px","display": "inline-block",
                                                   "text-align": "center"}),
                    html.Div(id="gdp_display",style={"background-color": "lightgray","width": 300,
                                                     "display": "inline-block"}),
                ]),
                html.Hr(),
                dbc.Row([
                    html.Label("Latest Population",style={"width": "150px","display": "inline-block",
                                                   "text-align": "center"}),
                    html.Div(id="pop_display",style={"background-color": "lightgray","width": 300,
                                                     "display": "inline-block"}),
                ]),
                html.Hr(),
                dbc.Row([
                    html.Label("Average Life Expectancy",style={"width": "150px","display": "inline-block",
                                                   "text-align": "center"}),
                    html.Div(id="life_display",style={"background-color": "lightgray","width": 300,
                                                     "display": "inline-block"}),
                ]),
            ]),
        ],
        style={"display": "inline-block","width": "50%"})],
        style={"justify-content": "space-between","display": "flex","flex": 1}),
        dcc.Graph(id="pop_plot"),
        dcc.Graph(id="gdp_plot"),
    ],
)


def register_callbacks(app):
    @app.callback(
        Output("lat_display", "children"),
        Output("log_display", "children"),
        Output("data_display", "children"),
        Output("country_display", "children"),
        [Input("lat_store", "data"),
        Input("long_store", "data"),
        Input("data_store", "data"),
        Input("country_store", "data")],
    )

    def input_display(lat, log, state, country):
        return lat, log, state, country

    @app.callback(
        Output("map_output", "children"),
        Output("map_output", "center"),
        [Input("lat_store", "data"), Input("long_store", "data")],
        )

    def simulation_map(latitude, longitude):
        if (latitude is None) & (longitude is None):
            raise PreventUpdate

        marker = dl.Marker(position=[latitude, longitude],
                        children=[dl.Tooltip(f"Latitude: {latitude}, Longitude: {longitude}")])
        center = [latitude, longitude]
        return [dl.TileLayer(), marker], center

    @app.callback(
            Output("gdp_display", "children"),
            Output("pop_display", "children"),
            Output("life_display", "children"),
            [Input("country_store", "data")],
        )

    def country_info(country):
        gdp_country = df[df["country"] == country]
        gdp = gdp_country[gdp_country["year"] == gdp_country["year"].max()]["gdpPercap"]

        pop_country = df[df["country"] == country]
        pop = pop_country[pop_country["year"] == pop_country["year"].max()]["pop"]

        life = df[df["country"] == country]["lifeExp"].mean()
        return gdp, pop, life


    @app.callback(
        Output("pop_plot", "figure"),
        [Input("country_store", "data")],
        )

    def update_bar_plot(selected_country):
        filtered_df = df[df["country"] == selected_country]

        fig = px.bar(filtered_df,x="year",y="pop",color="lifeExp",
                    labels={"pop": "Population", "lifeExp": "Life Expectancy"},
                    title=f"Bar Plot for {selected_country}")
        return fig


    @app.callback(
        Output("gdp_plot", "figure"),
        [Input("data_store", "data")],
        )

    def update_bar_plot(selected_state):
        X = selected_state
        fig = px.bar(df,x=X,y="gdpPercap",labels={"gdpPercap": "GDP per capita"},
                    title=f"GDP per capita over {selected_state}")
        return fig

def layout():
    return simulation_layout

