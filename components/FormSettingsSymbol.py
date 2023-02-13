import dash
from dash import html, dcc, callback, callback_context
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import pandas as pd
import config
import datetime

from helpers.functions import *
from helpers.dbconnect import *


def get_fields_text():
    fields = [  "id","symbol","decimals","profit","trend","momentum",
                "idsma-1","idsma-2","idsma-3",
                "psma-1","psma-2","psma-3",
                "csma-1","csma-2","csma-3",
                "dsma-1","dsma-2","dsma-3",
                "idema-1","idema-2","idema-3",
                "pema-1","pema-2","pema-3",
                "cema-1","cema-2","cema-3",
                "dema-1","dema-2","dema-3",
                "prsi","crsi","drsi","oversma","lowsma"
            ]
    return fields

text_fields = get_fields_text()

@callback(
        Output(component_id='output-symbols', component_property='children'),
        Input('confirm-update-symbols', 'submit_n_clicks'),
        [
            [State(component_id="frm-{}".format(field), component_property= "value") for field in text_fields]
        ]
    )
def update_output(*args):
    trigger = callback_context.triggered[0] 
    _ , d = args

    btn_id = trigger["prop_id"].split(".")[0]
    if btn_id:
        try:
            db = Conexion()
            cnx = db.mysqlConnect()

            sql = "UPDATE settingsymbols SET symbols='{}', decimals={}, porcent_profit={}, periodo_trend={}, periodo_momentum={}, period_rsi={}, color_rsi='{}', decimal_rsi={}, porcent_over_sma={}, porcent_low_sma={} WHERE id = {} ".format(d[1],d[2],d[3],d[4],d[5],d[30],d[31],d[32],d[33],d[34],d[0])
            r1=db.prepare(sql,cnx)
            if not r1:
                raise Exception("fail update generak settings!")
            
            #update smas
            if(d[6] != 0):
                sql = "UPDATE config_smas SET periods={}, colors='{}', decimals={} WHERE id = {} ".format(d[9],d[12],d[15],d[6])
                r2=db.prepare(sql,cnx)
                if not r2:
                    raise Exception("fail update generak settings!")

            if(d[7] != 0):
                sql = "UPDATE config_smas SET periods={}, colors='{}', decimals={} WHERE id = {} ".format(d[10],d[13],d[16],d[7])
                r3=db.prepare(sql,cnx)
                if not r3:
                    raise Exception("fail update generak settings!")

            if(d[8] != 0):
                sql = "UPDATE config_smas SET periods={}, colors='{}', decimals={} WHERE id = {} ".format(d[11],d[14],d[17],d[8])
                r4=db.prepare(sql,cnx)
                if not r4:
                    raise Exception("fail update generak settings!")

            #update emas
            if(d[18] != 0):
                sql = "UPDATE config_emas SET periods={}, colors='{}', decimals={} WHERE id = {} ".format(d[21],d[24],d[27],d[18])
                r5=db.prepare(sql,cnx)
                if not r5:
                    raise Exception("fail update generak settings!")

            if(d[19] != 0):
                sql = "UPDATE config_emas SET periods={}, colors='{}', decimals={} WHERE id = {} ".format(d[22],d[25],d[28],d[19])
                r6=db.prepare(sql,cnx)
                if not r6:
                    raise Exception("fail update generak settings!")

            if(d[20] != 0):
                sql = "UPDATE config_emas SET periods={}, colors='{}', decimals={} WHERE id = {} ".format(d[23],d[26],d[29],d[20])
                r7=db.prepare(sql,cnx)
                if not r7:
                    raise Exception("fail update generak settings!")

            db.ejecutar()
            db.mysqlClose() 
            return dbc.Alert("Datos guardados con éxito!", color="success", duration=5000)
        except Exception as e:
            return dbc.Alert(e, color="danger", duration=5000)


@callback(
        Output('confirm-update-symbols', 'displayed'),
        Input(component_id='submit-button-symbols', component_property='n_clicks')
    )
def display_confirm(n_clicks):
    print(n_clicks)
    if n_clicks:
        return True
    return False

def getDataGeneral():
    db = Conexion()
    cnx = db.mysqlConnect()
    r1=db.prepare("SELECT * FROM settingsymbols WHERE 1", cnx)
    print(r1)
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

