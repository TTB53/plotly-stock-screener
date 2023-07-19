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

CONTENT_STYLE = {
    "margin-left": "20%",
    "margin-right": "2rem",
    "min-width": "80%",
    "padding": "2rem 1rem",
}

sidebar_header = dbc.Row(
    [
        dbc.Col(
            [
                dcc.Link([
                    html.Img(id='logoImg', src=ATB_ANALYTICS_GRP_LOGO, alt="ATB Analytics Group Logo")
                ], href="https://www.atb-analytics-group.webflow.io"),
            ],
        ),

        dbc.Col(
            [
                html.Button(
                    # use the Bootstrap navbar-toggler classes to style
                    html.Span(className="navbar-toggler-icon"),
                    className="navbar-toggler",
                    # the navbar-toggler classes don't set color
                    style={
                        "color": "rgba(0,0,0,.5)",
                        "border-color": "rgba(0,0,0,.1)",
                    },
                    id="navbar-toggle",
                ),
                html.Button(
                    # use the Bootstrap navbar-toggler classes to style
                    html.Span(className="navbar-toggler-icon"),
                    className="navbar-toggler",
                    # the navbar-toggler classes don't set color
                    style={
                        "color": "rgba(0,0,0,.5)",
                        "border-color": "rgba(0,0,0,.1)",
                    },
                    id="sidebar-toggle",
                ),
            ],
            # the column containing the toggle will be only as wide as the
            # toggle, resulting in the toggle being right aligned
            width="auto",
            # vertically align the toggle in the center
            align="center",
        ),
        dbc.Col([
            html.Br(),
            html.H2(
                id='sidebar-menu-name',
                children=["Home"],
                # className="display-5",
            ),
        ],
            width=12,
        ),

    ]
)

sidebar = html.Div(
    [
        html.Br(),
        sidebar_header,
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
        dbc.Collapse(
            dbc.Nav(
                [
                    dbc.NavLink(f"{page['name']} ", href=page["relative_path"]) for page in
                    dash.page_registry.values() if page["module"] != "pages.not_found_404"

                ],
                vertical=True,
                pills=True,
            ),
            id="collapse",
        ),
        # theme_switch,
    ],
    id="sidebar",
)

content = dbc.Container(id='page-content',
                          children=[],
                          className='col-md-8',
                          style=CONTENT_STYLE,
                          fluid=True,
                          )

# dash.register_page(__name__, path='/', name='Homepage') # for use with use pages.
layout = dbc.Container(
    children=[
        dbc.Row([

            dcc.Location(id='url', refresh=False),
            dcc.Loading(dcc.Store(id='stock-storage', storage_type='session', data=[]), fullscreen=True, type="dot",
                        color="AQUAMARINE"),
            dbc.Col(utils.get_nav(app), width=8, style=CONTENT_STYLE),
            sidebar,
            content
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

    logging.info("Storage data is {}".format(data))
    return data


@app.callback(Output('page-content', 'children'),
              Input('url', 'pathname'))
def display_page(pathname):
    if pathname == '/pages/fundamentals':
        return fundamentalAnalysis.fundamental_page_layout

    if pathname == '/pages/technical':
        return technicalAnalysis.technical_page_layout
    else:
        home_page_layout = homepage.serve_layout()
        return home_page_layout


# if __name__ == '__main__':
#     app.run_server(
#         debug=True
#     )  # TODO Change to False in Production
