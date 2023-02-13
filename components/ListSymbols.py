from dash import html
import dash_bootstrap_components as dbc

symbols = ["BTCUSDT","BNBUSDT","ETHUSDT","SOLUSDT"]


style_list_symbols = {
    "border":"1px solid lightgray",
    "marginTop":3,
}

style_list_symbol_title={
    "border":"1px solid black",
    "textAlign":"center",
    "backgroundColor":'yellow',
    "color":"black",
}

def ListSymbols():
    list_symbols = []
    list_symbols.append(
        dbc.Col(children="SYMBOLS",style=style_list_symbol_title,md=12)
    )
    for symbol in symbols:
        list_symbols.append(
            dbc.Col( children=symbol, style=style_list_symbols, md=12)
        )
    return  [dbc.Row(children = list_symbols)]