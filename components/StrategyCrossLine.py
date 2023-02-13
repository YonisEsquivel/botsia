from dash import html
import pandas as pd
import config
import datetime

import dash_bootstrap_components as dbc
from helpers.functions import *
from helpers.dbconnect import *

box_line = {
    "width":"100%",
    "height":50,
    "textAlign":"center",
    "display": "flex",
    "alignItems": "center",
    "justifyContent": "space-around",
    "padding":20
}

def DataSmas(klines_df, periodos, decimals):
    sma_local = []
    for i in range (0,len(periodos)):
        klines_short = klines_df.tail(periodos[i])
        sma_average = klines_short['close'].rolling(window=periodos[i]).mean()
        sma_local.append({str(periodos[i]) : float(decimals.format(sma_average.tail(1).values[0]))})
    return sma_local

def DataEmas(klines_df, periodos, decimals):
    ema_local = []
    for i in range (0,len(periodos)):
        klines_short = klines_df.tail(periodos[i])
        closes = klines_short['close'].astype(float).tolist()
        last_ema = calculate_ema_average(closes, periodos[i])
        ema_local.append({str(periodos[i]) : float(decimals.format(last_ema))})
    return ema_local


def StrategyBuy(klines_df, price, config_smas, config_emas, amount_order, decimals_price, porcent_low_sma):
    db = Conexion()
    cnx = db.mysqlConnect()

    decimals_smas = config_smas[0]['decimals']
    periodos_smas = config_smas[1]['periodos']
    
    decimals_emas = config_emas[0]['decimals']
    periodos_emas = config_emas[1]['periodos']
    
    smas = DataSmas(klines_df, periodos_smas, decimals_smas)
    emas = DataEmas(klines_df, periodos_emas, decimals_emas)
    
    porc_low_sma = smas[0]['15'] + (smas[0]['15'] * porcent_low_sma) 
    strategry_text = "WHITE " + str(emas[0]['14']) + " > GREEN " + str(smas[0]['15']) + " <= LOWGREEN " + str(porc_low_sma)
    print(strategry_text)

    if((emas[0]['14'] > smas[0]['15'] and emas[0]['14'] <= porc_low_sma) and  (emas[0]['14'] < smas[1]['25']) and (emas[0]['14'] < smas[2]['50'])):
    #if True:    
        sql = "SELECT * FROM spot_entry_points WHERE status = '{}' AND action = '{}' AND symbol = '{}'".format('O','BUY',config.TRADESYMBOL)
        r1=db.prepare(sql,cnx)
        if not r1:
            print("success not exists entrypoint")
            fecha_actual = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            sql = "INSERT INTO spot_entry_points (symbol, price, emas, smas, action, strategy, porcent_low_over_sma, date_time, status) VALUES ('{}',{},'{}','{}','BUY','{}','{}','{}','{}')".format(config.TRADESYMBOL,price['price'], json.dumps(emas), json.dumps(smas), strategry_text, porcent_low_sma,fecha_actual, 'O')
            r2=db.prepare(sql,cnx)
            if r2:
                print("success insert entrypoint buy")
                usdt_open = amount_order
                quantity = round(amount_order / float(price['price']),5)
                sql = "INSERT INTO spot_trading_open (id_entry_point,symbol,open,usdt_open,quantity,date_time_open) VALUES ({},'{}',{},{},{},'{}')".format(r2['lastID'], config.TRADESYMBOL,price['price'],usdt_open, quantity, fecha_actual)
                r3=db.prepare(sql,cnx)
                if r3:
                    print("success insert trading open")
                else:
                    print("fail insert trading open")
            else:
                print("fail insert entrypoint buy")
        else:
            print("fail exists entrypoint")
    else:
        print("No se cumple la estrategia para compra")


    if((emas[0]['14'] >= porc_low_sma and emas[0]['14'] < smas[0]['15'])):
        color1 = "green"
    else:
        color1 = "red"

    if(emas[0]['14'] < smas[1]['25']):
        color2 = "green"
    else:
        color2 = "red"

    if(emas[0]['14'] < smas[2]['50']):
        color3 = "green"
    else:
        color3 = "red"
    
    db.ejecutar()
    db.mysqlClose() 

    return  [
        dbc.Col(html.Div(id="column4-left", children= [
            html.Div(id="line_white", children=str(emas[0]['14']),style=box_line),
            html.Div(id="line_equal", children=">=",style=box_line),
            html.Div(id="line_green", children=str(smas[0]['15']),style=box_line)
        ], style={
            "padding":5,
            "backgroundColor": color1,
            "color": "white"
        }), md=4),
        dbc.Col(html.Div(id="column4-left", children= [
            html.Div(id="line_white", children=str(emas[0]['14']),style=box_line),
            html.Div(id="line_menor", children="<",style=box_line),
            html.Div(id="line_yellow", children=str(smas[1]['25']),style=box_line)
        ], style={
            "padding":5,
            "backgroundColor": color2,
            "color": "white"
        }), md=4),
        dbc.Col(html.Div(id="column4-left", children= [
            html.Div(id="line_white", children=str(emas[0]['14']),style=box_line),
            html.Div(id="line_menor", children="<",style=box_line),
            html.Div(id="line_blue", children=str(smas[2]['50']),style=box_line)
        ], style={
            "padding":5,
            "backgroundColor": color3,
            "color": "white"
        }), md=4)
    ]

