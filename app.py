import dash
import dash_bootstrap_components as dbc
from dash import Input, Output, dcc, html, callback, State
import plotly.io as pio

import assets.templates.atbanalyticsgrp_dark as ATBDEFAULTTHEME

pio.templates.default = "atbAnalyticsGroupDefaultDark"

import dash
from sqlite3 import Error
import logging

import dash_bootstrap_components as dbc
import dash_core_components as dcc
from dash import html
from dash.dependencies import Input, Output
# Connect to main app.py file
from dash.exceptions import PreventUpdate

import db
import utils
from app import app
# Connect to your pages (pages)
from pages import fundamentalAnalysis, technicalAnalysis, homepage
from stock import MyStock



# BOOSTRAP APPLICATION THEME
#   CYBORG, DARKLY, LUX, MINTY, SOLAR, VAPOR,YETI -- All Cool can also create your own as well.
BS = "https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css"
# app = dash.Dash(external_stylesheets=[BS])

ATB_ANALYTICS_GRP_LOGO = './assets/img/logo/atb-analytics-group-logo.png'
FONTS = './assets/css/fonts.css'
BOOTSTRAP_THEME = dbc.themes.CYBORG
MAIN_STYLESHEET = "assets/css/style.css"

external_stylesheets = [ATBDEFAULTTHEME, FONTS, MAIN_STYLESHEET]

ALLOWED_TYPES = (
    "text", "number", "password", "email", "search",
    "tel", "url", "range", "hidden",
)

ATB_ANALYTICS_GRP_LOGO = './assets/img/logo/atb-analytics-group-logo.png'

# setup logger. Only run this once.
logging.basicConfig(level=logging.DEBUG,  # lowest level and up. # TODO Change before sending to production.
                    encoding='utf-8',
                    filename='./logs/logs.log',
                    filemode='w',
                    format="%(asctime)s - %(levelname)s - %(lineno)d | %(message)s ",
                    )

# Interacts with the Database
dbObj = db.DBConnection()

# Interacts with the yFinance API
StockObj = MyStock()
conn = None

# Connect to DB and  Load Data
DB_FILE = "./stock-db.db"

try:
    conn = dbObj.create_connection(db_file=DB_FILE)
except Error as e:
    logging.error(f"Error occurred when trying to connect to the database | {e}")

companies_df = dbObj.select_table_data(conn=conn, table_name='stock')



app = dash.Dash(__name__,
                use_pages=True,
                meta_tags=[
                    {'name': 'viewport',
                     'content': 'width=device-width, '
                                'initial-scale=1.0'
                     }
                ],
                external_stylesheets=external_stylesheets,
                title="Stock Screener | ATB Analytics Group",
                update_title="Gathering Data...",
                assets_folder="./assets",
                )

server = app.server
app.config.suppress_callback_exceptions = True
app.title = "Stock Screener"




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

    logging.info("Storage data is {}".format(data))
    return data


@callback(Output('page-content', 'children'),
              Input('url', 'pathname'))
def display_page(pathname):
    if pathname == '/pages/fundamentals':
        return fundamentalAnalysis.fundamental_page_layout

    if pathname == '/pages/technical':
        return technicalAnalysis.technical_page_layout
    else:
        home_page_layout = homepage.serve_layout()
        return home_page_layout



if __name__ == '__main__':
    app.run_server(
        debug=True
    )  # TODO Change to False in Production
