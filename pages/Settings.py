import dash
from dash import html
import dash_bootstrap_components as dbc
from helpers.dbconnect import *
from components.FormSettingsGral import *
from components.FormSettingsSymbol import *
from components.ListSettingsSymbols import *

dash.register_page(__name__)

def layout():
    return  html.Div([
                dbc.Row([
                    dbc.Col(html.Div(id="column-top-left", children= [html.H1('Settings Botsia',style={'textAlign':'center'})]), md=12),
                ]),
                dbc.Row([
                    dbc.Col(html.Div(id="column-top-center", children= ShowFormConfigGral()), md=3),
                    dbc.Col(html.Div(id="column-top-center", children= ShowFormSettingSymbol()), md=9),
                ]),
                html.Hr(),
                dbc.Row([
                    dbc.Col(html.Div(id="column-top-left", children= ShowListSymbols() ), md=12),
                ])
            ])