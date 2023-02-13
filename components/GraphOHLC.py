import pandas as pd
from dash import dcc
import config
import plotly.graph_objects as go
from helpers.functions import *

def GraphOHLC(n, klines_df, config_smas, config_emas, periodo_graph, longitud_graph):
    try:        
        print("render graph " + str(n))
        smas = config_smas[1]['periodos']
        emas = config_emas[1]['periodos']
        df = calculate_smas_list(klines_df, smas)
        df = calculate_ema_list(klines_df, emas, periodo_graph)
        df = df.tail(longitud_graph)
        graph_candlestick = go.Candlestick(x=df["closeTime"], open=df["open"], high=df["high"], low=df["low"], close=df["close"], name='Price')
        graph_layout = [graph_candlestick]

        for i in smas:
            sma = go.Scatter(x=df["closeTime"], y=df[f'sma_{i}'], name=f'sma_{i}',line=dict(width=2, color='blue' if i==50 else 'green' if i==15 else 'yellow'))
            graph_layout.append(sma)

        for j in emas:
            ema = go.Scatter(x=df["closeTime"], y=df[f'ema_{j}'], name=f'ema_{j}',line=dict(width=2, color='white'))
            graph_layout.append(ema)


        layout = go.Layout(xaxis=dict(rangeslider=dict(visible=False)),yaxis=dict(title='Price'))

        fig = go.Figure(data=graph_layout,layout=layout)
        
        title = {
            'text': " Candlestick Chart "+config.TRADESYMBOL,
            'y':0.9,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top' 
        }

        xaxis = {
            'showline':True,
            'rangeslider_visible':False,
            'title':'Date',
            "showspikes": True,
            "spikemode": "across",
            "spikedash": "solid",
            'linewidth':2,
            'spikecolor':"white", 
            'spikethickness':1,
        }
        yaxis = {
            'showline':True,
            'title':'Price',
            'side':'right',
            'tickformat' : 'd',
            "showspikes": True,
            "spikemode": "across",
            "spikedash": "solid",
            'linewidth':2,
            'spikecolor':"white", 
            'spikethickness':1,
        }
        fig.update_layout(
                hovermode="x unified", 
                showlegend = True,
                xaxis = xaxis,
                yaxis = yaxis,
                title=title,
                plot_bgcolor="rgb(30, 30, 30)",
                transition= {
                    'duration': 500,
                    'easing': 'cubic-in-out'
                },
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=1.02,
                    xanchor="right",
                    x=1,
                    traceorder="normal",
                    font=dict(
                        family="sans-serif",
                        size=12,
                        color="white"
                    ),
                    bgcolor="rgb(30, 30, 30)",
                    bordercolor="white",
                    borderwidth=1
                )
            )
        fig.update_xaxes(showgrid=False)
        fig.update_yaxes(showgrid=False)
        fig.update_traces(overwrite=True)

        return [ dcc.Graph(id='graph_chart', animate=False, figure=fig)]

    except Exception as e:
        print("Error: ", e)