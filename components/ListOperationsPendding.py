import pandas as pd
from dash import html, dash_table
from collections import OrderedDict
import config
from helpers.dbconnect import *

style_title_op = {
    "backgroundColor":'yellow',
    "color":"black",
}

data = OrderedDict([("Data", ["Sin Operaciones Pendientes"])])
df_sin_info = pd.DataFrame(data)

def ListOperationsPendding():
    db = Conexion()
    cnx = db.mysqlConnect()
    sql = "SELECT orderId,symbol,open,usdt_open,quantity,date_time_open FROM spot_trading_open WHERE status = '{}' AND symbol = '{}'".format('O',config.TRADESYMBOL)
    r1=db.prepare(sql,cnx)
    if r1:
        df = pd.DataFrame(r1)
        #df.drop(['id_entry_point'], axis = 'columns', inplace=True)
        # df = df[['orderId','symbol','type','side','price','origQty','time']]
        # df['price'] = df['price'].apply(lambda x: '{:.2f}'.format(float(x)))
        # df.time = pd.to_datetime(df.time, unit='ms').dt.strftime("%Y-%m-%d %H:%M:%S")
        # df = df.rename(columns={'price':'Precio','origQty':'Cantidad','time':'Fecha','symbol':'Simbolo','type':'Tipo','side':'Accion'})
        table_layout = dash_table.DataTable(
                                    df.to_dict('records'), 
                                    [{"name": i, "id": i} for i in df.columns],
                                    style_cell_conditional=[
                                        {'if': {'column_id': 'orderId'},'textAlign': 'center'},
                                        {'if': {'column_id': 'Simbolo'},'textAlign': 'center'},
                                        {'if': {'column_id': 'Tipo'},'textAlign': 'center'},
                                        {'if': {'column_id': 'Accion'},'textAlign': 'center'},
                                        {'if': {'column_id': 'Fecha'},'textAlign': 'center'},
                                    ],
                                    style_header={
                                        'backgroundColor': 'rgb(30, 30, 30)',
                                        'color': 'white'
                                    },
                                    style_data={
                                        'backgroundColor': 'rgb(50, 50, 50)',
                                        'color': 'white'
                                    })
    else:
        table_layout = dash_table.DataTable(
            data=df_sin_info.to_dict('records'),
            columns=[{'id': c, 'name': c} for c in df_sin_info.columns],
            style_cell_conditional=[{'if': {'column_id': 'Data'},'textAlign': 'left'},],
            style_header={'backgroundColor': 'rgb(30, 30, 30)','color': 'white'},
            style_data={'backgroundColor': 'rgb(50, 50, 50)','color': 'white'}
        )

    return [html.Div(
                id='list_operations', 
                children=[
                    html.Div(   id='title-operation_pendding',
                                children=[
                                    html.Label("Operaciones Pendientes"),
                                ],
                                style=style_title_op),
                    html.Div(   table_layout,style={'height':"100%"})
                ],
                style={
                    "marginTop":20,
                }
        )]