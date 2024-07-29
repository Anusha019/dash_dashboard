from dash import Dash, dcc,html,Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px

app = Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

df=pd.read_csv('gapminderDataFiveYear.csv')

app.layout=dbc.Container(
    [
        dcc.Dropdown(
            options=[{'label': country, 'value': country} for country in df['country'].unique()],
            value=['Brazil','Albania','India'],
            multi=True,
            id='country'),

        dcc.Graph(id='selected_country')
    ]
)

@app.callback(
    Output('selected_country', 'figure'),
    Input('country', 'value')
)

def update_figure(country):
    filtered_df=df[df['country'].isin(country)]
    filtered_df=filtered_df.groupby(['country'])['gdpPercap'].sum().reset_index()
    fig = px.pie(filtered_df, values="gdpPercap", names="country", title='GDP in different countries of the world from 1952 to 2007')
    fig.update_layout()

    return fig

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)