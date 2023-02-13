import pandas as pd
from dash import html, dash_table
from collections import OrderedDict

style_title_op = {
    "backgroundColor":'yellow',
    "color":"black",
}

data = OrderedDict([("Data", ["Sin Ordenes abiertas"])])
df_sin_info = pd.DataFrame(data)

def ListOrdersOpen(orders):
    if len(orders) > 0:
        df = pd.DataFrame(orders)
        df.drop(['orderListId','clientOrderId','timeInForce','icebergQty','updateTime','isWorking','workingTime','selfTradePreventionMode','origQuoteOrderQty','cummulativeQuoteQty','executedQty','stopPrice'], axis = 'columns', inplace=True)
        df = df[['orderId','symbol','type','side','price','origQty','time']]
        df['price'] = df['price'].apply(lambda x: '{:.2f}'.format(float(x)))
        df.time = pd.to_datetime(df.time, unit='ms').dt.strftime("%Y-%m-%d %H:%M:%S")
        df = df.rename(columns={'price':'Precio','origQty':'Cantidad','time':'Fecha','symbol':'Simbolo','type':'Tipo','side':'Accion'})
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
                id='list_orders_open', 
                children=[
                    html.Div(   id='title-open-orders',
                                children=[
                                    html.Label("Ordenes Abiertas"),
                                ],
                                style=style_title_op),
                    html.Div(   table_layout,style={'height':100})
                ],
                style={
                    "marginTop":20,
                }
        )]