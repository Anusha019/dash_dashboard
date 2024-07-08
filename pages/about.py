# Callback to update the page content based on the URL
from dash import Dash,dcc,html,dash_table,Input, Output
import dash_bootstrap_components as dbc
import pandas as pd


gapMinder=pd.read_csv('gapminderDataFiveYear.csv')

about_layout = html.Div([

    html.H1("About Page"),
    html.H3("Introduction to GapMinder", style={"textAlign": "center"}),
    html.Label("Show no of rows"),
    dcc.Dropdown(id="page_size",
                 options=[{"label": "10", "value": 10},
                          {"label": "50", "value": 50},
                          {"label": "70", "value": 70}],value=10,style={"width": "50%"}),

    dash_table.DataTable(id="data_table",data=gapMinder.to_dict("records"),page_size=10,
              columns=[{"name": "continent", "id": "continent"},
                       {"name": "country", "id": "country"},
                       {"name": "Population", "id": "pop"},
                       {"name": "Life expectancy", "id": "lifeExp"}]),
    dbc.Row([
        dbc.Col(
            dcc.Dropdown(id="continent",options=gapMinder["continent"].unique(),value='Asia'),
            style={"width": 300}
        ),
        dbc.Col(
            dcc.Dropdown(id="country",options=gapMinder["country"].unique(),value='India',multi=True),
            style={"width": 300},
        ),
        dbc.Col(
            dcc.Slider(id="pop_slider",min=gapMinder['pop'].min(), max=gapMinder['pop'].max(),value=gapMinder['pop'].min()),
            style={"width": 300},
        ),
        dbc.Col(
            dcc.Slider(id="exp_slider",min=gapMinder["lifeExp"].min(),max=gapMinder["lifeExp"].max(),value=60),
            style={"width": 300},
        ),
    ],
    style={"justify-content": "space-between",
           "display": "flex",
           "flex": 1}
    ),
    html.Button("Download CSV", id="btn_download_csv"),
    dcc.Download(id="download_csv"),
])

def register_callbacks(app):
    @app.callback(
        Output("data_table", "data"),
        [Input("continent", "value"),
        Input("country", "value"),
        Input("pop_slider", "value"),
        Input("exp_slider", "value")])

    def update_dataframe(value_continent, value_country, value_pop, value_exp):
        df = gapMinder[(gapMinder["continent"] == value_continent)& (gapMinder["country"].isin(value_country))]
        df = df[(df["pop"] >= value_pop) & (df["lifeExp"] >= value_exp)]
        return df.to_dict("records")

    @app.callback(
        Output("country", "options"),
        [Input("continent", "value")])

    def country_list(value_continent):
        df = gapMinder[gapMinder["continent"] == value_continent]
        return [{"label": country, "value": country} for country in df["country"].unique()]

    @app.callback(
        Output("data_table", "page_size"),
        [Input("page_size", "value")])

    def update_page_size(page_size):
        if page_size is None:
            raise PreventUpdate
        return page_size


    @app.callback(
        Output("download_csv", "data"),
        [Input("btn_download_csv", "n_clicks"), Input("data_table", "data")])

    def download_csv(n_clicks, data):
        if n_clicks is not None:
            df = pd.DataFrame(data)
            csv_string = df.to_csv(index=False, encoding="utf-8")
            return dict(content=csv_string, filename="data.csv")

def layout():
    return about_layout
