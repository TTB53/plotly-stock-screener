from sqlite3 import Error

import dash_bootstrap_components as dbc
import dash_core_components as dcc
from dash.dependencies import Input, Output
# Connect to main app.py file
from dash.exceptions import PreventUpdate

import db
import utils
from app import app
# Connect to your apps (pages)
from apps import fundamentalAnalysis, technicalAnalysis, homepage
from stock import MyStock

# Interacts with the Database
dbObj = db.DBConnection()

# Interacts with the yFinance API
StockObj = MyStock()
conn = None

# Connect to DB and  Load Data
DB_FILE = "C:/Users/TTB53\Documents/The_Vintage_D_Modernist/TVDM Digital/PythonProjects/stock-db.db"

try:
    conn = dbObj.create_connection(db_file=DB_FILE)
except Error as e:
    print(e)

companies_df = dbObj.select_table_data(conn=conn, table_name='stock')

CONTENT_STYLE = {
    "margin-left": "20%",
    "margin-right": "2rem",
    "min-width": "80%",
    "padding": "2rem 1rem",
}

app.layout = dbc.Container([

    dbc.Row([

        dcc.Location(id='url', refresh=False),
        dcc.Store(id='stock-storage', storage_type='session', data=[]),
        dbc.Col(utils.get_nav(app), width=8, style=CONTENT_STYLE),
        dbc.Container(id='page-content',
                      children=[],
                      className='col-md-8',
                      style=CONTENT_STYLE,
                      fluid=True,
                      )
    ]),
])


@app.callback(Output('stock-storage', 'data'),
              Input('companies_dropdown', 'value'))
def add_stock_data_to_storage(stock_symbol, data=None):
    if stock_symbol is None or stock_symbol == "Company Ticker Symbol":
        raise PreventUpdate

    stock_data = companies_df.query('"{}" in company'.format(stock_symbol))
    data = data or {'stock': stock_data['symbol'].values[0],
                    'company': stock_data['company'].values[0],
                    'sector': stock_data['gics_sector'].values[0],
                    'subsector': stock_data['gics_subsector'].values[0],
                    }

    print("Storage data is {}".format(data))
    return data


@app.callback(Output('page-content', 'children'),
              Input('url', 'pathname'))
def display_page(pathname):
    if pathname == '/apps/fundamentals':
        return fundamentalAnalysis.fundamental_page_layout

    if pathname == '/apps/technical':
        return technicalAnalysis.technical_page_layout
    else:
        home_page_layout = homepage.serve_layout()
        return home_page_layout


if __name__ == '__main__':
    app.run_server(debug=True)  # TODO Change to False in Production