def StrategySell(klines_df, price, config_smas, config_emas, porcentaje_profit, porcent_over_sma):
    db = Conexion()
    cnx = db.mysqlConnect()

    decimals_smas = config_smas[0]['decimals']
    periodos_smas = config_smas[1]['periodos']
    
    decimals_emas = config_emas[0]['decimals']
    periodos_emas = config_emas[1]['periodos']
    
    smas = DataSmas(klines_df, periodos_smas, decimals_smas)
    emas = DataEmas(klines_df, periodos_emas, decimals_emas)

    calc_porc_over_sma = smas[0]['15'] - (smas[0]['15'] * porcent_over_sma) 
    
    strategry_text = "WHITE " + str(emas[0]['14']) + " > OVERGREEN " + str(calc_porc_over_sma) + " <= GREEN " + str(smas[0]['15'])
    print(strategry_text)
    
    if(( emas[0]['14'] > calc_porc_over_sma and emas[0]['14'] <= smas[0]['15']) and  (emas[0]['14'] > smas[1]['25']) and (emas[0]['14'] > smas[2]['50'])):
    #if True:
        sql = "SELECT * FROM spot_entry_points WHERE status = '{}' AND action = '{}' AND symbol = '{}'".format('O','BUY',config.TRADESYMBOL)
        r1=db.prepare(sql,cnx)
        print(r1)
        if r1:
            print("Si hay una Operacion de Compra entonces debo vender")
            sql = "SELECT open, usdt_open, quantity FROM spot_trading_open WHERE symbol = '{}' AND close = 0 ".format(config.TRADESYMBOL)
            r2=db.prepare(sql,cnx)
            print(r2)
            if r2:
                print("ya qu existe operacion anterior consulto sus datos para verificar que el punto de venta sea mayor que el punto de compra")
                qty_profit_est = ((porcentaje_profit * float(r2[0]['open']))/100) + float(r2[0]['open'])
                validation_price = "CLOSE " + str(float(price['price'])) + " OPEN " + str(float(r2[0]['open'])) + " SHOULD > " + str(qty_profit_est)
                print(validation_price)
                print("Precio Venta: "+str(float(price['price'])) + " Precio de Compra + Profit Estimado: " + str(qty_profit_est))
                if(qty_profit_est < float(price['price'])):
                    print("en punto de venta si es mayor que la compra. procedemos a actualizar")

                    fecha_actual = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    usdt_close = (float(price['price']) * float(r2[0]['quantity']))
                    print(str(usdt_close))
                    profit = abs(round(usdt_close - float(r2[0]['usdt_open']), 5))
                    print(str(profit))

                    sql = "UPDATE spot_trading_open SET close={},usdt_close={},profit={},date_time_close='{}' WHERE symbol = '{}' AND close = 0 ".format(price['price'],usdt_close, profit, fecha_actual, config.TRADESYMBOL)
                    r3=db.prepare(sql,cnx)
                    if r3:
                        print("success trading close")
                        sql = "UPDATE spot_entry_points SET status='{}' WHERE status = '{}' AND symbol = '{}'".format('C', 'O', config.TRADESYMBOL)
                        r4=db.prepare(sql,cnx)
                        if r4:
                            print("success update entrypoint buy")
                            sql = "INSERT INTO spot_entry_points (symbol,price,emas,smas,action,strategy,porcent_low_over_sma,date_time, status) VALUES ('{}',{},'{}','{}','SELL','{}',{},'{}','{}')".format(config.TRADESYMBOL,price['price'], json.dumps(emas), json.dumps(smas),strategry_text,porcent_over_sma,fecha_actual,'C')
                            r5=db.prepare(sql,cnx)
                            if r5:
                                print("success insert entrypoint sell")
                            else:
                                print("fail insert entrypoint sell")
                        else:
                            print("fail update entrypoint buy")
                    else:
                        print("fail trading close")
                else:
                    print("El precio de compra es mayor que el posible precio de venta. hay que esperar al siguiente punto")

            else:
                print("No se pudo obtener los datos de la operacion anterior")
            
        else:
            print("No tengo Operaciones de compra. no se cumple las condicion de venta")
    else:
        print("No se cumple la estrategia para venta")

    if(( emas[0]['14'] > calc_porc_over_sma and emas[0]['14'] <= smas[0]['15'])):
        color1 = "green"
    else:
        color1 = "red"

    if(emas[0]['14'] > smas[1]['25']):
        color2 = "green"
    else:
        color2 = "red"

    if(emas[0]['14'] > smas[2]['50']):
        color3 = "green"
    else:
        color3 = "red"

    db.ejecutar()
    db.mysqlClose()

    return [
        dbc.Col(html.Div(id="column4-left", children= [
            html.Div(id="line_white", children=str(emas[0]['14']),style=box_line),
            html.Div(id="line_equal", children="><",style=box_line),
            html.Div(id="line_green", children=str(smas[0]['15']),style=box_line)
        ], style={
            "padding":5,
            "backgroundColor": color1,
            "color": "white"
        }), md=4),
        dbc.Col(html.Div(id="column4-left", children= [
            html.Div(id="line_white", children=str(emas[0]['14']),style=box_line),
            html.Div(id="line_mayor", children=">",style=box_line),
            html.Div(id="line_yellow", children=str(smas[1]['25']),style=box_line)
        ], style={
            "padding":5,
            "backgroundColor": color2,
            "color": "white"
        }), md=4),
        dbc.Col(html.Div(id="column4-left", children= [
            html.Div(id="line_white", children=str(emas[0]['14']),style=box_line),
            html.Div(id="line_mayor", children=">",style=box_line),
            html.Div(id="line_blue", children=str(smas[2]['50']),style=box_line)
        ], style={
            "padding":5,
            "backgroundColor": color3,
            "color": "white"
        }), md=4)
    ]

