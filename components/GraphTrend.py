from dash import html
import pandas as pd
from helpers.functions import *

def ShowGraphTrend(klines_df, periodo_trend, periodo_momentum):
    trend_values = getTrendValues(klines_df, periodo_trend, periodo_momentum)
    diff = trend_values[0]
    _momentum = trend_values[1]
    
    if (diff > 0 and _momentum > 0):
        layout_trend = html.Img(src='assets/alza.jpg', style={'width': '100%', "height":250})
    elif (diff < 0 and _momentum < 0):
        layout_trend = html.Img(src='assets/baja.jpg', style={'width': '100%', "height":250})
    else:
        layout_trend = html.Img(src='assets/laterizando.jpg', style={'width': '100%', "height":250})

    return [layout_trend]