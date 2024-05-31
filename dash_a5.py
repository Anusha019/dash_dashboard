from dash import Dash, dcc,html,Input, Output,State
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px

app = Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

df=pd.read_csv('gapminderDataFiveYear.csv')

app.layout=dbc.Container(
    [
        dbc.Row([
            dbc.Col([
                dcc.Dropdown(
                    options=[{'label': country, 'value': country} for country in df['country'].unique()],
                    value=['Brazil','Albania','India'],
                    multi=True,
                    id='country'),

                dcc.Dropdown(
                    options=[{'label': year, 'value': year} for year in df['year'].unique()],
                    value=1972,
                    id='year')
            ])
        ]),

        dcc.Graph(id='selected_country'),
        dcc.Graph(id='scatter_plot')
    ]
)

@app.callback(
    [Output('selected_country', 'figure'),Output('scatter_plot', 'figure')],
    [Input('country', 'value'),Input('year', 'value')]
)

def update_figure(country,year):
    filtered_df=df[df['country'].isin(country)]
    filtered_dfc=filtered_df.groupby(['country'])['gdpPercap'].sum().reset_index()
    fig1 = px.pie(filtered_dfc, values="gdpPercap", names="country", title='GDP in different countries of the world from 1952 to 2007')
    filtered_df=filtered_df[filtered_df['year']==year]
    fig2 = px.scatter(filtered_df, x="gdpPercap", y="lifeExp",color='country',size='gdpPercap', size_max=30)
    fig2.update_traces(marker=dict(line=dict(width=3)))
    return fig1,fig2

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)