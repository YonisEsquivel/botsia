from dash import html
import pandas as pd
import config
from datetime import datetime
import asyncio

import dash_bootstrap_components as dbc
from helpers.functions import *
from helpers.dbconnect import *

box_line = {
    "width":"100%",
    "height":20,
    "textAlign":"center",
    "display": "flex",
    "alignItems": "center",
    "justifyContent": "space-around",
    "padding":15
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


def def_amount_trade(info, price, decimals_quantity, amount = 10):
    # amount = 10 usdt que van a utilizar para hacer las operaciones
    cantidad = float(amount / price) 
    min_quantity = info['lot_size_min_quantity']
    max_quantity = info['lot_size_max_quantity']
    step_size = info['lot_size_step_size'] 
    min_notional = info['min_notional']

    if cantidad < min_quantity: 
        print('Cantidad demasiado pequeña') 
        return 0
    if cantidad > max_quantity:
        print('Cantidad demasiado grande')
        return 0
    
    cantidad = round_step_size(cantidad, step_size) 
    cantidad = float(decimals_quantity.format(cantidad))
    my_notional = price * float(cantidad)
    if my_notional < min_notional:
        print('Valor del trade ['+str(my_notional)+'] es demasiado PEQUEÑO.')
        print('Esto significa que la cantidad que estamos enviando al pedido aún es demasiado pequeña')
        print('La configuracion indica mayor de ['+str(min_notional)+']')
        return 0

    return cantidad

def StrategyBuy(klines_df, price, config_smas, config_emas, amount_order, decimals_price, porcent_low_sma, decimals_quantity, info_asset):
    db = Conexion()
    cnx = db.mysqlConnect()

    decimals_smas = config_smas[0]['decimals']
    periodos_smas = config_smas[1]['periodos']
    
    decimals_emas = config_emas[0]['decimals']
    periodos_emas = config_emas[1]['periodos']
    
    smas = DataSmas(klines_df, periodos_smas, decimals_smas)
    emas = DataEmas(klines_df, periodos_emas, decimals_emas)
    
    porc_low_sma = smas[0]['15'] + (smas[0]['15'] * porcent_low_sma) 
    strategry_text = "EMA_WHITE " + str(emas[0]['14']) + " > SMA_GREEN " + str(smas[0]['15']) + " <= LOWGREEN " + str(porc_low_sma)
    #print(strategry_text)
    usdt_open = amount_order

    quantity = def_amount_trade(info_asset, float(price['price']), decimals_quantity, amount_order)
    usd_open_text = '{:.4f}'.format((quantity * float(price['price'])))
    fecha_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    evaluation_strategy = []
    if((emas[0]['14'] > smas[0]['15'] and emas[0]['14'] <= porc_low_sma) and  (emas[0]['14'] < smas[1]['25']) and (emas[0]['14'] < smas[2]['50'])):
    #if True:    
        strategy_smas = " AND EMA_WHITE " + str(emas[0]['14']) + " < SMA_YELLOW "+ str(smas[1]['25']) + "AND EMA_WHITE " + str(emas[0]['14']) + " < SMA_YELLOW "+ str(smas[2]['50'])
        sql = "SELECT * FROM spot_entry_points WHERE status = '{}' AND action = '{}' AND symbol = '{}'".format('O','BUY',config.TRADESYMBOL)
        r1=db.prepare(sql,cnx)
        if not r1:
            print("success not exists entrypoint")
            sql = "INSERT INTO spot_entry_points (symbol, price, emas, smas, action, strategy, porcent_low_over_sma, date_time, status) VALUES ('{}','{}','{}','{}','BUY','{}','{}','{}','{}')".format(config.TRADESYMBOL,price['price'], json.dumps(emas), json.dumps(smas), strategry_text + strategy_smas, porcent_low_sma,fecha_actual, 'O')
            r2=db.prepare(sql,cnx)
            if r2:
                #asyncio.run(SendNotificationTelegram("Puntos de Entrada con: "+strategry_text + strategy_smas))
                print("success insert entrypoint buy")
                
                sql = "INSERT INTO spot_trading_open (id_entry_point_open,symbol,open,usdt_open,quantity,date_time_open) VALUES ({},'{}','{}',{},{},'{}')".format(r2['lastID'], config.TRADESYMBOL,price['price'],usd_open_text, quantity, fecha_actual)
                r3=db.prepare(sql,cnx)
                if r3:
                    evaluation_strategy = [config.TRADESYMBOL, 'BUY', quantity, float(price['price']), r3['lastID'], r2['lastID']]
                    txt = "<b><u>Compra abierta "+ config.TRADESYMBOL+":</u></b> \n<i>Precio:</i> "+ str(price['price'] + " \n<i>Monto:</i> "+str(usd_open_text)+" \n<i>Cantidad:</i> " + str(quantity))
                    asyncio.run(SendNotificationTelegram(txt))
                    print("success insert trading open")
                else:
                    print("fail insert trading open")
            else:
                print("fail insert entrypoint buy")
        else:
            print("fail exists entrypoint")
    else:
        print("No se cumple la estrategia para compra "+ fecha_actual)
        #pass

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

    return  {   "layout" :[
                    html.Div(className="line-strategy", children= [
                        html.Div(id="line_white", children=str(emas[0]['14']),style=box_line),
                        html.Div(id="line_equal", children=">=",style=box_line),
                        html.Div(id="line_green", children=str(smas[0]['15']),style=box_line)
                    ], style={
                        "backgroundColor": color1,
                        "color": "white"
                    }),
                    html.Div(className="line-strategy", children= [
                        html.Div(id="line_white", children=str(emas[0]['14']),style=box_line),
                        html.Div(id="line_menor", children="<",style=box_line),
                        html.Div(id="line_yellow", children=str(smas[1]['25']),style=box_line)
                    ], style={
                        "backgroundColor": color2,
                        "color": "white"
                    }),
                    html.Div(className="line-strategy", children= [
                        html.Div(id="line_white", children=str(emas[0]['14']),style=box_line),
                        html.Div(id="line_menor", children="<",style=box_line),
                        html.Div(id="line_blue", children=str(smas[2]['50']),style=box_line)
                    ], style={
                        "backgroundColor": color3,
                        "color": "white"
                    })
                ],
                "evaluation" : evaluation_strategy
            }

def StrategySell(klines_df, price, config_smas, config_emas, amount_order, porcentaje_profit, porcent_over_sma):
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
    #print(strategry_text)
    fecha_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    evaluation_strategy = []

    if(( emas[0]['14'] > calc_porc_over_sma and emas[0]['14'] <= smas[0]['15']) and  (emas[0]['14'] > smas[1]['25']) and (emas[0]['14'] > smas[2]['50'])):
    #if True:
        strategy_smas = " AND EMA_WHITE " + str(emas[0]['14']) + " > SMA_YELLOW "+ str(smas[1]['25']) + "AND EMA_WHITE " + str(emas[0]['14']) + " > SMA_BLUE "+ str(smas[2]['50'])
        sql = "SELECT * FROM spot_entry_points WHERE status = '{}' AND action = '{}' AND symbol = '{}'".format('O','BUY',config.TRADESYMBOL)
        r1=db.prepare(sql,cnx)
        #print(r1)
        if r1:
            print("Si hay una Operacion de Compra entonces debo vender")
            sql = "SELECT orderId, open, usdt_open, quantity FROM spot_trading_open WHERE symbol = '{}' AND status = 'O' ".format(config.TRADESYMBOL)
            r2=db.prepare(sql,cnx)
            #print(r2)
            if r2:
                print("ya que existe operacion anterior consulto sus datos para verificar que el punto de venta sea mayor que el punto de compra")
                qty_profit_est = ((porcentaje_profit * float(r2[0]['open']))/100) + float(r2[0]['open'])
                #validation_price = "CLOSE " + str(float(price['price'])) + " OPEN " + str(float(r2[0]['open'])) + " SHOULD > " + str(qty_profit_est)
                #print(validation_price)
                print("Precio Venta: "+str(float(price['price'])) + " Precio de Compra + Profit Estimado: " + str(qty_profit_est))
                if(qty_profit_est < float(price['price'])):
                    print("en punto de venta si es mayor que la compra. procedemos a actualizar")

                    
                    usdt_close = (float(price['price']) * float(r2[0]['quantity']))
                    print(str(usdt_close))
                    profit = abs(round(usdt_close - float(r2[0]['usdt_open']), 3))
                    print(str(profit))



                    sql = "UPDATE spot_trading_open SET close='{}',usdt_close={},profit={},date_time_close='{}',status='C' WHERE symbol = '{}' AND status = 'O' AND orderId={} ".format(price['price'],usdt_close, profit, fecha_actual, config.TRADESYMBOL, r2[0]['orderId'])
                    r3=db.prepare(sql,cnx)
                    if r3:
                        evaluation_strategy = [ config.TRADESYMBOL, 'SELL', float(r2[0]['quantity']), float(price['price']), r2[0]['orderId']]
                        txt = "<b><u>Venta Cerrada "+ config.TRADESYMBOL+":</u></b> \n<i>Precio:</i> "+ str(price['price'] + " \n<i>Monto:</i> "+str(usdt_close)+" \n<i>Cantidad:</i> "+str(r2[0]['quantity'])+" \n<i>Profit:</i> " + str(profit))
                        asyncio.run(SendNotificationTelegram(txt))
                        print("success trading close")
                        sql = "UPDATE spot_entry_points SET status='{}' WHERE status = '{}' AND symbol = '{}' AND id={} ".format('C', 'O', config.TRADESYMBOL, r1[0]['id'])
                        r4=db.prepare(sql,cnx)
                        if r4:
                            print("success update entrypoint buy")
                            sql = "INSERT INTO spot_entry_points (symbol,price,emas,smas,action,strategy,porcent_low_over_sma,date_time, status) VALUES ('{}','{}','{}','{}','SELL','{}',{},'{}','{}')".format(config.TRADESYMBOL,price['price'], json.dumps(emas), json.dumps(smas),strategry_text + strategy_smas,porcent_over_sma,fecha_actual,'C')
                            r5=db.prepare(sql,cnx)
                            if r5:
                                print("success insert entrypoint sell")
                                evaluation_strategy.append(r5['lastID'])
                                
                                sql = "UPDATE spot_trading_open SET id_entry_point_close = {} WHERE orderId={} ".format(r5['lastID'], r2[0]['orderId'])
                                r6=db.prepare(sql,cnx)
                                #asyncio.run(SendNotificationTelegram("Puntos de Salida con: "+strategry_text + strategy_smas))
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
        print("No se cumple la estrategia para venta "+fecha_actual)
        #pass

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

    return {    "layout" :[
                    html.Div(className="line-strategy", children= [
                        html.Div(id="line_white", children=str(emas[0]['14']),style=box_line),
                        html.Div(id="line_equal", children="><",style=box_line),
                        html.Div(id="line_green", children=str(smas[0]['15']),style=box_line)
                    ], style={
                        "backgroundColor": color1,
                        "color": "white"
                    }),
                    html.Div(className="line-strategy", children= [
                        html.Div(id="line_white", children=str(emas[0]['14']),style=box_line),
                        html.Div(id="line_mayor", children=">",style=box_line),
                        html.Div(id="line_yellow", children=str(smas[1]['25']),style=box_line)
                    ], style={
                        "backgroundColor": color2,
                        "color": "white"
                    }),
                    html.Div(className="line-strategy", children= [
                        html.Div(id="line_white", children=str(emas[0]['14']),style=box_line),
                        html.Div(id="line_mayor", children=">",style=box_line),
                        html.Div(id="line_blue", children=str(smas[2]['50']),style=box_line)
                    ], style={
                        "backgroundColor": color3,
                        "color": "white"
                    })
                ],
                "evaluation": evaluation_strategy
            }

def StrategyLaterizando(klines_df, config_smas, config_emas):
    decimals_smas = config_smas[0]['decimals']
    periodos_smas = config_smas[1]['periodos']
    
    decimals_emas = config_emas[0]['decimals']
    periodos_emas = config_emas[1]['periodos']

    smas = DataSmas(klines_df, periodos_smas, decimals_smas)
    emas = DataEmas(klines_df, periodos_emas, decimals_emas)

    style_laterianzo = {
        "backgroundColor": "yellow",
        "color": "black"
    }
    return {    "layout":[
                    html.Div(className="line-strategy", children= [
                        html.Div(id="line_white", children=emas[0]['14'],style=box_line),
                        html.Div(id="line_equal", children=" ",style=box_line),
                        html.Div(id="line_yellow", children=smas[1]['25'],style=box_line)
                    ], style=style_laterianzo),
                    html.Div(className="line-strategy", children= [
                        html.Div(id="line_white", children=emas[0]['14'],style=box_line),
                        html.Div(id="line_mayor", children=" ",style=box_line),
                        html.Div(id="line_green", children=smas[0]['15'],style=box_line)
                    ], style=style_laterianzo),
                    html.Div(className="line-strategy", children= [
                        html.Div(id="line_white", children=emas[0]['14'],style=box_line),
                        html.Div(id="line_menor", children=" ",style=box_line),
                        html.Div(id="line_blue", children=smas[2]['50'],style=box_line)
                    ], style=style_laterianzo)
                ],
                "evaluation":[]
            }

def StrategyFailed(klines_df, config_smas, config_emas):
    decimals_smas = config_smas[0]['decimals']
    periodos_smas = config_smas[1]['periodos']
    
    decimals_emas = config_emas[0]['decimals']
    periodos_emas = config_emas[1]['periodos']

    smas = DataSmas(klines_df, periodos_smas, decimals_smas)
    emas = DataEmas(klines_df, periodos_emas, decimals_emas)

    style_laterianzo = {
        "backgroundColor": "orange",
        "color": "black"
    }
    return {    "layout":[
                    html.Div(className="line-strategy", children= [
                        html.Div(id="line_white", children=emas[0]['14'],style=box_line),
                        html.Div(id="line_equal", children=" ",style=box_line),
                        html.Div(id="line_yellow", children=smas[1]['25'],style=box_line)
                    ], style=style_laterianzo),
                    html.Div(className="line-strategy", children= [
                        html.Div(id="line_white", children=emas[0]['14'],style=box_line),
                        html.Div(id="line_mayor", children=" ",style=box_line),
                        html.Div(id="line_green", children=smas[0]['15'],style=box_line)
                    ], style=style_laterianzo),
                    html.Div(className="line-strategy", children= [
                        html.Div(id="line_white", children=emas[0]['14'],style=box_line),
                        html.Div(id="line_menor", children=" ",style=box_line),
                        html.Div(id="line_blue", children=smas[2]['50'],style=box_line)
                    ], style=style_laterianzo)
                ],
                "evaluation":[]
            }

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
            porcent_over_sma,
            decimals_quantity,
            info_asset
        ):
    trend_values = getTrendValues(klines_df, periodo_trend, periodo_momentum)
    diff = trend_values[0]
    _momentum = trend_values[1]
    
    strategy_layout = StrategyFailed(klines_df, config_smas, config_emas)

    if (diff > 0 and _momentum > 0):
        #print("alza compra")
        balance_asset = GetBalanceAsset(balance, 'alza')
        if(balance_asset > amount_order):
            strategy_layout = StrategyBuy(  klines_df, 
                                            price, 
                                            config_smas, 
                                            config_emas, 
                                            amount_order, 
                                            decimals_price, 
                                            porcent_low_sma,
                                            decimals_quantity,
                                            info_asset)
        else:
            print("Sin saldo para la compra")

    elif (diff < 0 and _momentum < 0):
        #print("baja vende")
        balance_asset = GetBalanceAsset(balance, 'baja')
        cant_base = balance_asset * float(price['price'])
        if(cant_base > amount_order):
            strategy_layout = StrategySell( klines_df, 
                                            price, 
                                            config_smas, 
                                            config_emas, 
                                            amount_order,
                                            porcentaje_profit, 
                                            porcent_over_sma)
        else:
            print("Sin saldo para la venta")
    else:
        #print("laterizando")
        strategy_layout = StrategyLaterizando(klines_df, config_smas, config_emas)

    return strategy_layout