def StrategyLaterizando(klines_df, config_smas, config_emas):
    decimals_smas = config_smas[0]['decimals']
    periodos_smas = config_smas[1]['periodos']
    
    decimals_emas = config_emas[0]['decimals']
    periodos_emas = config_emas[1]['periodos']

    smas = DataSmas(klines_df, periodos_smas, decimals_smas)
    emas = DataEmas(klines_df, periodos_emas, decimals_emas)

    style_laterianzo = {
        "padding":5,
        "backgroundColor": "yellow",
        "color": "black"
    }
    return [
        dbc.Col(html.Div(id="column4-left", children= [
            html.Div(id="line_white", children=emas[0]['14'],style=box_line),
            html.Div(id="line_equal", children=" ",style=box_line),
            html.Div(id="line_yellow", children=smas[1]['25'],style=box_line)
        ], style=style_laterianzo), md=4),
        dbc.Col(html.Div(id="column4-left", children= [
            html.Div(id="line_white", children=emas[0]['14'],style=box_line),
            html.Div(id="line_mayor", children=" ",style=box_line),
            html.Div(id="line_green", children=smas[0]['15'],style=box_line)
        ], style=style_laterianzo), md=4),
        dbc.Col(html.Div(id="column4-left", children= [
            html.Div(id="line_white", children=emas[0]['14'],style=box_line),
            html.Div(id="line_menor", children=" ",style=box_line),
            html.Div(id="line_blue", children=smas[2]['50'],style=box_line)
        ], style=style_laterianzo), md=4)
    ]

