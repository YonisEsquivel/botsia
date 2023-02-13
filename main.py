import dash
import pandas as pd
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
from dash.dependencies import Input, Output, State
from helpers.functions import *
from components.NavBarHor import NavBarHor


app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP, './assets/styles.css'], use_pages=True, prevent_initial_callbacks=True)

def ContentLayout():
    return html.Div(children=[
        dash.page_container
    ], style={ "padding": "2rem 1rem" })

def save_layout():
    return html.Div(children=[
            dcc.Store(id='local-storage', storage_type='local'),
            dcc.Store(id='memory'),
            dcc.Location(id="url"),
            NavBarHor(),
            ContentLayout(),
            dcc.Interval(
                    id='refresh_data_trading',
                    interval=5*1000,
                    n_intervals=0
                ),
        ], style={
            "backgroundColor":"#161A1E",
            "color":"white",
        })

app.layout = save_layout

def page404(pathname):
    return html.Div(
                dbc.Container(
                    [
                        html.H1("404: Not found", className="text-danger"),
                        html.Hr(),
                        html.P(f"The pathname {pathname} was not recognised..."),
                    ],
                    fluid=True,
                    className="py-3",
                ),
                className="h-100 p-5 text-white bg-dark rounded-3",
            )


@app.callback(
    Output("navbar-collapse", "is_open"),
    [Input("navbar-toggler", "n_clicks")],
    [State("navbar-collapse", "is_open")],
)

def toggle_navbar_collapse(n, is_open):
    if n:
        return not is_open
    return is_open


if __name__ == '__main__':
    app.run_server(debug=True, port=3000)