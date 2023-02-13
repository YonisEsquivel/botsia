import dash
from dash import html
from dash import dcc
import dash_bootstrap_components as dbc


def routerpages():
    links=[]
    for page in dash.page_registry.values():
        links.append(
            dbc.NavItem(dbc.NavLink(f"{page['name']}", href=page["relative_path"]))
        )
    return links

def NavBarHor():
    return html.Div(children=[
        dbc.Navbar(
            dbc.Container(
                    [
                        dbc.NavbarToggler(id="navbar-toggler", n_clicks=0),
                        dbc.Collapse(
                            children = [ dbc.Nav(children = routerpages(),pills=True,fill=True)],
                            id="navbar-collapse",
                            is_open=False,
                            navbar=True,
                        ),
                    ],
                    style={
                        "justifyContent": "normal",
                        "maxWidth": "100%",
                    }
                    ),
            color="dark",
            dark=True,
            style={
                "color": "white",
            }
        )
    ])
