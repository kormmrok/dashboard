# import niezbednych bibliotek

import dash
from dash import dcc
from dash import html
from dash.dependencies import DashDependency
from dash.exceptions import PreventUpdate
import mysql.connector

# options = []

app = dash.Dash(__name__)

app.layout = html.Div(children=[
    html.H1(children='Lista programu 3'),
    html.Div(children='''Statystyki i ciekawostki part 3'''),
    html.Label('Wykonawca: '),
    dcc.Dropdown(id='wykonawca'),
    dcc.Dropdown(id='tytul')
    ])


@app.callback(
    dash.dependencies.Output("wykonawca", "options"),
    [dash.dependencies.Input("wykonawca", "search_value")],
)
def zwrot_listy(search_value):
    # łączenie z bazą danych
    mydb = mysql.connector.connect(
        host = 'localhost',
        user = 'python',
        password = 'python',
        database = "lista_portfolio"
    )

    mycursor = mydb.cursor()
    
    options = []
    if not search_value:
        raise PreventUpdate
    if len(search_value)>3:
        mycursor.execute("SELECT DISTINCT wykonawca FROM lp3 WHERE wykonawca LIKE " + "'%" + search_value + "%'" + ";")
        wynik = mycursor.fetchall()
        wynik_list = [list(i) for i in wynik]
        for i in wynik_list:
            options.append({"label": i[0], "value": i[0]})    
    mydb.close()        
    return [o for o in options if search_value.casefold() in o["label"].casefold()]


@app.callback(
    dash.dependencies.Output("tytul", "options"),
    [dash.dependencies.Input("wykonawca", "value")]
)
def utwory(value):
    
     # łączenie z bazą danych
    mydb = mysql.connector.connect(
        host = 'localhost',
        user = 'python',
        password = 'python',
        database = "lista_portfolio"
    )

    mycursor = mydb.cursor()

    options = []
    if not value:
        raise PreventUpdate
    mycursor.execute("SELECT DISTINCT tytul FROM lp3 WHERE wykonawca='" + value +"' ORDER BY tytul;")
    wynik = mycursor.fetchall()
    wynik_list = [list(i) for i in wynik]
    for i in wynik_list:
        options.append({"label" : i[0], "value" : i[0]})
    mydb.close()
    return options

if __name__ == '__main__':
    app.run_server(debug=True)