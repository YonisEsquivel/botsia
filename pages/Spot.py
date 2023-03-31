import dash
import config
import dash_bootstrap_components as dbc
from dash import html, dcc, callback, Input, Output, State
from helpers.binance_api import BinanceApiClient
from helpers.functions import *
from helpers.dbconnect import *
from components.GraphOHLC import GraphOHLC
from components.ListSymbols import ListSymbols
from components.ListDataAsset import DatosAssetTrading
from components.ListOrdersOpen import ListOrdersOpen
from components.ListOperationsPendding import ListOperationsPendding
from components.RsiMeter import GraphRsiMeter
from components.GraphTrend import ShowGraphTrend
from components.IndicatorsActive import ShowIndicators
from components.StrategyCrossLine import ShowStrategyCrossLine

cliente = BinanceApiClient(config.BINANCE_API_KEY, config.BINANCE_SECRET_KEY, config.URL_SPOT_BINANCE)

dash.register_page(__name__)

# @callback(
#     Output('local-storage', 'data'), 
#     [Input('refresh_data_trading', 'n_intervals')], 
# )
# def get_values_store(n):
#     data = []
#     number = 2200+n
#     data.append({
#         'botsia': '{"price":'+str(number)+',"asset":"BTC","type":"buy","orderId":"123456"}'
#     })
#     print('localstorage '+ str(n))
#     return data

@callback(
            [   
                Output('candlestick_chart', 'children'), 
                Output('column-left-data', 'children'),
                Output('list-orders-open', 'children'),
                Output('list-operations-pendding', 'children'),
                Output('rsi-meter', 'children'),
                Output('graph-trend', 'children'),
                Output('indicators-active', 'children'),
                Output('strategy-cross-line', 'children')
            ],
            [Input('refresh_data_trading', 'n_intervals')],
            prevent_initial_call=True,
        )
def LoadDataTrading(n):
    #init data
    interval = '5m'
    periodo_graph = 200
    longitud_graph = 150
    amount_order = 51 # Cantidad USDT como limite para las operaciones
    porcentaje_profit = 0.1 # Porcentaje estimado por encima de ultima compra para tomar ganancia
    periodo_trend = 8 # Utilizado para obtener el numero de klines y calcular su tendencia
    periodo_momentum = 8
    porcent_low_sma = 0.002
    porcent_over_sma = 0.002
    decimals = '.2f' #'.6f' ACH
    decimals_price = '{:'+decimals+'}' #'{:.2f}' BTC
    decimals_quantity = '{:.5f}' # Para presentar la cadena de texto de la candidad de monedas compradas
    round_quantity = 7 # Para redondear los decimales tipo float en las operaciones

    config_rsi = [
        {'decimals': decimals_price}, #'{:.0f}' BTC
        {'periodo': 14},
        {'colors':'orange'},
        {'line': 'sma'}
    ]

    config_smas = [
        {'decimals': decimals_price}, #'{:.0f}' BTC
        {'periodos': [15,25,50]},
        {'colors':['lightgreen','yellow','lightblue']}
    ]

    config_emas = [
        {'decimals': decimals_price}, #'{:.0f}' BTC
        {'periodos': [14]},
        {'colors':['white']}
    ]

    #get data
    klines = cliente.get_klines_data(config.TRADESYMBOL, interval, periodo_graph)
    klines_df = get_klines_df(klines)
    info_asset = cliente.get_symbol_info(config.TRADESYMBOL)
    price = cliente.get_price_symbol(symbol=config.TRADESYMBOL)
    balance = cliente.get_balance_account()
    orders = cliente.get_open_orders(symbol=config.TRADESYMBOL)

    #create layout
    layout_graph = GraphOHLC(n, klines_df, config_smas, config_emas, periodo_graph, longitud_graph, decimals)

    layout_data_asset = DatosAssetTrading(price, decimals_price, balance, klines_df, config_smas, config_emas, config_rsi)
    layout_orders_open = ListOrdersOpen(orders)
    layout_opertions_pendding = ListOperationsPendding()

    layout_rsi = GraphRsiMeter(klines_df, config_rsi)
    layout_trend = ShowGraphTrend(klines_df, periodo_trend, periodo_momentum)
    layout_indicators = ShowIndicators(klines_df, periodo_trend, orders, amount_order, balance, price, periodo_momentum, porcentaje_profit, decimals_price)
    
    data_strategy = ShowStrategyCrossLine(klines_df, 
                                            price, 
                                            periodo_trend, 
                                            periodo_momentum, 
                                            config_smas, 
                                            config_emas, 
                                            balance, 
                                            amount_order, 
                                            decimals_price, 
                                            porcentaje_profit, 
                                            porcent_low_sma,
                                            porcent_over_sma,
                                            decimals_quantity,
                                            info_asset)
    layout_Strategy =[dbc.Row(data_strategy['layout'])]
    response_strategy = data_strategy['evaluation']
    if (len(response_strategy)> 0 ):
        print(response_strategy)
        symbol, side, quantity, price_side, id_orden_open, lastid = response_strategy
        print("quantity: " + str(quantity))
        res = cliente.create_order_limit(symbol, side, float(quantity), float(decimals_price.format(price_side)))
        print("orden ejecutada: esperemos 1 minuto...")
        print(res)
        db = Conexion()
        cnx = db.mysqlConnect()
        sql = "INSERT INTO spot_response_order (id_entry_point,id_orden_open,response) VALUES({},{},'{}')".format(lastid, id_orden_open, json.dumps(res['data']))
        db.prepare(sql,cnx)
        db.ejecutar()
        db.mysqlClose()
        time.sleep(120)
        
        
    return layout_graph, layout_data_asset, layout_orders_open, layout_opertions_pendding, layout_rsi, layout_trend, layout_indicators, layout_Strategy

def ColumnLeftLayout():
    return [
        html.Div(id="column-left-menu", children= ListSymbols()),
        html.Div(id="column-left-data")
    ]

def CandlestickChart():
    return [html.Div(id='candlestick_chart')]

def ColumnRightLayout():
    return [html.Div(id="column-right-form", children=[
            dbc.Row([
                dbc.Col(html.Div(id='graph-trend')),
            ]),
            dbc.Row([
                dbc.Col(html.Div(id='indicators-active')),
            ]),
            dbc.Row([
                dbc.Col(html.Div(id='strategy-cross-line')),
            ]),
            dbc.Row([
                dbc.Col(html.Div(id="rsi-meter")),
            ]),
        ])]

def layout():
    return  html.Div([
                dbc.Row([
                    dbc.Col(html.Div(id="column-top-left", children= ColumnLeftLayout()), md=2),
                    dbc.Col(html.Div(id="column-top-center", children= CandlestickChart()), md=8),
                    dbc.Col(html.Div(id="column-top-right", children= ColumnRightLayout()), md=2),
                ]),
                dbc.Row([
                    dbc.Col([
                            html.Div(id="list-orders-open"),
                            html.Div(id="list-operations-pendding")
                        ], md=9),
                    dbc.Col(html.Div(id="log-terminal", children= []), md=3)
                ])
            ])