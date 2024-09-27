from dash import Dash,dcc,html,Input,Output
import dash_bootstrap_components as dbc
import pandas as pd

# Import page layouts
from pages import about,input,simulation


app = Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

gapMinder=pd.read_csv('D:/ML Apps/Dash/multipage/gapminderDataFiveYear.csv')

# Add a placeholder for the page content
app.layout = html.Div([
    dcc.Store(id="valid_user", data=0),
    dcc.Store(id="lat_store", data=56),
    dcc.Store(id="long_store", data=45),
    dcc.Store(id="data_store", data="year"),
    dcc.Store(id="country_store", data="India"),
    dcc.Location(id="url", refresh=False),  # Location component to track the URL

    dbc.Row(children=[html.Div([
        dbc.Row([
            dbc.Col(children=[
                html.Img(src="https://www.tigeranalytics.com/wp-content/uploads/2023/09/TA-Logo-resized-for-website_.png",  # Replace with your logo URL
                         style={"height": "50px","width": "120px","backgroundColor": "white"},)], # Adjust size as needed
                         style={"width": 200}),
            dbc.Col(children=[
                dcc.Link("About",href="/page-1",style={"color": "white","float": "left","width": 70},),  # Link to Page 1
                dcc.Link("Input field",href="/page-2",style={"color": "white","display": "inline-flex","width": 85}),  # Link to Page 2
                dcc.Link("Simulation",href="/page-3",style={"color": "white","width": 80}),  # Link to Page 3
            ],
            style={"backgroundColor": "blue", "height": 50}),
            dbc.Row( id="page-content",children=about.layout())
        ]),
    ])
    ])
    ])

@app.callback(
    Output("page-content", "children"),
    [Input("url", "pathname")]
)
def display_page(pathname):
       if pathname == "/page-1":
          return about.layout()
       elif pathname == "/page-2":
          return input.layout()
       elif pathname == "/page-3":
           return simulation.layout()
       else:
           return about.layout()

# Register callbacks for each page
about.register_callbacks(app)
input.register_callbacks(app)
simulation.register_callbacks(app)

if __name__ == "__main__":
    app.run_server(debug=True)