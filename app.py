"""
Author - Anthony Thomas - Bell
Version 2.0
Aug 6 2023

-------------------------------------------------------------------------------
Program Description
-------------------------------------------------------------------------------


Main Entry point into the Stock Screener Application.

Will Help to identify Market Trends and Patterns, Analyze companies by their fundaments
and technical analysis
-------------------------------------------------------------------------------
v1.0 May 2021 - July 2023
v2.0 July 2023 - Present

"""

import sqlalchemy

import config
import dash_bootstrap_components as dbc
from dash import Input, Output, dcc, html, callback, State
import plotly.io as pio

import assets.templates.atbanalyticsgrp_dark as ATBDEFAULTTHEME

pio.templates.default = "atbAnalyticsGroupDefaultDark"

import dash
from sqlite3 import Error
import logging

import dash_core_components as dcc
from dash import html
from dash.dependencies import Input, Output
# Connect to main app.py file
from dash.exceptions import PreventUpdate

import db
from utils import Utils as utils

# Connect to your pages (pages)
# from pages import fundamentalAnalysis, technicalAnalysis, homepage
# from stock import MyStock

# BOOSTRAP APPLICATION THEME
#   CYBORG, DARKLY, LUX, MINTY, SOLAR, VAPOR,YETI -- All Cool can also create your own as well.
BS = "https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css"
# app = dash.Dash(external_stylesheets=[BS])

ATB_ANALYTICS_GRP_LOGO = './assets/img/logo/atb-analytics-group-logo.png'
FONTS = './assets/css/fonts.css'
BOOTSTRAP_THEME = dbc.themes.CYBORG
BOOTSTRAP_ICONS = dbc.icons.BOOTSTRAP
FA_ICONS = dbc.icons.FONT_AWESOME
MAIN_STYLESHEET = "assets/css/style.css"

external_stylesheets = [
    BOOTSTRAP_THEME,
    BOOTSTRAP_ICONS,
    FA_ICONS,
    ATBDEFAULTTHEME,
    FONTS,
    MAIN_STYLESHEET
]

ALLOWED_TYPES = (
    "text", "number", "password", "email", "search",
    "tel", "url", "range", "hidden",
)

# creating the config clas
DEFAULTS = config.ScreenerConfig()

# setup logger. Only run this once.
logging.basicConfig(level=logging.DEBUG,  # lowest level and up. # TODO Change before sending to production.
                    encoding='utf-8',
                    datefmt='%m-%d-%y %H:%M',
                    filename='./logs/logs.log',
                    filemode='w',
                    format="%(asctime)s - %(levelname)s - %(lineno)d | %(message)s ",
                    )

# Interacts with the Database
dbObj = db.DBConnection()

# Interacts with the yFinance API
# StockObj = MyStock()
conn = None

# Connect to DB and  Load Data
DB_FILE = DEFAULTS.database_defaults['sqlite']['DB_FILE']
DB_FILE_SQLALCHMY = DEFAULTS.database_defaults['sqlite']['DB_FILE_SA_SQLITE']

try:
    conn = dbObj.create_connection(db_file=DB_FILE_SQLALCHMY)
    logging.info(f"Successfully Connected to the DB using {DB_FILE_SQLALCHMY}")
    logging.info(f"SQLAlchemy Version -- {sqlalchemy.__version__}")
except Error as e:
    logging.error(f"Error occurred when trying to connect to the database using {DB_FILE_SQLALCHMY}| {e}")

companies_df = dbObj.select_table_data(conn=conn, table_name='stock')

page_stock_info_ids = {}
# page_stock_info_ids['stock-name'] = 'stock-name'
# page_stock_info_ids['stock-title'] = 'stock-title'
# page_stock_info_ids['stock-price'] = 'stock-price'
# page_stock_info_ids['stock-sector'] = 'stock-sector'
# page_stock_info_ids['stock-subsector'] = 'stock-subsector'

app = dash.Dash(__name__,
                use_pages=True,
                external_stylesheets=external_stylesheets,
                meta_tags=[
                    {'name': 'viewport',
                     'content': 'width=device-width, '
                                'initial-scale=1.0'
                     }
                ],
                title="Stock Screener | ATB Analytics Group",
                update_title="Gathering Data...",
                assets_folder="./assets",
                )

navbar_sticky = utils.get_nav(utils, 1)

