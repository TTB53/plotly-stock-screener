"""
Utils

------------------------------------------------------------------------------
Program Description
-------------------------------------------------------------------------------

utility file that houses helper functions for things related to
    - Data Viz and graphing
    - Common Components across various pages
    - Certain Financial Functions

----------------------------------------------------------------------------------

"""
import os
import re
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import random

import dash
import dash_bootstrap_components as dbc
from dash import html, dcc, dash_table
import dash_table.FormatTemplate as FormatTemplate
import pandas as pd
import numpy as np
import plotly.graph_objs as go
from dash_table.Format import Sign
from plotly.subplots import make_subplots

# DB Error and Logging
from sqlite3 import Error
import logging

# import app
from sqlalchemy import text

import assets.templates.atbanalyticsgrp_dark as ATBDEFAULTTHEME
import db

SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "max-width": "20%",
    "padding": "2rem 1rem",
    # "background-color": "#f8f9fa",
    "overflow": "auto",
    "overflow-x": "hidden",
}

'''
Produces the Navigation Bar that is on every app(page) of the applcation.
'''

PLOTLY_LOGO = "https://images.plot.ly/logo/new-branding/plotly-logomark.png"
ATB_ANALYTICS_GRP_LOGO = './assets/img/logo/atb-analytics-group-logo.png'


