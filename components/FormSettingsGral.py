import dash
from dash import html, dcc, callback
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import pandas as pd
import config
import datetime

from helpers.functions import *
from helpers.dbconnect import *

@callback(
        Output(component_id='output-settings', component_property='children'),
        Input('confirm-update', 'submit_n_clicks'),
        [
            State(component_id='periodograph', component_property='value'),
            State(component_id='longitudgraph', component_property='value'),
            State(component_id='interval', component_property='value')
        ]
    )
def update_output(submit_n_clicks, pg, lg, i):
    print(submit_n_clicks)
    if submit_n_clicks:
        try:
            db = Conexion()
            cnx = db.mysqlConnect()

            sql = "UPDATE settings SET periodo_graph={}, longitud_graph={}, interval_klines='{}' WHERE id = 1 ".format(pg,lg,i)
            r1=db.prepare(sql,cnx)
            if not r1:
                raise Exception("fail update generak settings!")

            db.ejecutar()
            db.mysqlClose() 

            return dbc.Alert("Datos guardados con éxito!", color="success", duration=5000)
        except Exception as e:
            return dbc.Alert(e, color="danger", duration=5000)


@callback(
        Output('confirm-update', 'displayed'),
        Input(component_id='submit-button', component_property='n_clicks')
    )
def display_confirm(n_clicks):
    print(n_clicks)
    if n_clicks:
        return True
    return False

def getDataGeneral():
    db = Conexion()
    cnx = db.mysqlConnect()
    r1=db.prepare("SELECT * FROM settings WHERE 1",cnx)
    #print(r1)
    dat = {}
    if r1:
        dat = r1[0]
    db.ejecutar()
    db.mysqlClose() 
    return dat

style_field = {
    "textAlign":"center",
    "fontSize": 24
}

def ShowFormConfigGral():
    d = getDataGeneral()
    periodo_graph = 0
    longitud_graph = 0
    interval = '5m'

    if len(d) > 0:
        periodo_graph = d['periodo_graph']
        longitud_graph = d['longitud_graph']
        interval = d['interval_klines']

    return [
            html.Div([
                html.H3("General"),
                dbc.Form([
                    dbc.Label("Periodo Graph"),
                    dcc.Input(id='periodograph', type='number', value=periodo_graph, className="form-control" , style=style_field),
                    dbc.Label("Longitud Graph"),
                    dcc.Input(id='longitudgraph', type='number', value=longitud_graph, className="form-control", style=style_field),
                    dbc.Label("Interval"),
                    dcc.Input(id='interval', type='text', value=interval, className="form-control", style=style_field),
                    html.Hr(style={"border":"1px solid white", "color":"white"}),
                    dbc.Button("Update", id="submit-button", color="primary"),
                ]),
                html.Br(),
                html.Div(id='output-settings'),
                html.Div(id='output-symbols'),
                dcc.ConfirmDialog(
                    id="confirm-update",
                    message="¿Está seguro de guardar los cambios?"
                ),
                dcc.ConfirmDialog(
                    id="confirm-update-symbols",
                    message="¿Está seguro de guardar los cambios para este Par?"
                )
            ], style={
                "textAling":"left"
            })
        ]