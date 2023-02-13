import dash
from dash import html, callback_context, callback
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State

from helpers.functions import *
from helpers.dbconnect import *


def get_data_settings(id=0, all=None):
    db = Conexion()
    cnx = db.mysqlConnect()
    data = []
    
    if id != 0:
        r1 = db.prepare("SELECT * FROM settingsymbols WHERE id={}".format(id), cnx)
    else:
        r1 = db.prepare("SELECT * FROM settingsymbols WHERE 1", cnx)
        if(all==None):
            return r1
    
    if r1:
        for row in r1:
            data_sma = []
            data_ema = []
            r2 = db.prepare("SELECT * FROM config_smas WHERE idsettings = {} ".format(row['id']), cnx)
            if r2:
                for row2 in r2:
                    data_sma.append(row2)
                row.update({'config_smas':data_sma})
            else:
                row.update({'config_smas':''})
            r3= db.prepare("SELECT * FROM config_emas WHERE idsettings = {} ".format(row['id']), cnx)
            if r3:
                for row3 in r3:
                    data_ema.append(row3)
                row.update({'config_emas':data_ema})
            else:
                row.update({'config_emas':''})
            data.append(row)
            
    db.ejecutar()
    db.mysqlClose()
    
    return data

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
buttons = len(get_data_settings())

def generate_table(data):

    theader_layout =  [
            html.Thead(
                html.Tr([
                    html.Th("Id"),
                    html.Th("Symbols"),
                    html.Th("Decimals"),
                    html.Th("% Profit"),
                    html.Th("% OverSma"),
                    html.Th("% LowSma"),
                    html.Th("Config SMAS"),
                    html.Th("Config EMAS"),
                    html.Th("Config RSI"),
                    html.Th("Action")
                ])
            )
        ]

    rows_layout = []

    if data:
        for row in data:
            rows = []
            rows.append(html.Td(row['id']))
            rows.append(html.Td(row['symbols']))
            rows.append(html.Td(row['decimals']))
            rows.append(html.Td(row['porcent_profit']))
            rows.append(html.Td(row['porcent_over_sma']))
            rows.append(html.Td(row['porcent_low_sma']))
            
            psmas = []
            csmas = []
            dsmas = []
            idsmas = []
            for row2 in row['config_smas']:
                psmas.append(row2['periods'])
                csmas.append(row2['colors'])
                dsmas.append(row2['decimals'])
                idsmas.append(row2['id'])

            rows.append(html.Td([
                html.Div([
                    dbc.Row([
                        dbc.Col(html.Div(children=[
                            html.Span(p, style={'color': c, "width":"100%"})
                        ], style={"textAlign":"center", "marginTop":5 ,"border": "1px solid {}".format(c)}), md=4),
                        dbc.Col(html.Div(children=[html.Span(d, style={'color': c, "width":"100%"})], style={"textAlign":"center", "marginTop":5 ,"border": "1px solid {}".format(c)}), md=4),
                        dbc.Col(html.Div(children=[html.Span(c[0], style={'color': c, "width":"100%"})], style={"backgroundColor":c,"textAlign":"center", "marginTop":5 ,"border": "1px solid {}".format(c)}), md=4),
                    ])]
                ) for p, d, c in zip(psmas, dsmas, csmas)
            ]))


            pemas = []
            cemas = []
            demas = []
            idemas = []
            for row3 in row['config_emas']:
                pemas.append(row3['periods'])
                cemas.append(row3['colors'])
                demas.append(row3['decimals'])
                idemas.append(row3['id'])

            rows.append(html.Td([
                html.Div([
                    dbc.Row([
                        dbc.Col(html.Div(children=[html.Span(p, style={'color': c, "width":"100%"})], style={"textAlign":"center", "marginTop":5 ,"border": "1px solid {}".format(c)}), md=4),
                        dbc.Col(html.Div(children=[html.Span(d, style={'color': c, "width":"100%"})], style={"textAlign":"center", "marginTop":5 ,"border": "1px solid {}".format(c)}), md=4),
                        dbc.Col(html.Div(children=[html.Span(c[0], style={'color': c, "width":"100%"})], style={"backgroundColor":c,"textAlign":"center", "marginTop":5 ,"border": "1px solid {}".format(c)}), md=4),
                    ])]
                ) for p, d, c in zip(pemas, demas, cemas)
            ]))

            rows.append(html.Td([
                html.Div([
                    dbc.Row([
                        dbc.Col(html.Div(children=[html.Span(row['period_rsi'], style={'color': row['color_rsi'], "width":"100%"})], style={"textAlign":"center", "marginTop":5 ,"border": "1px solid {}".format(row['color_rsi'])}), md=4),
                        dbc.Col(html.Div(children=[html.Span(row['decimal_rsi'], style={'color': row['color_rsi'], "width":"100%"})], style={"textAlign":"center", "marginTop":5 ,"border": "1px solid {}".format(row['color_rsi'])}), md=4),
                        dbc.Col(html.Div(children=[html.Span(row['color_rsi'][0], style={'color': row['color_rsi'], "width":"100%"})], style={"backgroundColor":row['color_rsi'],"textAlign":"center", "marginTop":5 ,"border": "1px solid {}".format(row['color_rsi'])}), md=4),
                    ])]
                )
            ]))

            rows.append(html.Td([
                dbc.Button("C", id="btn-sea-{}".format(row['id']), className="btn-search", color="success", style={"marginLeft":5}),
                dbc.Button("X", id="btn-del-{}".format(row['id']), className="btn-delete", color="danger", style={"marginLeft":5})
            ], style={"textAlign":"center"}))

            rows_layout.append(html.Tr(rows))

    table_body = [html.Tbody(rows_layout)]    

    return dbc.Table(
                theader_layout + table_body,
                bordered=True,
                dark=True,
                hover=True,
                responsive=True,
                striped=True
        )


