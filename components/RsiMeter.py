import pandas as pd
from dash import dcc
import plotly.graph_objects as go


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
    return rsi_value

def generate_gauge(rsi_value):
    sobrecompra = 69
    sobreventa = 31
    min_value = 0
    max_value = 100

    if rsi_value <= sobreventa:
        estado = "Sobreventa"
        color = "red"    
    elif rsi_value >= sobrecompra:
        estado = "Sobrecompra"
        color = "green"
    else:
        estado = ""
        color = "yellow"

    sector = [
        {'range': [0, 31], 'color': 'red'},
        {'range': [31, 69], 'color': 'yellow'},
        {'range': [69, 100], 'color': 'green'}
    ]

    gauge = go.Figure(go.Indicator(
        mode="gauge+number",
        value = rsi_value,
        delta={
            "font":{
                "color": color
            },
            'reference': rsi_value,
            "position":"top"
        },
        title = {
            "text": estado,
            "font_size":11
        },
        gauge = {
            'axis': {'range': [min_value, max_value]},
            'bar': {
                'color': 'rgba(0,0,0,0)'
            },
            'steps': sector,
            'threshold': {
                'line': {'color': 'blue', 'width': 4},
                'thickness': 0.75,
                'value': rsi_value
            },
        }
    ))
    return gauge

def GraphRsiMeter(klines_df, config_rsi):
    rsi_value = DataRsi(klines_df, config_rsi)
    fig = generate_gauge(rsi_value)
    return [dcc.Graph(id='rsi_meter_chart', animate=False, figure=fig)]