sidebar = dbc.Col(
    id='sidebar',
    # className='col-md-4',
    children=[
        html.Br(),
        # sidebar_header,
        dbc.Row(
            [
                html.Br(),
                html.Div(
                    id="blurb",
                    children=[
                        # width: 3rem ensures the logo is the exact width of the
                        # collapsed sidebar (accounting for padding)
                        # html.Img(src=PLOTLY_LOGO, style={"width": "3rem"}),
                        # html.H2("Sidebar", ),
                        html.P("This is a blurb that is about, the menu items.")
                    ],

                ),
                html.Hr(),

                # dbc.Nav(
                #     [
                #         dbc.NavLink(f"{page['name']} ", href=page["relative_path"]) for page in
                #         dash.page_registry.values() if page["module"] != "pages.not_found_404"
                #     ],
                #     vertical=True,
                #     pills=True,
                # ),

                # html.Div(stock_row_info, )
                # theme_switch,
            ]
        ),

    ],
    # width=12
)

content = dbc.Col(
    id='page-content',
    children=[dash.page_container],
    # className='col-md-8',
    # style=CONTENT_STYLE,
    width="auto",
)

# Application Layout
app.layout = dbc.Container(
    children=[
        dcc.Loading(
            children=[
                dcc.Store(
                    id='stock-storage',
                    storage_type='session',
                    data=[]
                )
            ],
            fullscreen=True,
            type="dot",
            color=utils.get_random_color(utils, ),
        ),

        dbc.Row(
            children=[
                navbar_sticky,
                content
            ],
        )

    ],
    fluid=True
)


@callback(
    Output('stock-storage', 'data'),
    Input('companies_dropdown', 'value'),
)
def add_stock_data_to_storage(stock_symbol, data=None):
    if stock_symbol is None or stock_symbol == "Company Ticker Symbol":
        logging.error(f"Error Occurred {stock_symbol} is None.")
        raise PreventUpdate

    stock_data = companies_df.query('"{}" in company'.format(stock_symbol))
    data = data or {'stock': stock_data['symbol'].values[0],
                    'company': stock_data['company'].values[0],
                    'sector': stock_data['gics_sector'].values[0],
                    'subsector': stock_data['gics_subsector'].values[0],
                    }

    logging.info(f"Storage data is {data}")
    return data


# @callback(
#     Output("sidebar", "className"),
#     [Input("sidebar-toggle", "n_clicks")],
#     [State("sidebar", "className")],
#     suppress_callback_exceptions=True,
#     prevent_initial_callbacks=True,
# )
# def toggle_classname(n, classname):
#     if n and classname == "":
#         return "collapsed"
#     return ""


@callback(
    Output("collapse", "is_open"),
    [Input("navbar-toggler2", "n_clicks")],
    [State("collapse", "is_open")],
    suppress_callback_exceptions=True,
    prevent_initial_callbacks=True,
)
def toggle_collapse(n, is_open):
    if n:
        return not is_open
    return is_open


# @callback(
#     Output('sidebar-menu-name', 'children'),
#     Output('blurb', 'children'),
#     Input('stock-storage', 'data'),
#     Input('page-content', 'children'),
#     suppress_callback_exceptions=True,
#     prevent_initial_callbacks=True,
# )
# def update_sidebar_menu(data, page_content):
#     pathname = page_content[0]['props']['children'][0]['props']['pathname']
#     logging.info(f"{pathname} | {page_content}")
#
#     if pathname == '/fundamental-analysis':
#         menu_name = "Fundamental Analysis"
#         blurb = "Fundamental Analysis is ..."
#     elif pathname == '/technical-analysis':
#         menu_name = "Technical Analysis "
#         blurb = """
#                 Technical Analysis is...
#             """
#     #     elif pathname == '/contact':
#     #         menu_name = "Contact ATB Analytics Group"
#     #         blurb = """
#     #                         Ready to do more with your data?
#     #                         Looking to have something similar created for your business.
#     #                         Get in touch with us today.
#     #                     """
#     #     elif pathname == '/about':
#     #         menu_name = "About"
#     #         blurb = """
#     # This is a little history on OList and the Economy of Brazil at the time that this dataset was published.
#     #                         """
#     #     elif pathname == '/marketing-analysis':
#     #         menu_name = "Marketing Analysis"
#     #         blurb = """
#     #                            This is the Marketing Campaign Data that was provided by OList.
#     #                        """
#     else:
#         menu_name = "Stock Screener"
#         blurb = "A Simpler way to view and learn about the stock market."
#     return menu_name, blurb


# @callback(Output('page-content', 'children'),
#           Input('url', 'pathname'))
# def display_page(pathname):
#     if pathname == '/pages/fundamentals':
#         return fundamentalAnalysis.fundamental_page_layout
#
#     if pathname == '/pages/technical':
#         return technicalAnalysis.technical_page_layout
#     else:
#         home_page_layout = homepage.serve_layout()
#         return home_page_layout


# server = app.server
# app.config.suppress_callback_exceptions = True
# app.title = "Stock Screener"

if __name__ == '__main__':
    app.run_server(
        debug=True
    )  # TODO Change to False in Production
