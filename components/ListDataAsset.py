from dash import html
import config
import pandas as pd
import dash_bootstrap_components as dbc
from helpers.functions import *

style_list_symbols = {
    "border":"1px solid lightgray",
    "marginTop":3,
}

style_list_symbol_title={
    "border":"1px solid black",
    "textAlign":"center",
    "backgroundColor":'yellow',
    "color":"black",
    "marginTop":20,
}

def PriceSymBol(price, decimals):
    return html.Label("Price: " +str( decimals.format(float(price['price']))))

def BalanceAsset(_balance):
    asset = []
    for data in _balance:
        if(data['asset'] == config.BASE_ASSET):
            asset.append(
                html.Label("Saldo "+config.BASE_ASSET + ": " +str(float(data['free'])))
            )
        if(data['asset'] == config.QUOTE_ASSET):
            asset.append(
                html.Label("Saldo "+config.QUOTE_ASSET + ": " +str(round(float(data['free']),4)))
            )
    return asset
  
def DataSmas(klines_df, config_smas):
    sma_local = []
    decimals = config_smas[0]['decimals']
    periodos = config_smas[1]['periodos']
    colors_smas = config_smas[2]['colors']

    for i in range (0,len(periodos)):
        cant_periodos_ema = (int(periodos[i]) + 0)
        klines_short = klines_df.tail(cant_periodos_ema)
        closes = klines_short['close'].tolist()
        sma_average = decimals.format(calculate_sma_average(closes, cant_periodos_ema))

        sma_local.append(
            html.Label("SMA(" + str(periodos[i]) + ") : "+ sma_average, style={'color': colors_smas[i]})
        )
    return sma_local


def DataEmas(klines_df, config_emas):
    ema_local = []
    decimals = config_emas[0]['decimals']
    periodos = config_emas[1]['periodos']
    colors_emas = config_emas[2]['colors']

    for i in range (0,len(periodos)):
        klines_short = klines_df.tail(periodos[i])
        closes = klines_short['close'].astype(float).tolist()
        last_ema = decimals.format(calculate_ema_average(closes, periodos[i]))
        ema_local.append(
            html.Label("EMA(" + str(periodos[i]) + ") : " + last_ema, style={'color': colors_emas[i]})
        )
    return ema_local
    

def DataRsi(klines_df, config_rsi):

    periodo = config_rsi[1]['periodo']
    line = config_rsi[3]['line']

    klines_df['sma'] = klines_df['close'].rolling(window=periodo).mean()
    df_diff_cp = klines_df["close"].astype('float64').diff(1)
    df_diff_cp =  df_diff_cp[1:]
    positivos = df_diff_cp.copy()
    negativos = df_diff_cp.copy()
    positivos[positivos<0]=0
    negativos[negativos>0]=0
    if line == 'ema':
        ema_positivos = positivos.ewm(com= (periodo-1), adjust=False ).mean()
        ema_negativos = abs(negativos.ewm(com= (periodo-1), adjust=False ).mean())
        rs = ema_positivos / ema_negativos

    elif line == 'sma':
        sma_positivos = positivos.rolling(periodo).mean()
        sma_negativos = abs(negativos.rolling(periodo).mean())
        rs = sma_positivos / sma_negativos
    
    rsi = 100 - (100 / (rs + 1))
    rsi_value = round(rsi.iloc[-1],2) + (round(rsi.iloc[-1],2) * 0.032)
    return html.Label("RSI(" + str(periodo) + ") : " + str(round(rsi_value,2)), style={'color': 'pink'})

def DatosAssetTrading(price, decimals_price, balance, klines_df, config_smas, config_emas, config_rsi):
    list_data = []
    list_data.append(
        dbc.Col(children="DATOS ASSET",style=style_list_symbol_title, md=12)
    )
    
    price_layout = PriceSymBol(price, decimals_price)
    list_data.append(price_layout)

    list_data.append(dbc.Col(children=[html.Hr()], md=12))
    
    balance_layout = BalanceAsset(balance)
    for bal in balance_layout:
        list_data.append(bal)

    list_data.append(dbc.Col(children=[html.Hr()], md=12))
    
    smas_layout = DataSmas(klines_df, config_smas)
    for sma in smas_layout:
        list_data.append(sma)

    emas_layout = DataEmas(klines_df, config_emas)
    for ema in emas_layout:
        list_data.append(ema)

    rsi_layout = DataRsi(klines_df, config_rsi)
    list_data.append(rsi_layout)

    return  [dbc.Row(children = list_data)]