def StrategyFailed(klines_df, config_smas, config_emas):
    decimals_smas = config_smas[0]['decimals']
    periodos_smas = config_smas[1]['periodos']
    
    decimals_emas = config_emas[0]['decimals']
    periodos_emas = config_emas[1]['periodos']

    smas = DataSmas(klines_df, periodos_smas, decimals_smas)
    emas = DataEmas(klines_df, periodos_emas, decimals_emas)

    style_laterianzo = {
        "padding":5,
        "backgroundColor": "orange",
        "color": "black"
    }
    return [
        dbc.Col(html.Div(id="column4-left", children= [
            html.Div(id="line_white", children=emas[0]['14'],style=box_line),
            html.Div(id="line_equal", children=" ",style=box_line),
            html.Div(id="line_yellow", children=smas[1]['25'],style=box_line)
        ], style=style_laterianzo), md=4),
        dbc.Col(html.Div(id="column4-left", children= [
            html.Div(id="line_white", children=emas[0]['14'],style=box_line),
            html.Div(id="line_mayor", children=" ",style=box_line),
            html.Div(id="line_green", children=smas[0]['15'],style=box_line)
        ], style=style_laterianzo), md=4),
        dbc.Col(html.Div(id="column4-left", children= [
            html.Div(id="line_white", children=emas[0]['14'],style=box_line),
            html.Div(id="line_menor", children=" ",style=box_line),
            html.Div(id="line_blue", children=smas[2]['50'],style=box_line)
        ], style=style_laterianzo), md=4)
    ]

def ShowStrategyCrossLine(
            klines_df, 
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
            porcent_over_sma
        ):
    trend_values = getTrendValues(klines_df, periodo_trend, periodo_momentum)
    diff = trend_values[0]
    _momentum = trend_values[1]
    
    strategy_layout = StrategyFailed(klines_df, config_smas, config_emas)

    if (diff > 0 and _momentum > 0):
        print("alza compra")
        #balance_asset = GetBalanceAsset(balance, 'alza')
        #if(balance_asset > amount_order):
        strategy_layout = StrategyBuy(  klines_df, 
                                        price, 
                                        config_smas, 
                                        config_emas, 
                                        amount_order, 
                                        decimals_price, 
                                        porcent_low_sma)
        #else:
        #    print("Sin saldo para la compra")

    elif (diff < 0 and _momentum < 0):
        print("baja vende")
        balance_asset = GetBalanceAsset(balance, 'baja')
        cant_base = balance_asset * float(price['price'])
        if(cant_base > amount_order):
            strategy_layout = StrategySell( klines_df, 
                                            price, 
                                            config_smas, 
                                            config_emas, 
                                            porcentaje_profit, 
                                            porcent_over_sma)
        else:
            print("Sin saldo para la venta")
    else:
        print("laterizando")
        strategy_layout = StrategyLaterizando(klines_df, config_smas, config_emas)

    return [dbc.Row(strategy_layout)]