import dash
import config
import dash_bootstrap_components as dbc
from dash import html, dcc, callback, Input, Output, State
from helpers.binance_api import BinanceApiClient
from helpers.functions import *
from components.GraphOHLC import GraphOHLC
from components.ListSymbols import ListSymbols
from components.ListDataAsset import DatosAssetTrading
from components.ListOrdersOpen import ListOrdersOpen
from components.RsiMeter import GraphRsiMeter
from components.GraphTrend import ShowGraphTrend
from components.IndicatorsActive import ShowIndicators
from components.StrategyCrossLine import ShowStrategyCrossLine

cliente = BinanceApiClient(config.BINANCE_API_KEY, config.BINANCE_SECRET_KEY, config.URL_SPOT_BINANCE)

dash.register_page(__name__)

style_box_bottom = {
    "display": "flex",
    "alignItems": "center",
    "justifyContent": "space-around"
}

@callback(
            [   
                Output('candlestick_chart', 'children'), 
                Output('column-left-data', 'children'),
                Output('list-orders-open', 'children'),
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
    amount_order = 10.20 # Cantidad USDT como limite para las operaciones
    porcentaje_profit = 0.1 #Porcentaje estimado por encima de ultima compra para tomar ganancia
    periodo_trend = 8 # Utilizado para obtener el numero de klines y calcular su tendencia
    periodo_momentum = 8
    porcent_low_sma = 0.002
    porcent_over_sma = 0.002

    config_rsi = [
        {'decimals': '{:.0f}'},
        {'periodo': 14},
        {'colors':'orange'},
        {'line': 'sma'}
    ]

    config_smas = [
        {'decimals': '{:.0f}'},
        {'periodos': [15,25,50]},
        {'colors':['lightgreen','yellow','lightblue']}
    ]

    config_emas = [
        {'decimals': '{:.0f}'},
        {'periodos': [14]},
        {'colors':['white']}
    ]

    decimals_price = '{:.2f}'
    
    #get data
    klines = cliente.get_klines_data(config.TRADESYMBOL, interval, periodo_graph)
    klines_df = get_klines_df(klines)

    price = cliente.get_price_symbol(symbol=config.TRADESYMBOL)
    balance = cliente.get_balance_account()
    orders = cliente.get_open_orders(symbol=config.TRADESYMBOL)

    #create layout
    layout_graph = GraphOHLC(n, klines_df, config_smas, config_emas, periodo_graph, longitud_graph)

    layout_data_asset = DatosAssetTrading(price, decimals_price, balance, klines_df, config_smas, config_emas, config_rsi)
    layout_orders_open = ListOrdersOpen(orders)
    layout_rsi = GraphRsiMeter(klines_df, config_rsi)
    layout_trend = ShowGraphTrend(klines_df, periodo_trend, periodo_momentum)
    layout_indicators = ShowIndicators(klines_df, periodo_trend, orders, amount_order, balance, price, periodo_momentum)
    
    layout_Strategy = ShowStrategyCrossLine(klines_df, 
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
                                            porcent_over_sma)

    return layout_graph, layout_data_asset, layout_orders_open, layout_rsi, layout_trend, layout_indicators, layout_Strategy


def CandlestickChart():
    return [html.Div(id='candlestick_chart')]

def ColumnLeftLayout():
    return [
        html.Div(id="column-left-menu", children= ListSymbols()),
        html.Div(id="column-left-data")
    ]

def ColumnRightLayout():
    return [html.Div(id="column-right-form")]

def ColumnRsiMeter():
    return [html.Div(id="rsi-meter")]

def ColumnGraphTrend():
    return [html.Div(id='graph-trend')]

def ColumnIndicators():
    return [html.Div(id='indicators-active')]

def ColumnStrategyCross():
    return [html.Div(id='strategy-cross-line')]

def layout():
    return  html.Div([
                dbc.Row([
                    dbc.Col(html.Div(id="column-top-left", children= ColumnLeftLayout()), md=2),
                    dbc.Col(html.Div(id="column-top-center", children= CandlestickChart()), md=8),
                    dbc.Col(html.Div(id="column-top-right", children= ColumnRightLayout()), md=2),
                ]),
                dbc.Row(dbc.Col(html.Div(id="list-orders-open"))),
                dbc.Row([
                    dbc.Col(html.Div(id="column1-bottom", children= ColumnRsiMeter()), md=3),
                    dbc.Col(html.Div(id="column2-bottom", children= ColumnGraphTrend()), md=3),
                    dbc.Col(html.Div(id="column3-bottom", children= ColumnIndicators(), style={"paddingLeft": 10, "paddingRight": 10}), md=3, style=style_box_bottom),
                    dbc.Col(html.Div(id="column4-bottom", children= ColumnStrategyCross()), md=3, style=style_box_bottom),
                ])
                
            ])