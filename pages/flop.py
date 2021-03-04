import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from app import dash_app
import dash_table
import dash
from dash.exceptions import PreventUpdate


cards = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
suits = ["Spade", "Heart", "Diamond", "Club"]

layout = html.Div(children=[
            html.Table(
                style={"width":"100%"},
                children=[
                    html.Tr(
                        children=[
                            html.Td(
                                children=[
                                    html.H1("Hand"),
                                    html.P(),
                                    dcc.Dropdown(
                                        id='hand1_card',
                                        options=[
                                            {'label': i, 'value': i} for i in cards
                                        ],
                                    ),
                                    dcc.Dropdown(
                                        id='hand1_suit',
                                        options=[
                                            {'label': i, 'value': i} for i in suits
                                        ],
                                    ),
                                    html.Br(),
                                    dcc.Dropdown(
                                        id='hand2_card',
                                        options=[
                                            {'label': i, 'value': i} for i in cards
                                        ],
                                    ),
                                    dcc.Dropdown(
                                        id='hand2_suit',
                                        options=[
                                            {'label': i, 'value': i} for i in suits
                                        ],
                                    ),
                                ]
                            ),
                            html.Td(
                                children=[
                                    html.H1("Probability"),
                                    html.Div(children=[
                                        html.P(),
                                        dash_table.DataTable(
                                            id='table_prob',
                                            columns=[{"name": "Hand", "id": "Hand"}, {"name": "Probability", "id": "Probability"}],
                                        ),
                                    ]),
                                ]
                            ),
                        ]
                    )
                ]
            ),
        ])

@dash_app.callback(
    [
        dash.dependencies.Output('table_prob', 'data'),
    ],
    [
        dash.dependencies.Input('hand1_card', 'value'),
        dash.dependencies.Input('hand2_card', 'value'),
        dash.dependencies.Input('hand1_suit', 'value'),
        dash.dependencies.Input('hand2_suit', 'value'),
    ]
)
def update_table(card1, card2, suit1, suit2):
    if card1 is None or card2 is None or suit1 is None or suit2 is None:
        raise PreventUpdate

    flush = 0
    straight = 0
    set = 0
    twopair = 0
    toppair = 0

    if suit1 == suit2:
        flush = "0.84%"

    if (abs(cards.index(card1) - cards.index(card2)) < 5):
        upper_range = max(cards.index(card1), cards.index(card2))
        lower_range = min(cards.index(card1), cards.index(card2))
    elif (card1 == "A" and abs(13 - cards.index(card2)) < 5):
        upper_range = 13
        lower_range = cards.index(card2)
    elif (card2 == "A" and abs(13 - cards.index(card1)) < 5):
        upper_range = 13
        lower_range = cards.index(card1)
    else:
        upper_range = None
        lower_range = None

    if upper_range is not None:
        diff = upper_range - lower_range
        upper_max = min(13, upper_range + (4 - diff))
        lower_max = max(0, lower_range - (4 - diff))
        total_range = upper_max - lower_max
        num_straight = total_range - 3
        straight = str(num_straight * 0.003265 * 100) + "%"

    if card1 == card2:
        set = "11.5%"
        twopair = "17.6%"
        straight = 0
    else:
        set = "1.4%"
        twopair = "4%"

    data = [{"Hand": "Flush", "Probability": flush}, {"Hand": "Straight", "Probability": straight},
            {"Hand": "Set", "Probability": set}, {"Hand": "Two Pair", "Probability": twopair},
            {"Hand": "Top Pair", "Probability": toppair}]

    return [data]
