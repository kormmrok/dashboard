# import niezbednych bibliotek

import dash
from dash import dcc
from dash import html
import mysql.connector

# łączenie z bazą danych



app = dash.Dash(__name__)

app.layout = html.Div(children=[
    html.H1(children='Lista programu 3'),
    html.Div(children='''Statystyki i ciekawostki part 3'''),
    html.Label('Wykonawca: '),
    dcc.Input(
        id='wykonawca_search',
        type='search'
        )
    ])

if __name__ == '__main__':
    app.run_server(debug=True)