import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from app import dash_app

from pages import flop, player
from app import app

#main layout
dash_app.layout = html.Div([
    html.H1(children='Poker Dashboard'),
    dcc.Tabs(id='tabs', value='flop', children=[
        dcc.Tab(label='Flop Analysis', value='flop'),
        dcc.Tab(label='Player Analysis', value='player'),
    ]),
    html.Div(id='tabs-content')
])

@dash_app.callback(Output('tabs-content', 'children'),
              Input('tabs', 'value'))
def render_content(tab):
    if tab == 'flop':
        return flop.layout
    elif tab == 'player':
        return player.layout

if __name__ == '__main__':
    dash_app.run_server(debug=True)
