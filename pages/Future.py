import dash
from dash import html
from components.ListSymbols import ListSymbols

dash.register_page(__name__)

def layout():
    return  [
                html.Div(children=[
                        html.Div(
                            className='row',
                            children=[
                                html.Div(
                                    className='col-2',
                                    children=[
                                        html.Div(
                                            className='row',
                                            children= ListSymbols()
                                        )
                                    ]
                                ),
                                html.Div(
                                    className='col-7',
                                    children=[
                                        html.Div(id='content_graph'),
                                    ]
                                ),
                                html.Div(
                                    className='col-3',
                                    children='Operaciones directas'
                                )
                            ]
                        ),
                        html.Div(
                            className='row',
                            children=[
                                html.Div(
                                    className='col-12',
                                    children="Columna de ordenes abiertas"
                                )
                            ]
                        ),
                        html.Div(
                            className='row',
                            children=[
                                html.Div(
                                    className='col-4',
                                    children='Box 3'
                                ),
                                html.Div(
                                    className='col-4',
                                    children='Box 4'
                                ),
                                html.Div(
                                    className='col-4',
                                    children='Box 5'
                                )
                            ]
                        )     
                    ],
                    style={

                    }
                )
            ]