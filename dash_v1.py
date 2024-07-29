from dash import Dash, dcc
import dash_bootstrap_components as dbc
import plotly.express as px

app = Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

tips = px.data.tips()

app.layout=dbc.Container(
    [
        dbc.Select(options=tips['day'].unique(),value='Sun'),
        dcc.Graph(figure=px.bar(tips,  x="sex", y="total_bill",color="smoker",barmode="group"))
    ]
)

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)