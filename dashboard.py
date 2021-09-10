# import niezbednych bibliotek

import dash
from dash import dcc
from dash import html
from dash import dependencies
from dash.html.Div import Div
from dash.html.Table import Table
from dash.html.Tr import Tr
import pandas as pd
import plotly.express as px
from dash.exceptions import PreventUpdate
import mysql.connector


def baza(sql_query):
     # łączenie z bazą danych
    mydb = mysql.connector.connect(
        host = 'localhost',
        user = 'python',
        password = 'python',
        database = "lista_portfolio"
    )

    mycursor = mydb.cursor()
    
    mycursor.execute(sql_query)
    wynik = mycursor.fetchall()
    mydb.close()
    return wynik


app = dash.Dash(__name__)

app.layout = html.Div(children=[
    html.Div(['Lista przebojów programu 3'], className='naglowek'),
    html.Div([
        html.Div('Wykonawca: ', className='etykieta'),
        html.Div([
            dcc.Dropdown(id='wykonawca', placeholder='Wpisz nazwę wykonawcy...')], className='dropdown')
        ], style={'display':'flex'}),
    html.Div([
        html.Div('Tytuł: ', className='etykieta'),
                html.Div([
            dcc.Dropdown(id='tytul', placeholder='Wybierz utwór...')], className='dropdown')
    ], style={'display':'flex'}),
    html.Div([], id='tabela'),
    html.Div([], id='utwor-1'),
    ])


@app.callback(
    dash.dependencies.Output("wykonawca", "options"),
    [dash.dependencies.Input("wykonawca", "search_value"),
    dash.dependencies.Input("tytul", "options")]
)
def zwrot_listy(search_value, opcje):
    
    options = []
    
    if not search_value and not opcje:
        return options
    elif not search_value:
        raise PreventUpdate
    if len(search_value)>1:
        wynik = baza("SELECT DISTINCT wykonawca FROM lp3 WHERE wykonawca LIKE " + "'%" + search_value.replace("'", "''") + "%'" + ";")       
        wynik_list = [list(i) for i in wynik]
        for i in wynik_list:
            options.append({"label": i[0], "value": i[0]})    
    
    return [o for o in options if search_value.casefold() in o["label"].casefold()]


@app.callback(
     dash.dependencies.Output("tytul", "options"),
    [dash.dependencies.Input("wykonawca", "value"),
    dash.dependencies.Input("wykonawca", "search_value")]
)
def utwory(value, search_value):
    options = []
    
    if not value:
        return options
#        raise PreventUpdate
    
    wynik = baza("SELECT DISTINCT tytul FROM lp3 WHERE wykonawca='" + value.replace("'", "''") +"' ORDER BY tytul;")
    wynik_list = [list(i) for i in wynik]
    
    for i in wynik_list:
        options.append({"label" : i[0], "value" : i[0]})
    
    return options


@app.callback(
    [dash.dependencies.Output("utwor-1", "children"),
    dash.dependencies.Output("tabela", "children")],
    [dash.dependencies.Input("tytul", "value"),
    dash.dependencies.Input("wykonawca", "value")]
)
def wykres(tytul, wykonawca):
        
    if not tytul or not wykonawca:
        return [html.Div(), html.Div()]
#        raise PreventUpdate
    
    dataframe = baza("SELECT distinct pozycja, notowanie, data_notowania FROM lp3 where tytul='"+ tytul.replace("'", "''") + "' and wykonawca='" + wykonawca.replace("'", "''") + "';")
    
    df = pd.DataFrame(dataframe, columns=['pozycja', 'notowanie', 'data_notowania'])
    if len(df) == 0:
        return [html.Div(), html.Div()]
    
    fig = px.line(df, x='data_notowania', y='pozycja', markers=True, text='notowanie')
    fig.update_yaxes(title_font=dict(size=18, family='Verdana', color='blue'), autorange = "reversed", title_text = 'Pozycja', title_standoff = 25, ticks = 'inside', tickvals=[1,5,10,15,20,25,30,35,40,45,50])
    fig.update_xaxes(title_font=dict(size=18, family='Verdana', color='blue'), tickformat='%d-%m-%Y', title_text = 'Data notowania', title_standoff = 25, tickangle = 45, tickvals=df['data_notowania'].tolist(), ticks = 'inside')
    fig.update_traces(textposition="bottom center")
    
    pozycja_naj = df['pozycja'].min()
    tygodnie = len(df)
    
    return [dcc.Graph(figure=fig),
        html.Table([
            html.Tr([
                html.Td('Najwyższa pozycja', className='statystyka_nazwa'),
                html.Td(pozycja_naj, className='statystyka_wartosc'),
                html.Td('Ilość tygodni na liście', className='statystyka_nazwa'),
                html.Td(tygodnie, className='statystyka_wartosc')
            ], className='tr'),
            html.Tr([
#               html.Td('Ilość tygodni na liście', className='statystyka_nazwa'),
#              html.Td(tygodnie, className='statystyka_wartosc')
            ], className='tr'),
        ], className='tabela')
    ]

if __name__ == '__main__':
    app.run_server(debug=True)