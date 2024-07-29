from dash import Dash, dcc,html
import dash_bootstrap_components as dbc
import plotly.express as px

app = Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

df = px.data.gapminder()

app.layout=dbc.Container(style={'backgroundColor': 'black'}, fluid=True,children=
    [
        html.H1(children='Dash bootstrap and core components',style={'textAlign': 'center','color': 'white'}),
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.Label('Dropdown'),
                        dcc.Dropdown(df['year'].unique(), value='1952',style={'color': 'white'}),
                    ]
                ),
                dbc.Col(
                    [
                        html.Label('Radio items'),
                        dcc.RadioItems(['New York City', 'Montréal', 'San Francisco'], 'Montréal',style={'color': 'white'})
                    ]
                )
            ],style={'backgroundColor': 'black', 'padding': '10px','color': 'white'}
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.Label('Slider'),
                        dcc.Slider(0, 10, 1, value=5),
                    ]
                ),
                dbc.Col(
                    [
                        html.Label('Text input'),
                        dcc.Textarea(placeholder='Enter a value...', value='Initial Text', style={'width': '100%','color': 'white', 'background-color': 'black'})
                    ]
                )
            ],style={'backgroundColor': 'black', 'padding': '10px','color': 'white'}
        )
    ]
)

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)