def new_func(buttons):
    print(buttons)
    return buttons

@callback(
    [Output("frm-"+field, "value") for field in text_fields],
    [Input("btn-sea-"+str(j+1), "n_clicks") for j in range(new_func(buttons))],
)
def on_button_click(*args):
    trigger = callback_context.triggered[0] 
    print(trigger)
    btn_id = trigger["prop_id"].split(".")[0]
    data_fields = {field: 0 for field in text_fields}

    if(len(btn_id) > 0):
        id = btn_id.split("-")[2]
        print(id)
        db_data = get_data_settings(id,'all')[0]
        print(db_data)
        for data in db_data:
            if type(db_data[data]) != list:
                if(data=='id'): data_fields['id'] = db_data[data]
                if(data=='symbols'): data_fields['symbol'] = db_data[data]
                if(data=='decimals'): data_fields['decimals'] = db_data[data]
                if(data=='porcent_profit'): data_fields['profit'] = db_data[data]
                if(data=='periodo_trend'): data_fields['trend'] = db_data[data]
                if(data=='periodo_momentum'): data_fields['momentum'] = db_data[data]
                if(data=='period_rsi'): data_fields['prsi'] = db_data[data]
                if(data=='color_rsi'): data_fields['crsi'] = db_data[data]
                if(data=='decimal_rsi'): data_fields['drsi'] = db_data[data]
                if(data=='porcent_over_sma'): data_fields['oversma'] = db_data[data]
                if(data=='porcent_low_sma'): data_fields['lowsma'] = db_data[data]

            else:
                if(data == 'config_smas'):
                    for i in range(0,len(db_data[data])):
                        print(db_data[data][i])
                        print('psma-{}'.format(i+1))
                        data_fields['idsma-{}'.format(i+1)] = db_data[data][i]['id']
                        data_fields['psma-{}'.format(i+1)] = db_data[data][i]['periods']
                        data_fields['csma-{}'.format(i+1)] = db_data[data][i]['colors']
                        data_fields['dsma-{}'.format(i+1)] = db_data[data][i]['decimals']
                
                if(data == 'config_emas'):
                    for i in range(0,len(db_data[data])):
                        print(db_data[data][i])
                        print('pema-{}'.format(i+1))
                        data_fields['idema-{}'.format(i+1)] = db_data[data][i]['id']
                        data_fields['pema-{}'.format(i+1)] = db_data[data][i]['periods']
                        data_fields['cema-{}'.format(i+1)] = db_data[data][i]['colors']
                        data_fields['dema-{}'.format(i+1)] = db_data[data][i]['decimals']

    return list(data_fields.values())

def ShowListSymbols():
    data = get_data_settings(all=True)
    tabla_layout = generate_table(data)
    return html.Div(id="vista tabla", children=[html.Div(id="outputData"),tabla_layout])
