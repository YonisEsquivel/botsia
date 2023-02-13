from dash import html, dcc
import config
import pandas as pd
from helpers.functions import *
from helpers.dbconnect import *

def IndicatorBuySell(klines_df, periodo_trend, amount_order, balance, price, periodo_momentum):
    trend_values = getTrendValues(klines_df, periodo_trend, periodo_momentum)
    diff = trend_values[0]
    _momentum = trend_values[1]

    if (diff > 0 and _momentum > 0):
        balance_asset = GetBalanceAsset(balance, 'alza')
        font_color = "white"
        if(balance_asset > amount_order):
            text_action = "Con Saldo Para Comprar"
            backgound_color = "Green"
        else:
            text_action = "Sin Saldo Para Comprar"
            backgound_color = "red"
    elif (diff < 0 and _momentum < 0):
        balance_asset = GetBalanceAsset(balance, 'baja')
        cant_base = balance_asset * float(price['price'])
        font_color = "white"
        if(cant_base > amount_order):
            text_action = "Con Saldo Para Vender"
            backgound_color = "Green"
        else:
            text_action = "Sin Saldo Para Vender"
            backgound_color = "red"
    else:
        text_action = "En espera de tendencia"
        backgound_color = "yellow"
        font_color = "black"

    return html.Div(id='balance_asset_indicators', 
                    children=text_action, 
                    style={ 
                        "width": "270px", 
                        "backgroundColor": backgound_color,
                        "height": 70, 
                        "color": font_color,
                        "display":"flex",
                        "alignItems": "center",
                        "justifyContent": "space-around",
                        "fontWeight":"bold"
                    })
            

def ExistLastOperation(klines_df, periodo_trend, periodo_momentum):
    trend_values = getTrendValues(klines_df, periodo_trend, periodo_momentum)
    diff = trend_values[0]
    _momentum = trend_values[1]
    
    db = Conexion()
    cnx = db.mysqlConnect()
    sql = "SELECT * FROM spot_entry_points WHERE status = '{}' AND action = '{}' AND symbol = '{}'".format('O','BUY',config.TRADESYMBOL)
    r1=db.prepare(sql,cnx)
    db.ejecutar()
    db.mysqlClose()
    text_exist_operations = "Sin reconocer operaciones"
    color="white"

    if (diff > 0 and _momentum > 0):
        if r1:
            text_exist_operations = "Existe operaciones pendientes"
            color="red"
        
        else:
            text_exist_operations = "No existe operaciones pendientes"
            color="green"

    elif (diff < 0 and _momentum < 0):
        if r1:
            text_exist_operations = "Existe operaciones pendientes"
            color="green"
        
        else:
            text_exist_operations = "No existe operaciones pendientes"
            color="red"

    return html.Div(id='exist_last_operations_indicators', 
                    children=text_exist_operations, 
                    style={ 
                        "width": "270px", 
                        "backgroundColor": color,
                        "height": 70, 
                        "color":"white",
                        "display":"flex",
                        "alignItems": "center",
                        "justifyContent": "space-around",
                        "fontWeight":"bold"
                    })

def ExistOrders(orders):
    existe_orders = len(orders)
    text_action = "Ordenes Abiertas ("+str(existe_orders)+")"
    if (existe_orders > 0):
        color = "red"
    else:
        color = "green"

    return html.Div(id='open_orders_indicators', 
                    children=text_action, 
                    style={ 
                        "width": "270px", 
                        "backgroundColor": color,
                        "height": 70, 
                        "color":"white",
                        "display":"flex",
                        "alignItems": "center",
                        "justifyContent": "space-around",
                        "fontWeight":"bold"
                    })



def ShowIndicators(klines_df, periodo_trend, orders, amount_order, balance, price, periodo_momentum):
    indicators = []

    ord = ExistOrders(orders)
    indicators.append(ord)
    
    trend = IndicatorBuySell(klines_df, periodo_trend, amount_order, balance, price, periodo_momentum)
    indicators.append(trend)

    operations = ExistLastOperation(klines_df, periodo_trend, periodo_momentum)
    indicators.append(operations)

    return indicators