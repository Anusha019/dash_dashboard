from dash import Dash,dcc,html,Input, Output,State
import dash_bootstrap_components as dbc
import pandas as pd


input_layout=dbc.Container([
    dbc.Row([
        dbc.Col([
            html.H3("User Input"),
            html.Hr(style={"border-width": "3px"}),
            html.Div([
                dbc.Row([
                    html.Label('Latitude: *',style={"width": "150px","display": "inline-block"}),
                    dcc.Input(id="lat", type="number", placeholder="Latitude",
                              style={"width":'300px',"display": "inline-block","height": 30})
                ]),
                dbc.Row([
                    html.Label('Longitude: *',style={"width": "150px","display": "inline-block"}),
                    dcc.Input(id="long", type="number", placeholder="Longitude",style={"width":'300px'})
                ]),
                dbc.Row([
                    html.Label('Data: *',style={"width": "150px","display": "inline-block"}),
                    dcc.Input(id="data", type="text", placeholder="Enter dataset GDP vs (country or year)",style={"width":'300px'})
                ]),
                dbc.Row([
                    html.Label('Country: *',style={"width": "150px","display": "inline-block"}),
                    dcc.Input(id="country", type="text", placeholder="Enter a country name",style={"width":'300px'})
                ]),
            ]),
        ]),
        dbc.Col([
            html.H3("Calculated Output"),
            html.Hr(style={"border-width": "1px"}),
            html.Div(id="output_gen_display"),
        ],style={"width": "50%"})
    ]),

    html.Button(id='submit',n_clicks=0,children='SIMULATE',style={"margin": "auto", "display": "block"})

])

def register_callbacks(app):
    @app.callback(
        [Output('lat', 'children'),Output('long', 'children'),Output('data', 'children'),Output('country', 'children')],
        [Input('submit','n_clicks')],
        [State('lat', 'value'),State('long', 'value'),State('data', 'value'),State('country', 'data')]
        )

    def update(n_clicks,lat,long,data,country):
        if (data != "country") & (data != "year"):
            raise PreventUpdate
        country_list = gapMinder["country"].unique().tolist()

        if country not in country_list:
            raise PreventUpdate
        out_1 = lat
        out_2 = long
        out_3 = data
        out_4 = country
        return out_1, out_2, out_3, out_4

    @app.callback(
        Output("output_gen_display", "children"),
        Input("simulate-button", "n_clicks")
        )

    def output_gen(clicks):
        if clicks is None:
            raise PreventUpdate
        return "Output generated"

def layout():
    return input_layout