class Utils:

    def get_nav(self, nav_selection):
        nav = dbc.Nav(
            id='navigation',
            children=[

                dbc.NavLink(
                    children=
                    [
                        html.I(
                            children=[],
                            className="bi bi-house"
                        ),
                        "Home"
                    ],
                    href="/",
                    active="exact",
                ),
                dbc.NavLink(
                    [
                        html.I(
                            children=[],
                            className="bi bi-clipboard-data"
                        ),
                        "Fundamental Analysis"
                    ], href="/pages/fundamentals",
                    active="exact"),
                dbc.NavLink(
                    [
                        html.I(
                            children=[],
                            className="bi bi-graph-up-arrow"
                        ),
                        "Technical Analysis"
                    ], href="/pages/technical",
                    active="exact"),
            ],
            pills=True,
            fill=True,
        ),

        navbar_objs = {
            1: dbc.Navbar(
                dbc.Container(
                    [
                        html.A(
                            # Use row and col to control vertical alignment of logo / brand
                            dbc.Row(
                                [
                                    dbc.Col(html.Img(src=ATB_ANALYTICS_GRP_LOGO, height="20px")),
                                    dbc.Col(dbc.NavbarBrand("ATB Analytics Group", className="ms-2")),
                                ],
                                align="center",
                                className="g-0",
                            ),
                            href="https://www.atb-analytics-group.webflow.io",
                            style={"textDecoration": "none"},
                        ),
                        dbc.NavbarToggler(id="navbar-toggler2", n_clicks=0),
                        dbc.Collapse(
                            dbc.Nav(
                                [
                                    dbc.NavLink(f"{page['name']} ", href=page["relative_path"]) for page in
                                    dash.page_registry.values() if page["module"] != "pages.not_found_404"
                                ],
                                id='navigation',
                                className="ms-auto",
                                navbar=True,
                            ),
                            id="navbar-collapse2",
                            navbar=True,
                            # is_open=True,
                        ),
                    ],
                ),
                color=ATBDEFAULTTHEME.DIMGREY,
                dark=True,
                sticky='top',
                className="mb-5",
            ),
            2: dbc.Nav(
                id='navigation',
                children=[

                    dbc.NavLink(
                        children=[
                            html.I(
                                children=[],
                                className="fa-solid fa-home"
                            ),
                            "Home"],
                        href="/",
                        active="exact",
                    ),
                    dbc.NavLink(
                        [
                            html.I(
                                children=[],
                                className="fa-solid fa-house"
                            ), "Fundamental Analysis"
                        ], href="/pages/fundamentals",
                        active="exact"),
                    dbc.NavLink(
                        [
                            html.I(
                                children=[],
                                className="fa-solid fa-house"
                            ), "Technical Analysis"
                        ], href="/pages/technical",
                        active="exact"),
                ],
                pills=True,
                fill=True,
            ),
            3: dbc.Navbar(
                html.A(
                    # Use row and col to control vertical alignment of logo / brand
                    dbc.Row(
                        [
                            dbc.Col(html.Img(src=ATB_ANALYTICS_GRP_LOGO, height="30px"), width=4),
                            # dbc.Col(dbc.NavbarBrand("Navbar", className="ml-2")),
                            dbc.Col(nav, width=8),
                        ],
                        align="center",
                        # no_gutters=True,
                    ),
                    href="https://plotly.com",
                ),

            ),
        }

        if nav_selection > len(navbar_objs):
            logging.error(f"{nav_selection} greater than the navbar_objs has objects.({len(navbar_objs)})")

        # navbar_sticky = dbc.Navbar(
        #     dbc.Container(
        #         [
        #             html.A(
        #                 # Use row and col to control vertical alignment of logo / brand
        #                 dbc.Row(
        #                     [
        #                         dbc.Col(html.Img(src=ATB_ANALYTICS_GRP_LOGO, height="30px")),
        #                         dbc.Col(dbc.NavbarBrand("ATB Analytics Group", className="ms-2")),
        #                     ],
        #                     align="center",
        #                     className="g-0",
        #                 ),
        #                 href="https://www.atb-analytics-group.webflow.io",
        #                 style={"textDecoration": "none"},
        #             ),
        #             dbc.NavbarToggler(id="navbar-toggler2", n_clicks=0),
        #             dbc.Collapse(
        #                 dbc.Nav(
        #                     [
        #                         dbc.NavLink(f"{page['name']} ", href=page["relative_path"]) for page in
        #                         dash.page_registry.values() if page["module"] != "pages.not_found_404"
        #                     ],
        #                     id='navigation',
        #                     className="ms-auto",
        #                     navbar=True,
        #                 ),
        #                 id="navbar-collapse2",
        #                 navbar=True,
        #                 # is_open=True,
        #             ),
        #         ],
        #     ),
        #     color=ATBDEFAULTTHEME.DIMGREY,
        #     dark=True,
        #     sticky='top',
        #     className="mb-5",
        # )

        #
        # navbar = dbc.Navbar(
        #     html.A(
        #         # Use row and col to control vertical alignment of logo / brand
        #         dbc.Row(
        #             [
        #                 dbc.Col(html.Img(src=ATB_ANALYTICS_GRP_LOGO, height="30px"), width=4),
        #                 # dbc.Col(dbc.NavbarBrand("Navbar", className="ml-2")),
        #                 dbc.Col(nav, width=8),
        #             ],
        #             align="center",
        #             # no_gutters=True,
        #         ),
        #         href="https://plotly.com",
        #     ),
        #
        # ),

        return navbar_objs[nav_selection]

    '''
    Produces the sidebar that is  in every app(page) of the application and controls what the user see's.
    
    '''

    def get_sidebar(self, dataframe, page_stock_info_ids):
        if page_stock_info_ids == {}:
            page_stock_info_ids['stock-name'] = 'fundamentals-stock-name'
            page_stock_info_ids['stock-title'] = 'fundamentals-stock-title'
            page_stock_info_ids['stock-price'] = 'fundamentals-stock-price'
            page_stock_info_ids['stock-sector'] = 'fundamentals-stock-sector'
            page_stock_info_ids['stock-subsector'] = 'fundamentals-stock-subsector'

        sidebar = dbc.Row(
            children=[
                html.H4('Select a Stock'),
                html.Br(),
                html.P("Select a company from the list below, or enter a stock ticker into the search box."),
                html.Br(),
                dbc.Col(
                    [
                        dbc.Card(
                            className='mb-2 mt-2',
                            children=[
                                dbc.CardBody(
                                    className='pl-2 pr-2',
                                    children=[
                                        dbc.Row(
                                            [
                                                dbc.Col(
                                                    id="sb-stock-select-column",
                                                    # className='col-md-4',
                                                    children=[
                                                        dbc.Card(
                                                            className='mb-2 mt-2',
                                                            children=[
                                                                dbc.CardBody(
                                                                    className='pl-2 pr-2',
                                                                    children=[
                                                                        html.P(
                                                                            "Select a Company from the Dropdown below."),
                                                                        html.Br(),
                                                                        dcc.Dropdown(
                                                                            id='companies_dropdown',
                                                                            value='Company Ticker Symbol',
                                                                            options=[
                                                                                {'label': company, 'value': company} for
                                                                                company in
                                                                                sorted(dataframe.company.unique())
                                                                            ],
                                                                            optionHeight=35,
                                                                            searchable=True,
                                                                        ),
                                                                    ],
                                                                ),
                                                            ],
                                                        ),
                                                    ],
                                                    width=6,
                                                ),

                                                dbc.Col(
                                                    children=[
                                                        dbc.Card(
                                                            className='mb-2 mt-2',
                                                            children=[
                                                                dbc.CardBody(
                                                                    children=
                                                                    [
                                                                        html.P(
                                                                            "Enter the ticker symbol of the stock you wish to research"),
                                                                        html.Br(),
                                                                        dcc.Input(id="ticker_input", type="text",
                                                                                  className='ml-2 mr-4',
                                                                                  placeholder="Enter a Stock Ticker"),
                                                                        html.Button(
                                                                            ['Submit'],
                                                                            id='get_stock_btn',
                                                                            className='btn ml-2 p-2',
                                                                        ),
                                                                    ]
                                                                )
                                                            ]
                                                        )
                                                    ],
                                                    width=6
                                                )
                                            ]
                                        )
                                    ],
                                ),
                            ],
                        ),
                    ]
                ),

                # dbc.CardGroup(
                #     children=[
                #         dbc.Col(
                #             id="sb-stock-select-column",
                #             # className='col-md-4',
                #             children=[
                #                 dbc.Card(
                #                     className='mb-2 mt-2',
                #                     children=[
                #                         dbc.CardBody(
                #                             className='pl-2 pr-2',
                #                             children=[
                #                                 html.P("Select a Company from the Dropdown below."),
                #                                 html.Br(),
                #                                 dcc.Dropdown(
                #                                     id='companies_dropdown',
                #                                     value='Company Ticker Symbol',
                #                                     options=[
                #                                         {'label': company, 'value': company} for company in
                #                                         sorted(dataframe.company.unique())
                #                                     ],
                #                                     optionHeight=35,
                #                                     searchable=True,
                #                                 ),
                #                             ],
                #                         ),
                #                     ],
                #                 ),
                #             ],
                #             width=6,
                #         ),
                #
                #         dbc.Col(
                #             children=[
                #                 dbc.Card(
                #                     className='mb-2 mt-2',
                #                     children=[
                #                         dbc.CardBody(
                #                             children=
                #                             [
                #                                 html.P("Enter the ticker symbol of the stock you wish to research"),
                #                                 html.Br(),
                #                                 dcc.Input(id="ticker_input", type="text",
                #                                           placeholder="Enter a Stock Ticker"),
                #                                 html.Button(
                #                                     ['Submit'],
                #                                     id='get_stock_btn',
                #                                     className='btn ml-2 p-2',
                #                                 ),
                #                             ]
                #                         )
                #                     ]
                #                 )
                #             ],
                #             width=6
                #         )
                #     ]
                # ),

                # dbc.Col(
                #     id="sb-stock-info-column",
                #     # className='col-md-4',
                #     children=[
                #         dbc.Card(
                #             className='mb-2 mt-2 pl-2 pr-2',
                #             children=[
                #                 # dbc.CardImg(src="/static/images/placeholder286x180.png", top=True),
                #                 dbc.CardBody(
                #                     className='pl-2 pr-2',
                #                     children=[
                #                         html.H4(id=page_stock_info_ids['stock-name'], className='text-left', ),
                #                         # Company Name
                #                         html.H5(id=page_stock_info_ids['stock-title'], className='text-left', ),
                #                         # Stock symbol
                #                         html.H5(id=page_stock_info_ids['stock-price'], className='text-left', ),
                #                         html.Br(),
                #                         html.H6(id=page_stock_info_ids['stock-sector'], className='text-left', ),
                #                         html.H6(id=page_stock_info_ids['stock-subsector'], className='text-left', ),
                #
                #                         # dbc.Button("Go somewhere", color="primary"),
                #                         # dbc.CardLink("Card link", href="#"),
                #                         # dbc.CardLink("External link", href="https://google.com"),
                #
                #                     ],
                #                 ),
                #
                #             ],
                #         ),
                #     ],
                #     width=12,
                # ),

            ],
        ),

        return sidebar

    '''
    Generate a random stock from the list to populate the application with some data on initial load.
    
    :param: stock_symbols is a list of strings that contains the stocks ticker symbol.
    :returns: random stock in the list of stocks that were provided or the default stock symbols list as of Jun 2021
    '''

    def generate_random_stock(self, stock_symbols=None):
        if stock_symbols is None:
            stock_symbols = ['AAPL', 'VTI', 'TSCO', 'SQ', 'SBUX', 'BK', 'GOOG', 'DX', 'LMFA', 'ABCM', 'CHPT', 'BLNK',
                             'SPGI', 'VALU', 'YUM', 'AC', 'PINS', 'SNAP']
        if not stock_symbols:
            stock_symbols = stock_symbols

        stock = random.randrange(0, len(stock_symbols) - 1)
        stock_symbol = stock_symbols[stock]

        return stock_symbol

    '''
     Gets the Stock's company info from the database. 
    :param stock_symbol
    :returns company_df
    
    '''

    def get_company_info(self, stock_symbol):
        try:
            # Connect to database
            conn = db.DBConnection.create_connection(db.DBConnection.DB_FILE)

            # Getting record for company - If no record returned we create and get data.
            company_info_df = pd.read_sql_query(
                'SELECT symbol, id, company, gics_sector, gics_subsector, headquarters FROM stock WHERE stock.symbol="{}"'.format(
                    stock_symbol), conn)
            if company_info_df.empty:
                logging.info(
                    "{} company information is empty.{} needs to be added to our database.".format(stock_symbol,
                                                                                                   stock_symbol))
                raise Error

            return company_info_df, conn

        except Error as e:
            logging.error(e)
            return None

    '''
    Converts Timestamp column's to only be the year.
    :param: Pandas Dataframe Object containing the Data
    :param: inplace if you want the columns conversions to be done inplace.
    :returns: the Dataframe with the converted timestamps to year
    
    '''

    def convert_timestamp_columns(self, dataframe, inplace=True):
        for c in dataframe.columns:
            if type(c) == pd.Timestamp:
                year = c.year
                dataframe.rename(columns={c: str(year)}, inplace=True)
                # dataframe.reset_index()
            elif type(c) == int:
                year = c
                dataframe.rename(columns={c: str(year)}, inplace=True)
            else:
                pass

        logging.info(
            "Columns were converted from Timestamps to Strings and are of type\n{}\n".format(type(dataframe.columns)))

        return dataframe

    '''
    Convert Year column from Timestamp to int so that it can be used in downstream 
    fucnctions etc.
    
    Modifies the df in place. 
    '''

    def convert_ts_col_to_year(self, df, column_name):
        for i, val in enumerate(df[column_name]):
            if isinstance(val, pd.Timestamp):
                logging.info(f"Timestamp present at {i} with a value of {val}. Converting to int.{val.timestamp()}")
                df.at[i, column_name] = val.timestamp()

            if isinstance(val, str):
                logging.info(f"Timestamp in string format at {i} value of {val}. Converting to ts then int.")
                ts = pd.to_datetime(val)
                ts = ts.year
                df.at[i, column_name] = ts

        self.convert_timestamp_columns(self, df)

    '''
    Generating a generic html table
    
    :param: Pandas Dataframe Object containing the Data
    :param: max_rows is the max number of rows to show in the html table.
    :returns: html table with the max number of rows.
    '''

    def generate_html_table(self, dataframe, max_rows=10):
        return html.Table(className='twelve columns', children=[
            html.Thead(
                html.Tr([html.Th(col) for col in dataframe.columns])
            ),
            html.Tbody([
                html.Tr([
                    html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
                ]) for i in range(min(len(dataframe), max_rows))
            ])
        ])

    '''
    Generating a generic dash data table
    
    :param: Pandas Dataframe Object containing the Data
    :param: id is the id of choice for the table being created.
    :returns: Dash data table that has been formatted to for easier reading.
    '''

    def generate_generic_dash_datatable(self, dataframe, id, ):
        columns = [{"name": str(i), "id": str(i), 'type': 'numeric', 'format': FormatTemplate.money(2)} for i in
                   dataframe.columns]  # for when the column names can change

        return dash_table.DataTable(
            id=id,
            columns=columns,
            data=dataframe.to_dict('records'),
            # fixed_rows={'headers': True},
            # filter_action='native',
            row_selectable="multi",
            selected_rows=[],
            selected_columns=[],
            sort_action="native",
            sort_mode="multi",
            # page_size=pageSize,  # we have less data in this example, so setting to 20
            style_header={
                'backgroundColor': '#060606',
                'fontWeight': 'bold',
                'font-style': 'Montserrat',
            },

            style_data={'whiteSpace': 'normal', 'height': 'auto', 'backgroundColor': '#060606'},
            style_table={'height': '400px', 'overflowY': 'auto'},
            style_as_list_view=True,
        )

    '''
    Generating an Option dash data table that highlights in the money (ITM) calls/puts in Green,
    and out the money in Red.
    
    :param: Pandas Dataframe Object containing the Options Data for the security
    :param: id is the id of choice for the table being created.
    :returns: Dash data table that has been formatted to for easier reading.
    '''

    def generate_option_dash_datatable(self, dataframe, id, ):
        # columns = [{"name": i, "id": i} for i in dataframe.columns] # For when you do not know the column name of the df

        columns = [
            # {
            #     'id': 'contractSymbol',
            #     'name': 'contract',
            #     'type': 'text'
            # },
            # {
            #     'id': 'lastTradeDate',
            #     'name': 'last trade date',
            #     'type': 'datetime'
            # },
            {
                'id': 'strike',
                'name': 'strike',
                'type': 'numeric',
                'format': FormatTemplate.money(2)
            },
            {
                'id': 'lastPrice',
                'name': 'last price',
                'type': 'numeric',
                'format': FormatTemplate.money(2)
            }, {
                'id': 'bid',
                'name': 'bid',
                'type': 'numeric',
                'format': FormatTemplate.money(2)

            },
            {
                'id': 'ask',
                'name': 'ask',
                'type': 'numeric',
                'format': FormatTemplate.money(2)

            },
            {
                'id': 'change',
                'name': 'change',
                'type': 'numeric',
                'format': FormatTemplate.percentage(1).sign(Sign.positive)

            },
            {
                'id': 'percentChange',
                'name': 'percentChange',
                'type': 'numeric',
                'format': FormatTemplate.percentage(1).sign(Sign.positive)
            },
            {
                'id': 'volume',
                'name': 'volume',
                'type': 'numeric',
            },
            {
                'id': 'openInterest',
                'name': 'openInterest',
                'type': 'numeric',
            },
            {
                'id': 'impliedVolatility',
                'name': 'impliedVolatility',
                'type': 'numeric',
                'format': FormatTemplate.percentage(1).sign(Sign.positive)
            },
            {
                'id': 'inTheMoney',
                'name': 'inTheMoney',
            },
            # {'id': 'contractSize',
            #  'name': 'contractSize'
            #  },
            # {'id': 'currency',
            #  'name': 'currency'
            #  },

        ]

        return dash_table.DataTable(
            id=id,
            columns=columns,
            data=dataframe.to_dict('records'),
            fixed_rows={'headers': True},
            # filter_action='native',
            row_selectable="multi",
            selected_rows=[],
            selected_columns=[],
            sort_action="native",
            sort_mode="multi",
            # page_size=20,  # we have less data in this example, so setting to 20
            style_header={
                'backgroundColor': 'rgb(230, 230, 230)',
                'fontWeight': 'bold',
                'font-style': 'Montserrat',
            },
            css=[{'selector': 'tr:hover',
                  'rule': 'background-color:  yellow',
                  }],
            style_data_conditional=[
                {
                    'if': {
                        'filter_query': '{inTheMoney} contains ""',
                        # 'column_id': 'inTheMoney'
                    },
                    'backgroundColor': 'yellow',
                    'color': 'black'
                },
                {
                    'if': {
                        'filter_query': '{inTheMoney} contains "true"',
                        # 'column_id': 'inTheMoney'
                    },
                    'backgroundColor': ATBDEFAULTTHEME.AQUAMARINE,
                    'color': 'white'
                },
                {
                    'if': {
                        'filter_query': '{inTheMoney} contains "false"',
                        # 'column_id': 'inTheMoney'
                    },
                    'backgroundColor': ATBDEFAULTTHEME.ROSYBROWN,
                    'color': 'black'
                },

            ],

            style_data={'whiteSpace': 'normal', 'height': 'auto'},
            style_table={'height': '300px', 'overflowY': 'auto'},
            style_as_list_view=True,
        )

    '''
    Generating and returning a Plotly Dash Candlestick Graph for the Stock
    
    :param: Pandas dataframe object that contains price, date, close, open, high, low, and volume
    :returns: Plotly Dash Candlestick Graph Object
    
    '''

    def generate_candlestick_graph(self, dataframe, stock_symbol):
        candlestick_figure = make_subplots(specs=[[{'secondary_y': True}]])

        candlestick_layout = go.Layout(
            title='{} Price'.format(stock_symbol),
            barmode='overlay',
            autosize=True,
            xaxis={'range': [dataframe.date.min(), dataframe.date.max()]},
            yaxis={'range': [dataframe['adjusted_close'].min(), dataframe['adjusted_close'].max()]},
            yaxis2={'range': [dataframe['Volume'].min() - 1000, dataframe['Volume'].max() + 1000]},
            height=600,
            # paper_bgcolor="#000000",
            # plot_bgcolor="#000000",
            # font={
            #     'color': '#FFFFFF',
            # },
            # legend=dict(
            #     orientation="h",
            #     yanchor="bottom",
            #     y=1.02,
            #     xanchor="left",
            #     x=2
            # ),
            margin=dict(
                t=120,
                b=70,
                l=25,
                r=25
            )
        )

        price = go.Candlestick(x=dataframe['date'],
                               open=dataframe['Open'],
                               high=dataframe['High'],
                               low=dataframe['Low'],
                               close=dataframe['Close'],
                               name="{}".format(stock_symbol),
                               increasing_line_color=ATBDEFAULTTHEME.AQUAMARINE,
                               decreasing_line_color=ATBDEFAULTTHEME.ROSYBROWN,
                               )

        volume = go.Bar(x=dataframe.date, y=dataframe.Volume, name='Volume', opacity=.7,
                        marker_color=ATBDEFAULTTHEME.IVORY)

        # Adding the traces to the candlestick figure that will populate our graph mutli-plot graph Setting one of the traces
        # on the secondary axis to true allows for a nice multiplot
        candlestick_figure.add_trace(volume, secondary_y=True)
        candlestick_figure.add_trace(price, secondary_y=False)

        # QUERY Does this need to have the date in datetime format to work?
        candlestick_figure.update_xaxes(
            rangeslider_visible=False,
            rangeselector=dict(
                buttons=list([
                    dict(count=1, label="1d", step="day", stepmode="backward"),
                    dict(count=3, label="3d", step="day", stepmode="backward"),
                    dict(count=7, label="1W", step="day", stepmode="backward"),
                    dict(count=14, label="2W", step="day", stepmode="backward"),
                    dict(count=30, label="1M", step="day", stepmode="todate"),
                    dict(count=90, label="3M", step="day", stepmode="todate"),
                    dict(count=180, label="6M", step="day", stepmode="todate"),
                    dict(count=240, label="9M", step="day", stepmode="todate"),
                    dict(count=365, label='YTD', step='day', stepmode='backward'),
                    dict(step="all")
                ]),
                font_color="#000000",
                bgcolor="#c4c4c4",
                activecolor=ATBDEFAULTTHEME.LIGHTGOLDENROD,

            ),
            rangebreaks=[
                dict(bounds=["sat", "mon"]),  # Removes Weekends
                # dict(values=["2015-12-25", "2016-01-01"]),  #Use to Remove Holidays
            ])

        # Updating the candlestick figure layout with the most
        candlestick_figure.update_layout(candlestick_layout)

        return candlestick_figure

    '''
    Generating and returning a Plotly Dash Candlestick Graph with additional indicatiors for the Stock
    
    :param: Pandas dataframe object that contains price, date, close, open, high, low, and volume
    :returns: Plotly Dash Candlestick Graph Object
    
    '''

    def generate_candlestick_graph_w_indicators(self, dataframe, stock_symbol):
        candlestick_figure = make_subplots(specs=[[{'secondary_y': True}]])

        candlestick_layout = go.Layout(
            title=f'{stock_symbol} Price',
            barmode='overlay',
            autosize=True,
            xaxis={'range': [dataframe.date.min(), dataframe.date.max()]},
            yaxis={'range': [dataframe['Bollinger-Lower'].min() - 10, dataframe['Bollinger-Upper'].max() + 10]},
            yaxis2={'range': [dataframe['Volume'].min() - 1000, dataframe['Volume'].max() + 1000]},
            height=600,
            # paper_bgcolor="#000000",
            # plot_bgcolor="#000000",
            # font={
            #     'color': '#FFFFFF',
            # },
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=-.2,
                xanchor="left",
                x=0
            ),
            margin=dict(
                t=120,
                b=70,
                l=25,
                r=25,
            )
        )

        price = go.Candlestick(x=dataframe['date'],
                               open=dataframe['Open'],
                               high=dataframe['High'],
                               low=dataframe['Low'],
                               close=dataframe['Close'],
                               name="{}".format(stock_symbol),
                               increasing_line_color=ATBDEFAULTTHEME.AQUAMARINE,
                               decreasing_line_color=ATBDEFAULTTHEME.ROSYBROWN
                               )

        sell_line = go.Scatter(x=dataframe.date, y=dataframe['Bollinger-Upper'],
                               line=dict(color=ATBDEFAULTTHEME.AZURE, dash='solid'), opacity=.75,
                               name='BB Upper (Sell)', visible='legendonly')
        mid_line = go.Scatter(x=dataframe.date, y=dataframe['Bollinger-Middle'],
                              line=dict(color=ATBDEFAULTTHEME.GOLDENROD, dash='solid'), opacity=.75,
                              name='BB T3 EMA', visible='legendonly')
        buy_line = go.Scatter(x=dataframe.date, y=dataframe['Bollinger-Lower'],
                              line=dict(color=ATBDEFAULTTHEME.CADETBLUE, dash='solid'), opacity=.75,
                              name='BB Lower (Buy)', visible='legendonly')

        volume = go.Bar(x=dataframe.date, y=dataframe.Volume, name='Volume', opacity=.3,
                        marker_color=ATBDEFAULTTHEME.IVORY)

        MA200 = go.Scatter(x=dataframe['date'], y=dataframe['MA200'], name='200 MA',
                           line=dict(color=ATBDEFAULTTHEME.AZURE, ),
                           visible='legendonly')
        MA72 = go.Scatter(x=dataframe['date'], y=dataframe['MA72'], name='72 MA',
                          line=dict(color=ATBDEFAULTTHEME.CADETBLUE, ),
                          visible='legendonly')
        MA50 = go.Scatter(x=dataframe['date'], y=dataframe['MA50'], name='50 MA',
                          line=dict(color=ATBDEFAULTTHEME.LIGHTGOLDENROD, ),
                          visible='legendonly')

        # Adding the traces to the candlestick figure that will populate our graph mutli-plot graph Setting one of the
        # traces on the secondary axis to true allows for a nice multiplot
        candlestick_figure.add_trace(volume, secondary_y=True)
        candlestick_figure.add_trace(sell_line, secondary_y=False)
        candlestick_figure.add_trace(mid_line, secondary_y=False)
        candlestick_figure.add_trace(buy_line, secondary_y=False)
        candlestick_figure.add_trace(price, secondary_y=False)
        candlestick_figure.add_trace(MA200)
        candlestick_figure.add_trace(MA72)
        candlestick_figure.add_trace(MA50)

        # QUERY Does this need to have the date in datetime format to work?
        candlestick_figure.update_xaxes(
            rangeslider_visible=False,
            rangeselector=dict(
                buttons=list([
                    dict(count=1, label="1d", step="day", stepmode="backward"),
                    dict(count=3, label="3d", step="day", stepmode="backward"),
                    dict(count=7, label="1W", step="day", stepmode="backward"),
                    dict(count=14, label="2W", step="day", stepmode="backward"),
                    dict(count=30, label="1M", step="day", stepmode="todate"),
                    dict(count=90, label="3M", step="day", stepmode="todate"),
                    dict(count=180, label="6M", step="day", stepmode="todate"),
                    dict(count=240, label="9M", step="day", stepmode="todate"),
                    dict(count=365, label='YTD', step='day', stepmode='backward'),
                    dict(step="all")
                ]),
                font_color="#000000",
                bgcolor="#c4c4c4",
                activecolor=ATBDEFAULTTHEME.LIGHTGOLDENROD,

            ),
            rangebreaks=[
                dict(bounds=["sat", "mon"]),  # Removes Weekends
                # dict(values=["2015-12-25", "2016-01-01"]),  #Use to Remove Federal and Bank Holidays
            ])

        # Updating the candlestick figure layout with the most
        candlestick_figure.update_layout(candlestick_layout)

        return candlestick_figure

    def generate_scatter_graph(self, dataframe, x_column, y_column, secondary_y_column, title, upper_bound,
                               lower_bound):
        scatter_chart = make_subplots(specs=[[{'secondary_y': True}]])

        x_col_series = dataframe[x_column]
        y_col_series = dataframe[y_column]

        logging.info("X Column Max {}\nY Column Max {}".format(x_col_series.max(), y_col_series.max()))

        scatter = go.Scatter(x=dataframe[x_column], y=dataframe[y_column], name=str(y_column))
        scatter_layout = go.Layout(title=title,
                                   barmode='stack',
                                   autosize=True,
                                   xaxis={'range': [x_col_series.min(), x_col_series.max()]},
                                   yaxis={'range': [y_col_series.min(), y_col_series.max()]},
                                   height=400,
                                   # paper_bgcolor="#000000",
                                   # plot_bgcolor="#000000",
                                   # font={
                                   #     'color': '#FFFFFF',
                                   # }
                                   )

        scatter_chart.add_trace(scatter)

        if len(secondary_y_column) > 0:
            secondary_y_bar = go.Bar(x=dataframe[x_column], y=dataframe[secondary_y_column], name='Volume', opacity=.7,
                                     marker_color=ATBDEFAULTTHEME.DIMGREY)
            scatter_chart.add_trace(secondary_y_bar, secondary_y=True)

        if (0 < upper_bound <= y_col_series.max()) or (0 <= lower_bound < y_col_series.max()):
            scatter_chart.add_hline(y=lower_bound, line_color=ATBDEFAULTTHEME.AQUAMARINE, opacity=.5)
            scatter_chart.add_hline(y=upper_bound, line_color=ATBDEFAULTTHEME.ROSYBROWN, opacity=.5)

            scatter_chart.update_xaxes(
                rangeslider_visible=True,
                rangeselector=dict(
                    buttons=list([
                        dict(count=1, label="1d", step="day", stepmode="backward"),
                        dict(count=3, label="3d", step="day", stepmode="backward"),
                        dict(count=7, label="1W", step="day", stepmode="backward"),
                        dict(count=14, label="2W", step="day", stepmode="backward"),
                        dict(count=30, label="1M", step="day", stepmode="todate"),
                        dict(count=90, label="3M", step="day", stepmode="todate"),
                        dict(count=180, label="6M", step="day", stepmode="todate"),
                        dict(count=365, label='YTD', step='day', stepmode='backward'),
                        dict(step="all")
                    ]),
                    font_color="#000000",
                    bgcolor="#c4c4c4",
                    activecolor=ATBDEFAULTTHEME.LIGHTGOLDENROD,
                ),

                rangebreaks=[
                    dict(bounds=["sat", "mon"]),  # Removes Weekends
                    # dict(values=["2015-12-25", "2016-01-01"]),  #Use to Remove Federal and Bank Holidays
                ]
            )

            scatter_chart.update_layout(scatter_layout)

        return scatter_chart

    ''' 
    Generates a Plotly Dash line scatter Graph from a dataframe that is passed in, has the functionality for a secondary axis
     as well, will return the line scatter graph if dataframe is not empty
    
    :param: Pandas Dataframe Object
    :param: x_column is the column of interest to be placed along the x axis
    :param: y_column is the column of interest to be placed along the y axis
    :param: secondary_y_column is the secondary column of interest to be placed along the y axis (Optional)
    :param: title is the title of the Graph
    :param: upper_bound is way to place a line at an upper limit of a designated range. 
    :param: lower_bound is a way to place a line at a lower limit of the designated range.
    :returns: Plotly Scatter(line) Graph Object
    
    '''

    def generate_scatter_graph_no_bar(self, dataframe, x_column, y_column, secondary_y_column, title, upper_bound,
                                      lower_bound,
                                      candlestick=False):
        scatter_chart = make_subplots(specs=[[{'secondary_y': True}]])

        x_col_series = dataframe[x_column]
        y_col_series = dataframe[y_column]

        logging.info("X Column Max {}\nY Column Max {}".format(x_col_series.max(), y_col_series.max()))

        scatter = go.Scatter(x=dataframe[x_column], y=dataframe[y_column], name=str(y_column))
        scatter_layout = go.Layout(title=title,
                                   barmode='stack',
                                   autosize=True,
                                   xaxis={'range': [x_col_series.min(), x_col_series.max()]},
                                   yaxis={'range': [y_col_series.min(), y_col_series.max()]},
                                   height=400,
                                   # paper_bgcolor="#000000",
                                   # plot_bgcolor="#000000",
                                   # font={
                                   #     'color': '#FFFFFF',
                                   # }
                                   )

        scatter_chart.add_trace(scatter)

        if len(secondary_y_column) > 0:
            if candlestick:
                secondary_y_scatter = go.Candlestick(
                    x=dataframe['date'],
                    open=dataframe['Open'],
                    high=dataframe['High'],
                    low=dataframe['Low'],
                    close=dataframe['Close'],
                    name='Price',
                    increasing_line_color=ATBDEFAULTTHEME.AQUAMARINE,
                    decreasing_line_color=ATBDEFAULTTHEME.ROSYBROWN,
                )
            else:
                secondary_y_scatter = go.Scatter(x=dataframe[x_column], y=dataframe[secondary_y_column], name='Price',
                                                 opacity=.7,
                                                 marker_color=ATBDEFAULTTHEME.DARKSLATEGREEN)
            scatter_chart.add_trace(secondary_y_scatter, secondary_y=True)

        if (0 < upper_bound <= y_col_series.max()) or (0 <= lower_bound < y_col_series.max()):
            scatter_chart.add_hline(y=lower_bound, line_color=ATBDEFAULTTHEME.AQUAMARINE, opacity=.5)
            scatter_chart.add_hline(y=upper_bound, line_color=ATBDEFAULTTHEME.ROSYBROWN, opacity=.5)

            scatter_chart.update_xaxes(
                rangeslider_visible=True,
                rangeselector=dict(
                    buttons=list([
                        dict(count=1, label="1d", step="day", stepmode="backward"),
                        dict(count=3, label="3d", step="day", stepmode="backward"),
                        dict(count=7, label="1W", step="day", stepmode="backward"),
                        dict(count=14, label="2W", step="day", stepmode="backward"),
                        dict(count=30, label="1M", step="day", stepmode="todate"),
                        dict(count=90, label="3M", step="day", stepmode="todate"),
                        dict(count=180, label="6M", step="day", stepmode="todate"),
                        dict(count=365, label='YTD', step='day', stepmode='backward'),
                        dict(step="all")
                    ]),
                    font_color="#000000",
                    bgcolor="#c4c4c4",
                    activecolor=ATBDEFAULTTHEME.LIGHTGOLDENROD,
                ),

                rangebreaks=[
                    dict(bounds=["sat", "mon"]),  # Removes Weekends
                    # dict(values=["2015-12-25", "2016-01-01"]),  #Use to Remove Holidays
                ]
            )

            scatter_chart.update_layout(scatter_layout)

        return scatter_chart

    # TODO ALLOW THE BARS(COLUMNS OF COMPARISONIAL INTEREST TO BE PASSED IN AS AN LIST, SAME WITH COLORS FOR THOSE TO COLUMNS

    ''' 
    
    Generates a Dash Bar Graph from a dataframe that is passed in will return the bar graph if dataframe is not empty
    
    :param: Pandas Dataframe Object
    :returns: Plotly Bar Graph Object
    
    '''

    # Generate Heatmap
    def generate_heatmap(self, dataframe, title, x_column, y_column, z_values):
        heatmap_figure = make_subplots(specs=[[{'secondary_y': True}]])

        x_col_series = dataframe[x_column]
        y_col_series = dataframe[y_column]

        logging.info("X Column Max {}\nY Column Max {}".format(x_col_series.max(), y_col_series.max()))

        heatmap_layout = go.Layout(
            title=title,
            autosize=True,
            xaxis={'range': [x_col_series.min(), x_col_series.max()]},
            yaxis={'range': [y_col_series.min(), y_col_series.max()]},
            height=400,
            # paper_bgcolor="#000000",
            # plot_bgcolor="#000000",
            # font={
            #     'color': '#FFFFFF',
            # },
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=-.5,
                xanchor="left",
                x=0
            ),

            margin=dict(
                t=5,
                b=5,
                l=5,
                r=5,
            ),
        )

        heatmap_graph = go.Heatmap(
            z=dataframe[z_values],
            x=dataframe[x_column],
            y=dataframe[y_column]
        )

        heatmap_figure.add_traces(heatmap_graph)
        heatmap_figure.update_layout(heatmap_layout)
        return heatmap_figure

    def generate_bar_graph(self, dataframe, title, x_column, y_column, secondary_y_column=None, upper_bound=None,
                           lower_bound=None):
        bar_figure = make_subplots(specs=[[{'secondary_y': True}]])

        x_col_series = dataframe[x_column]
        y_col_series = dataframe[y_column]

        logging.info("X Column Max {}\nY Column Max {}".format(x_col_series.max(), y_col_series.max()))

        bar_layout = go.Layout(title=title,
                               barmode='group',
                               autosize=True,
                               xaxis={'range': [x_col_series.min(), x_col_series.max()]},
                               yaxis={'range': [y_col_series.min(), y_col_series.max()]},
                               height=400,
                               # paper_bgcolor="#000000",
                               # plot_bgcolor="#000000",
                               # font={
                               #     'color': '#FFFFFF',
                               # },
                               legend=dict(
                                   orientation="v",
                                   yanchor="bottom",
                                   y=-.5,
                                   xanchor="left",
                                   x=0
                               ),

                               margin=dict(
                                   t=5,
                                   b=5,
                                   l=5,
                                   r=5,
                               ),
                               )
        profit_graph = go.Bar(x=dataframe[x_column], y=dataframe[y_column], name=str(y_column), opacity=.7,
                              marker_color='#d6c79f')
        operating_graph = go.Bar(x=dataframe[x_column], y=dataframe['Operating Margin'], name=str('Operating Margin'),
                                 opacity=.8, marker_color='#E4F2EF')
        gross_graph = go.Bar(x=dataframe[x_column], y=dataframe['Gross Margin'], name=str('Gross Margin'), opacity=.9,
                             marker_color='#cfa42f')

        bar_figure.add_traces(profit_graph)
        bar_figure.add_traces(operating_graph)
        bar_figure.add_traces(gross_graph)

        bar_figure.update_xaxes(
            {'range': [x_col_series.min(), x_col_series.max()]},
            categoryorder='category ascending',
            automargin=True,
        )
        bar_figure.update_layout(bar_layout)

        return bar_figure

    def generate_bar_and_line_graph(self, df1, df2, title, x_column, y_column, secondary_y_column=None,
                                    upper_bound=None,
                                    lower_bound=None):
        bar_figure = make_subplots(specs=[[{'secondary_y': True}]])

        x_col_series = df1[x_column]
        y_col_series = df1[y_column]

        bar_layout = go.Layout(
            title=title,
            barmode='group',
            autosize=True,
            xaxis={'range': [x_col_series.min(), x_col_series.max()]},
            yaxis={'range': [y_col_series.min(), y_col_series.max()]},
            height=400,
            # paper_bgcolor="#000000",
            # plot_bgcolor="#000000",
            # font={
            #     'color': '#FFFFFF',
            # },
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=-.5,
                xanchor="left",
                x=0
            ),

            margin=dict(
                t=5,
                b=5,
                l=5,
                r=5,
            ),
        )

        # Profit Margin
        profit_graph = go.Bar(
            x=df1[x_column], y=df1[y_column], name=str(y_column), opacity=.7,
            marker_color='#9BCEB5'
        )
        industry_profit_graph = go.Scatter(x=df2[x_column], y=df2[y_column], name=str("Industry" + y_column),
                                           opacity=.7,
                                           marker_color='#9BCEB5')

        # Operating Margin
        operating_graph = go.Bar(x=df1[x_column], y=df1['Operating Margin'], name=str('Operating Margin'),
                                 opacity=.8, marker_color='#709784')
        industry_operating_graph = go.Scatter(x=df2[x_column], y=df2['Operating Margin'],
                                              name=str('Industry Operating Margin'),
                                              opacity=.8, marker_color='#709784')
        # Gross Marign
        gross_graph = go.Bar(x=df1[x_column], y=df1['Gross Margin'], name=str('Gross Margin'), opacity=.9,
                             marker_color='#E4F2EF')
        industry_gross_graph = go.Scatter(x=df2[x_column], y=df2['Gross Margin'], name=str('Industry Gross Margin'),
                                          opacity=.9,
                                          marker_color='#E4F2EF')

        bar_figure.add_traces(profit_graph)
        bar_figure.add_traces(industry_profit_graph)

        bar_figure.add_traces(operating_graph)
        bar_figure.add_traces(industry_operating_graph)

        bar_figure.add_traces(gross_graph)
        bar_figure.add_traces(industry_gross_graph)

        bar_figure.update_xaxes(
            {'range': [x_col_series.min(), x_col_series.max()]},
            categoryorder='category ascending',
            automargin=True,
        )
        bar_figure.update_layout(bar_layout)

        return bar_figure

    # Generating the Buttons (Options Expiration dates for the security) for the button group.
    def generate_btn_grp_buttons(self, exDate, stock_symbol=None):
        if stock_symbol is not None:
            return dbc.Button(children=str(exDate),
                              color="primary",
                              className="mr-2 ml-2",
                              id=stock_symbol + "-" + str(exDate),
                              value=str(exDate),
                              )

        else:
            return dbc.Button(children=str(exDate),
                              color="secondary",
                              className="mr-2 ml-2",
                              id=str(exDate),
                              value=str(exDate),
                              )

    # create a "Master Financials Table" overview using the Financials, BalanceSheet, Cashflows, Earnings
    # Note Earnings will have to be transposed
    def generate_master_financials(self, financials, balanceSheet, cashflows, earnings):
        # Transposing the rows and columns for the earnings reports.
        if 'Year' in earnings.columns or 'year' in earnings.columns:
            earnings.set_index('Year', inplace=True)
            earnings = earnings.transpose()
            # earnings_cols = earnings['Year'].transpose()
            # earnings.drop(columns=['Year'], inplace=True)
            # earnings = earnings.transpose()
            # earnings.rename(columns=earnings_cols, inplace=True)
            pass
        elif 'Earnings' in earnings.index or 'earnings' in earnings.index:
            earnings.rename({'earnings': 'Earnings', 'revenue': 'Revenue'})
            pass
        else:
            earnings = earnings.transpose()

        if len(earnings.columns[earnings.columns.duplicated()]) > 0:
            logging.info(f'Duplicate Column names in the earnings column')
            earnings = earnings.groupby(earnings.columns.str, axis=1).agg(
                lambda x: x.join(str(v) for v in x if pd.notnull(v)))

        # converting the years into the same format as the other financial mm/yyyy format
        for c in earnings.columns:
            # Checking for timestamp objects. Might need to check for DateTime Objects as well.
            if type(c) is pd.Timestamp:
                year = str(c.year)
            else:
                year = str(c)
            earnings.rename(columns={c: "{}".format(year)}, inplace=True)

        master_financials_df = pd.DataFrame._append(financials, balanceSheet, )
        master_financials_df = pd.DataFrame._append(master_financials_df, cashflows, )
        master_financials_df = self.convert_timestamp_columns(self, master_financials_df)
        master_financials_df = pd.DataFrame._append(master_financials_df, earnings, )

        master_financials_df.index.rename('Financials', inplace=True)
        master_financials_df.reset_index(inplace=True)
        return master_financials_df
        pass

    def generate_opt_btn_list(self, options, stockSymbol):
        options_list = []
        for exDate in options['option_dates']:
            options_list.append(stockSymbol + "-" + str(exDate))

        return options_list

    '''
    Creates the MACD graph
    :param
    
    '''

    def generate_macd_chart(self, dataframe):
        macd_figure = go.Figure()

        macd_layout = go.Layout(
            title='MACD (Moving Average Convergence-Divergence)',
            barmode='stack',
            autosize=True,
            # paper_bgcolor="#000000",
            # plot_bgcolor="#000000",
            # font={
            #     'color': '#FFFFFF',
            # },
            # xaxis={'range': [x_col_series.min(), x_col_series.max()]},
            # yaxis={'range': [y_col_series.min(), y_col_series.max()]},
            # title='MACD (Moving Average Convergence-Divergence',
            # xaxis_tickfont_size=14,
            # yaxis=dict(
            #     title='USD (millions)',
            #     titlefont_size=16,
            #     tickfont_size=14,
            # ),
            height=600
        )

        macd_figure.add_trace(
            go.Bar(
                x=dataframe['date'],
                y=dataframe['macd_hist'],
                name='MACD-HIST',
                opacity=.7,
                marker_color='#388895',
            ),
        )

        macd_figure.add_trace(
            go.Scatter(
                x=dataframe['date'],
                y=dataframe['macd_signal'],
                name='MACD-SIGNAL-LINE',
                opacity=.7
            ))

        macd_figure.add_trace(
            go.Scatter(
                x=dataframe['date'],
                y=dataframe['macd'],
                name='MACD',
                opacity=.7
            ),
        )

        macd_figure.add_trace(
            go.Scatter(
                x=['date'],
                y=['200MA'],
                name='200MA',
                marker_color='#9BCEB5',
            ),
        )

        macd_figure.update_layout(macd_layout)

        macd_figure.update_xaxes(
            rangeslider_visible=True,
            rangeselector=dict(
                buttons=list([
                    dict(count=1, label="1d", step="day", stepmode="backward"),
                    dict(count=3, label="3d", step="day", stepmode="backward"),
                    dict(count=7, label="1W", step="day", stepmode="backward"),
                    dict(count=14, label="2W", step="day", stepmode="backward"),
                    dict(count=30, label="1M", step="day", stepmode="todate"),
                    dict(count=90, label="3M", step="day", stepmode="todate"),
                    dict(count=180, label="6M", step="day", stepmode="todate"),
                    dict(count=365, label='YTD', step='day', stepmode='backward'),
                    dict(step="all", label='ALL')
                ]),
                font_color="#000000",
                bgcolor="#c4c4c4",
                activecolor="lightgoldenrodyellow",
            )
        )

        return macd_figure

    '''
    On Balance Volume Chart
    :param Dataframe 
    
    '''

    '''
    The functions below are from 
    Derek Banas 
    https://github.com/derekbanas/Python4Finance/blob/main/Python%20for%20Finance%203.ipynb
    '''

    '''
    Get the ROI for a stock between two dates.
    
    :param Dataframe
    :param sdate start date
    :param edate end date
    returns ROI
    
    '''

    def roi_between_dates(self, dataframe, sdate, edate):
        try:
            # Gets the Adj Close price for 1st & last date
            start_val = dataframe.loc[sdate, 'adjusted_close']
            end_val = dataframe.loc[edate, 'adjusted_close']
            roi = ((end_val - start_val) / start_val)
        except Exception:
            logging.error("Data Corrupted")
        else:
            return roi

    def roi_between_dates_df(self, dataframe, company, sdate, edate):
        # Checking and removing any duplicate values in our dateframe on the date values.
        # dataframe.drop_duplicates(subset=['date'], inplace=True)

        try:
            # Gets the Adj Close price for 1st & last date
            start_val = dataframe[(dataframe['company'] == company)][(dataframe['date'] == sdate)][
                'adjusted_close'].item()
            end_val = dataframe[(dataframe['company'] == company)][(dataframe['date'] == edate)][
                'adjusted_close'].item()
            roi = ((end_val - start_val) / start_val) * 100
            logging.info("{}'s total roi for the period ({}, {}) is  {}".format(company, sdate, edate, roi))
        except Exception:
            logging.error("Data Corrupted\n{}".format(Exception))
        else:
            return roi

    '''
    add the daily ROI for a stock between two dates.
    
    :param Dataframe
    :returns Dataframe with ROI added to it
    
    '''

    def add_daily_return_to_df(self, dataframe):
        dataframe['daily_return'] = (dataframe['adjusted_close'] / dataframe['adjusted_close'].shift(1)) - 1
        return dataframe

    '''
    
    Check whether the column is in the Dataframe or not.
    
    :param Dataframe
    :returns boolean to answer if dataframe is present or not 
    
    '''

    def checkForColinDF(self, df, col_name):
        ans = False
        if df is not None:
            if col_name in df.index:
                ans = True
                return ans
            else:
                return ans
        else:
            return ans

    ''' 
        Opens and reads the SQL file line by line.
    '''

    def open_and_read_sql(self, filename=None):

        if os.path.exists(filename):
            f = open(filename, 'r')
            read_sql_file = f.read()
            f.close()

        return read_sql_file

    '''
    
        Preps and checks that the dataframe is producing the proper information and is removing 
        standard columns among table groups. 
        
        :param df - dataframe
        :param qry - either path to sql file to read data from table in database
        :param table_name table name to search in the database
    
    '''

    def prep_df_for_db_insert(self, qry_str, stock_id, col_check, drop_cols, conn):
        QRY = self.open_and_read_sql(self, qry_str)
        logging.info(f"Prepping the database with the following query\n{QRY}")
        ids_to_check = [stock_id]  # if using the same id multiple time
        id_string = ', '.join(str(id) for id in ids_to_check)
        df = pd.read_sql_query(text(QRY.format(id_string, id_string)), conn)
        logging.info(f"Data Received from QRY\n{df}")

        if df[col_check][0] is not None:
            df.drop(columns=drop_cols, inplace=True)

            if col_check == 'Year':
                self.convert_ts_col_to_year(self, df, col_check)
                df.drop_duplicates(inplace=True)
                df.set_index('Year', inplace=True)

                if df.index.name == 'Year':
                    logging.info(f"{col_check} column is a string. need to convert to int")
                    self.convert_timestamp_columns(self, df)

            else:
                df.set_index('year', inplace=True)

            df.sort_index(ascending=False, inplace=True)
            df = df.transpose()

        return df

    ''' 
        Returns a loading wrapped component can be a single component or a group of nested components
    '''

    def loading_wrapper(self, component, id=''):
        random_color = [
            ATBDEFAULTTHEME.AQUAMARINE,
            ATBDEFAULTTHEME.CADETBLUE,
            ATBDEFAULTTHEME.GOLDENROD,
            ATBDEFAULTTHEME.AZURE,
            ATBDEFAULTTHEME.AQUAMARINE,
        ]
        rand = random.randrange(0, len(random_color) - 1)

        return dcc.Loading(
            id=id,
            children=[
                component
            ],
            type='circle',
            color=random_color[rand]
        )

    ''' 
        Gets random color from array or from Colorways defined in the py file. 
    '''

    def get_random_color(self):
        random_color = ATBDEFAULTTHEME.dark_colorway_all
        #     [
        #     ATBDEFAULTTHEME.AQUAMARINE,
        #     ATBDEFAULTTHEME.CADETBLUE,
        #     ATBDEFAULTTHEME.GOLDENROD,
        #     ATBDEFAULTTHEME.AZURE,
        #     ATBDEFAULTTHEME.AQUAMARINE,
        # ]
        rand = random.randrange(0, len(random_color) - 1)

        random_color_choice = random_color[rand]

        return random_color_choice

    '''
        Checks that the columns in two dataframes are the same, and creates a third dataframe out of the 
        columns that are not the same.
        
        :param df1 is the database table columns that we are trying to insert into
        :param df2 is the API data that is trying to be inserted into the table.
    '''

    def check_dfs_same_cols(self, df1, df2):
        # Get columns from both dataframes
        first_columns = set(df1.columns)  # should be the database columns
        second_columns = set(df2.columns)

        # Find columns in the second dataframe that are not in the first
        missing_columns = second_columns - first_columns

        # Create a new dataframe with only the missing columns from the second dataframe
        missing_columns_df = df2[list(missing_columns)]

        return missing_columns_df

    '''
    :param sales growth is either a list of floats or a float value
    :param inflation rate  is either a list of floats or a float value 
    :param init_revenue = 1  is the revenue value at the start of the period 
    :param run_scenario = False if true will return a pd df for the sales growth, inflation rates and revenue.
    '''

    def forcast_sales_revenue(self, sales_growth, inflation_rate, init_revenue=1, run_scenario=False):
        if sales_growth is None:
            # Low, Base, High Sales Growth
            sales_growth = [0.05, 0.1, 0.15]

        if inflation_rate is None:
            # Low, Base, High Inflation
            inflation_rate = [0.02, 0.03, 0.04]

        # revenue = initial_revenue * (1 + sales_growth) / (1 + inflation_rate)
        revenue = init_revenue * (1 + sales_growth) / (1 + inflation_rate)

        if run_scenario:
            scenario_results = []
            for sg in sales_growth:
                for ir in inflation_rate:
                    revenue = init_revenue * (1 + sg) / (1 + ir)
                    scenario_results.append({'Sales_Growth': sg, 'Inflation_Rate': ir, 'Revenue': revenue})

            scenario_df = pd.DataFrame(scenario_results)
            return scenario_df
        else:
            return revenue

    def monte_carlo_sim(self, no_of_sims, p1, p2, b1, b2):

        if no_of_sims != 0 or no_of_sims is None:
            no_of_sims = 1000000
        logging.info(f"Starting Monte Carlo Simulation with a {no_of_sims} simulation run with {p1},{p2},{b1},{b2}")
        P = np.random.uniform(p1, p2, no_of_sims)
        B = np.random.uniform(b1, b2, no_of_sims)

        duration = P + B
        logging.info(f"{P}\n{B}\n{duration}")

        return duration



    # Example usage
    # log_file_path = 'example.log'
    # search_words = ['Error', 'Exception']
    # email_sender = 'sender@example.com'
    # email_recipient = 'recipient@example.com'
    # smtp_server = 'smtp.example.com'
    # smtp_port = 587
    # smtp_username = 'your_username'
    # smtp_password = 'your_password'

    def parse_log_file_and_send_email(self,log_file_path, search_words, email_sender, email_recipient, smtp_server,
                                      smtp_port, smtp_username, smtp_password):
        try:
            # Open the log file
            with open(log_file_path, 'r') as file:
                log_content = file.read()

            # Initialize a list to store found errors
            errors = []

            # Search for the specified words in the log content
            for word in search_words:
                errors.extend(re.findall(r'\b' + word + r'\b', log_content, flags=re.IGNORECASE))

            # Send email for each error found
            if errors:
                for error in errors:
                    subject = f"Error occurred: {error}"
                    body = f"Error details:\n{error}\n\nLog file: {log_file_path}"

                    # Create the email message
                    msg = MIMEMultipart()
                    msg['From'] = email_sender
                    msg['To'] = email_recipient
                    msg['Subject'] = subject
                    msg.attach(MIMEText(body, 'plain'))

                    # Attach the log file
                    attachment = MIMEBase('application', 'octet-stream')
                    with open(log_file_path, 'rb') as file:
                        attachment.set_payload(file.read())
                    encoders.encode_base64(attachment)
                    attachment.add_header('Content-Disposition',
                                          f'attachment; filename="{os.path.basename(log_file_path)}"')
                    msg.attach(attachment)

                    # Connect to SMTP server and send email
                    with smtplib.SMTP(smtp_server, smtp_port) as server:
                        server.starttls()
                        server.login(smtp_username, smtp_password)
                        server.sendmail(email_sender, email_recipient, msg.as_string())

            else:
                print("No errors found in the log file.")

        except FileNotFoundError:
            print("Log file not found.")

        except Exception as e:
            print(f"An error occurred: {e}")