def ShowFormSettingSymbol():
    return [
            html.Div([
                dbc.Form([
                    dbc.Row([
                        dbc.Col([
                            html.Hr(),
                            dcc.Input(id='frm-id', type='hidden', value=""),
                        ])
                    ]),
                    dbc.Row([
                        dbc.Col([
                            dbc.Label("Symbol"),
                            dcc.Input(id='frm-symbol', type='text', value="", className="form-control" , style=style_field),
                        ]),
                        dbc.Col([
                            dbc.Label("Decimal Price"),
                            dcc.Input(id='frm-decimals', type='number', value="", className="form-control" , style=style_field),
                        ]),
                        dbc.Col([
                            dbc.Label("% Profit"),
                            dcc.Input(id='frm-profit', type='number', value="", className="form-control" , style=style_field),
                        ]),
                        dbc.Col([
                            dbc.Label("Perido Trend"),
                            dcc.Input(id='frm-trend', type='number', value="", className="form-control" , style=style_field),
                        ]),
                        dbc.Col([
                            dbc.Label("Period Momentum"),
                            dcc.Input(id='frm-momentum', type='number', value="", className="form-control" , style=style_field),
                        ]),
                    ]),
                    dbc.Row([
                        dbc.Col([
                            html.Hr()
                        ])
                    ]),
                    dbc.Row([    
                        dbc.Col([
                            dbc.Row([
                                dbc.Col([
                                    dcc.Input(id='frm-idsma-1', type='hidden', value=""),
                                    dcc.Input(id='frm-idsma-2', type='hidden', value=""),
                                    dcc.Input(id='frm-idsma-3', type='hidden', value=""),
                                    dbc.Label("SMAS"),
                                    html.Div([
                                        dbc.Label("Periods"),
                                        dbc.Row([
                                            dbc.Col([
                                                dcc.Input(id='frm-psma-1', type='text', value="", className="form-control" , style=style_field),
                                            ]),
                                            dbc.Col([
                                                dcc.Input(id='frm-psma-2', type='text', value="", className="form-control" , style=style_field),
                                            ]),
                                            dbc.Col([
                                                dcc.Input(id='frm-psma-3', type='text', value="", className="form-control" , style=style_field),
                                            ])
                                        ]),    
                                        dbc.Label("Colors"),
                                        dbc.Row([
                                            dbc.Col([
                                                dcc.Input(id='frm-csma-1', type='text', value="", className="form-control" , style=style_field),
                                            ]),
                                            dbc.Col([
                                                dcc.Input(id='frm-csma-2', type='text', value="", className="form-control" , style=style_field),
                                            ]),
                                            dbc.Col([
                                                dcc.Input(id='frm-csma-3', type='text', value="", className="form-control" , style=style_field),
                                            ])
                                        ]),   
                                        dbc.Label("Decimals"),
                                        dbc.Row([
                                            dbc.Col([
                                                dcc.Input(id='frm-dsma-1', type='text', value="", className="form-control" , style=style_field),
                                            ]),
                                            dbc.Col([
                                                dcc.Input(id='frm-dsma-2', type='text', value="", className="form-control" , style=style_field),
                                            ]),
                                            dbc.Col([
                                                dcc.Input(id='frm-dsma-3', type='text', value="", className="form-control" , style=style_field),
                                            ])
                                        ]),     
                                    ])
                                ]),
                                dbc.Col([
                                    dcc.Input(id='frm-idema-1', type='hidden', value=""),
                                    dcc.Input(id='frm-idema-2', type='hidden', value=""),
                                    dcc.Input(id='frm-idema-3', type='hidden', value=""),
                                    dbc.Label("EMAS"),
                                    html.Div([
                                        dbc.Label("Periods"),
                                        dbc.Row([
                                            dbc.Col([
                                                dcc.Input(id='frm-pema-1', type='text', value="", className="form-control" , style=style_field),
                                            ]),
                                            dbc.Col([
                                                dcc.Input(id='frm-pema-2', type='text', value="", className="form-control" , style=style_field),
                                            ]),
                                            dbc.Col([
                                                dcc.Input(id='frm-pema-3', type='text', value="", className="form-control" , style=style_field),
                                            ])
                                        ]),    
                                        dbc.Label("Colors"),
                                        dbc.Row([
                                            dbc.Col([
                                                dcc.Input(id='frm-cema-1', type='text', value="", className="form-control" , style=style_field),
                                            ]),
                                            dbc.Col([
                                                dcc.Input(id='frm-cema-2', type='text', value="", className="form-control" , style=style_field),
                                            ]),
                                            dbc.Col([
                                                dcc.Input(id='frm-cema-3', type='text', value="", className="form-control" , style=style_field),
                                            ])
                                        ]),   
                                        dbc.Label("Decimals"),
                                        dbc.Row([
                                            dbc.Col([
                                                dcc.Input(id='frm-dema-1', type='text', value="", className="form-control" , style=style_field),
                                            ]),
                                            dbc.Col([
                                                dcc.Input(id='frm-dema-2', type='text', value="", className="form-control" , style=style_field),
                                            ]),
                                            dbc.Col([
                                                dcc.Input(id='frm-dema-3', type='text', value="", className="form-control" , style=style_field),
                                            ])
                                        ]),     
                                    ])
                                ]),
                                dbc.Col([
                                    dbc.Label("RSI"),
                                    html.Div([
                                        dbc.Label("Period"),
                                        dbc.Row([
                                            dbc.Col([
                                                dcc.Input(id='frm-prsi', type='text', value="", className="form-control" , style=style_field),
                                            ]),
                                        ]),    
                                        dbc.Label("Color"),
                                        dbc.Row([
                                            dbc.Col([
                                                dcc.Input(id='frm-crsi', type='text', value="", className="form-control" , style=style_field),
                                            ]),
                                        ]),   
                                        dbc.Label("Decimal"),
                                        dbc.Row([
                                            dbc.Col([
                                                dcc.Input(id='frm-drsi', type='text', value="", className="form-control" , style=style_field),
                                            ])
                                        ]),     
                                    ])
                                ]),
                            ]), 
                        ]),
                    ]),    
                    dbc.Row([
                        dbc.Col([
                            html.Hr()
                        ])
                    ]),
                    dbc.Row([
                        dbc.Col([
                            dbc.Label("Porcent Over Sma"),
                            dcc.Input(id='frm-oversma', type='number', value="", className="form-control" , style=style_field),
                        ]),
                        dbc.Col([
                            dbc.Label("Porcent Low Sma"),
                            dcc.Input(id='frm-lowsma', type='number', value="", className="form-control" , style=style_field),
                        ]),
                        dbc.Col([
                            html.A(dbc.Button("Update", id="submit-button-symbols", color="primary"), href='/settings')
                        ])
                    ])
                ]),
                html.Br(),
                dcc.ConfirmDialog(
                    id="confirm-update",
                    message="¿Está seguro de guardar los cambios?"
                )
            ], style={
                "textAling":"left"
            })
        ]