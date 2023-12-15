'''
Homepage

------------------------------------------------------------------------------
Program Description
-------------------------------------------------------------------------------

Homepage of the Stock Screening Application, will show mainly the market
information to get familiar with the current landscape, and then allow for
some quick and dirty type analysis to drive you towards either choosing a
stock from the list, entering a ticker symbol and then either navigating to
fundamental or technical analysis to learn more about that particular stock.

----------------------------------------------------------------------------------

'''
from sqlite3 import Error
import logging
import dash

import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import talib
from dash.dependencies import Input, Output
from dash import callback

from plotly import graph_objects as go
from plotly.subplots import make_subplots

# import app
import db
from utils import Utils as utils
from stock import MyStock

import assets.candlestickPattens as cp
import assets.templates.atbanalyticsgrp_dark as ATBDEFAULTTHEME

# Interacts with the Database
dbObj = db.DBConnection()

# Interacts with the yFinance API
StockObj = MyStock()
conn = None

# Connect to DB and  Load Data
DB_FILE = db.DB_FILE

try:
    conn = dbObj.create_connection(db_file=DB_FILE)
    logging.info("Successfully Connected to the DB from Homepage.")
    # stock_price_df = pd.read_sql('SELECT * FROM stock_price, stock WHERE stock_id= stock.id', conn)
except Error as e:
    logging.error(f"Error Occurred when trying to connect to the database |{e}")

companies_df = dbObj.select_table_data(conn=conn, table_name='stock')
patternsDict = cp.candlestick_patterns
stock, pattern = None, None

page_stock_info_ids = {}
page_stock_info_ids['stock-name'] = 'home-stock-name'
page_stock_info_ids['stock-title'] = 'home-stock-title'
page_stock_info_ids['stock-price'] = 'home-stock-price'
page_stock_info_ids['stock-sector'] = 'home-stock-sector'
page_stock_info_ids['stock-subsector'] = 'home-stock-subsector'

'''

Creating the card that holds the pricing chart of the stock that matches the 
patten that was selected from the dropdown.

:param: pattern - String
:param: stock - String
:returns: Card Containing Price Chart of Matching Stock

'''


def create_pattern_chart_card(pattern, stock, data):
    fig = utils.generate_candlestick_graph(data, stock + "-" + pattern)
    fig.update_layout(showlegend=False)

    patternChartCard = dcc.Graph(
        id=stock + "_" + pattern,
        animate=True,
        figure=fig,
    )
    return patternChartCard


# Registering the Dash Page
dash.register_page(__name__,
                   path='/',
                   name='Home',
                   title='Stock Screener - Home - ATB Analytics Group',
                   description='Stock Screener Homepage'
                   )


def serve_layout():
    return html.Div(
        children=[
            dcc.Interval(id='page-load-count', ),
            # App Instructions
            dbc.Row([
                # dbc.Col(
                #     children=[
                #         html.Div(
                #             [
                #                 html.H1(
                #                     children=[
                #                         "Simple Screener",
                #                     ],
                #                     className='display-1',
                #                 ),
                #                 dbc.Col(children=[
                #                     html.Img(
                #                         src='./assets/img/oren-elbaz-Wf1opKy4iaI-unsplash.jpg',
                #                         id='header-img',
                #                         className='img img-responsive',
                #                         width='100%',
                #                         height='30%',
                #                     ),
                #                 ],
                #                     width=6
                #                 ),
                #                 dbc.Col(children=[
                #                     html.H3("Keeping it simple when it comes to screening stocks."),
                #
                #                     html.Br(),
                #                     html.P("How to use the App"),
                #
                #                     html.Ul(
                #                         id='app-instruction-list',
                #                         children=[
                #                             html.Li(
                #                                 """Check out the Market Analysis Heatmap to see the current market
                #                                 returns, or select a specific market of interest to view the data. """
                #                             ),
                #                             html.Li(
                #                                 "Select a Candlestick pattern from the dropdown to populate a list"
                #                                 "of price graphs that match that pattern."),
                #                             html.Li(
                #                                 "Select the stock that you want to see more information on from the "
                #                                 "Dropdown and choose which analysis you would like to see."),
                #                             # html.Li("Choose the Analysis you wish to start with.You can flip between the "
                #                             #         "fundamental and technical analysis tabs without"),
                #                         ]
                #                     )
                #                 ],
                #                     width=6
                #                 ),
                #
                #                 html.Br(),
                #
                #             ],
                #             style={
                #                 'min-height': '20vh',
                #             },
                #             id='app-instructions-wrapper',
                #             className='mb-2 p-5'
                #         ),

                    # ],
                    # width=12
                # ),
                    dbc.Col(children=[
                        html.Img(
                            src='./assets/img/oren-elbaz-Wf1opKy4iaI-unsplash.jpg',
                            id='header-img',
                            className='img img-responsive',
                            width='100%',
                            height='30%',
                        ),
                    ],
                        width=6
                    ),
                    dbc.Col(children=[
                        html.H1(
                            children=[
                                "Simple Screener",
                            ],
                            className='display-1',
                        ),
                        html.H3("Keeping it simple when it comes to screening stocks."),

                        html.Br(),
                        html.P("How to use the App"),

                        html.Ul(
                            id='app-instruction-list',
                            children=[
                                html.Li(
                                    """Check out the Market Analysis Heatmap to see the current market 
                                    returns, or select a specific market of interest to view the data. """
                                ),
                                html.Li(
                                    "Select a Candlestick pattern from the dropdown to populate a list"
                                    "of price graphs that match that pattern."),
                                html.Li(
                                    "Select the stock that you want to see more information on from the "
                                    "Dropdown and choose which analysis you would like to see."),
                                # html.Li("Choose the Analysis you wish to start with.You can flip between the "
                                #         "fundamental and technical analysis tabs without"),
                            ]
                        )
                    ],
                        width=6
                    ),

                    html.Br(),


            ]),
            html.Br(),

            # Heatmaps and Market Analysis
            dbc.Row([
                html.Div(
                    children=
                    [
                        html.H2("Market Analysis"),
                        html.P(
                            """
    
                            Current year returns by sector and by security for a sector.
                            This can be used to identify hot sectors and/or securities.
    
                            """
                        ),
                        html.Hr(),
                    ],
                    id='market-analysis info wrapper',
                    className='mb-2 p-5'
                ),
                html.Br(),
                dbc.Col(
                    [
                        html.P(
                            """
                            Select a sector 
                            """
                        ),
                        dcc.Dropdown(
                            id='heatmap-sector-dropdown',
                            options=[{'label': i, 'value': i} for i in companies_df.gics_sector.unique()],
                            placeholder='Select a Sector',
                        ),

                    ],
                    width=12,
                    align='center',
                ),
                html.Br(),
                dbc.Col(
                    children=[
                        html.Div(
                            children=[
                                utils.loading_wrapper(
                                    utils,
                                    dbc.Card(
                                        className="card",
                                        children=[
                                            html.Div(),
                                            dbc.CardBody(
                                                children=[
                                                    html.H2("Sector Returns"),
                                                    html.Br(),
                                                    html.Div(
                                                        id='sector-margins-chart',
                                                        # type="circle",
                                                        # color=ATBDEFAULTTHEME.AQUAMARINE
                                                    ),
                                                ]),
                                        ],
                                        style={
                                            'width': '100%',
                                            # 'height': '25vh',
                                        }
                                    ),
                                )

                            ]
                        ),

                    ],
                    align='center',
                    width=6,
                ),

                html.Br(),
                dbc.Col(
                    children=[
                        html.Div(
                            children=[
                                utils.loading_wrapper(
                                    utils,
                                    dbc.Card(
                                        className="card",
                                        children=[

                                            dbc.CardBody(
                                                children=[
                                                    html.H2("Top Security Returns"),
                                                    html.Br(),
                                                    html.Div(
                                                        id='stock-rois-chart',
                                                        # type="circle",
                                                        # color=ATBDEFAULTTHEME.AZURE
                                                    ),
                                                ]),
                                        ],
                                        style={
                                            'width': '100%',
                                            # 'height': '25vh',
                                        }
                                    ),
                                )
                            ]
                        )
                    ],
                    align='center',
                    width=6,
                )
            ],
                className='mb-2 p-5'
            ),

            html.Br(),
            # Candlestick Patterns Selection Row
            dbc.Row(
                children=[
                dbc.Col(
                    [
                    html.H2("Candlestick Patterns"),
                    html.P(
                            """
                            A daily candlestick represents a market’s opening, high, low, and closing (OHLC) prices. The 
                            rectangular real body, or just body, is colored with a dark color (red or black) for a drop in 
                            price and a light color (green or white) for a price increase. 
                            """
                    ),
                    html.Br(),
                        html.Div(
                            children=[

                                html.P(
                                    """
                                    The lines above and below the body 
                                    are referred to as wicks or tails, and they represent the day’s maximum high and low. 
                                    Taken together, the parts of the candlestick can frequently signal changes in a market’s direction 
                                    or highlight significant potential moves that frequently must be confirmed by the next day’s candle.
                                    """
                                ),
                                html.Br(),
                                html.P(
                                    """
                                    Common patterns include things like Doji and Spinning Top, Bullish/Bearish Engulfing Lines,
                                 Hammers, Hanging Men and many others, but the key thing to remember is that these patterns
                                        can help in identify short-to-medium directions and momentum's of certain stocks or industries.
                                    """
                                ),
                            ],
                            id='cs-pattern-info-wrapper',
                            className='mb-2 p-5',
                        ),
                    html.Br()
                    ],
                    width=6,
                ),
                dbc.Col(
                    children=[
                        html.Img(
                            src='./assets/img/jason-briscoe-amLfrL8LGls-unsplash.jpg',
                            # id='header-img',
                            className='img img-responsive',
                            width='100%',
                            height='30%'
                        ),

                    ],
                    width=6
                ),
                html.Br(),
                html.Hr(),
                dbc.Col(
                    children=[
                        dbc.Card(
                            className="card",
                            children=[
                                dbc.CardHeader(html.H4("Candlestick Pattern Selection")),
                                dbc.CardBody(
                                    children=[
                                        html.P(
                                            children=
                                            [
                                                "Select a Candlestick Chart pattern below. Upon making your selection the application "
                                                "will search the database of stocks, and return the stocks that match that criteria."
                                                ""
                                            ]
                                        ),
                                        dcc.Dropdown(
                                            id="candlestick-pattern-dropdown",
                                            options=[

                                                {'label': patternsDict[pattern], 'value': patternsDict[pattern]} for
                                                pattern
                                                in
                                                sorted(patternsDict)
                                            ],
                                            optionHeight=35,
                                            searchable=True,
                                            clearable=False,
                                            placeholder="Select a Candlestick Chart Pattern",
                                        ),
                                        # html.Button('Submit', id='get-pattern-btn', n_clicks=0)
                                    ],
                                ),
                            ]
                        ),
                    ],
                    align='center',
                    width=12
                ),
                dbc.Col(
                    children=[
                        html.Div(
                            children=[
                                dcc.Loading(
                                    children=[
                                        dbc.Card(
                                            id='chart-pattern-card',
                                            className="card",
                                            children=[
                                                html.Div(id='chart-pattern-container'),
                                                html.Center(
                                                    html.Div(
                                                        dcc.Graph(
                                                            id='empty',
                                                            figure={}
                                                        ),
                                                        style={'display': 'none'},
                                                    ),
                                                ),
                                            ],
                                            style={
                                                'width': '100%',
                                                # 'height': '25vh',
                                            }
                                        )
                                    ],
                                    type='circle',
                                    color=utils.get_random_color(utils),
                                ),

                            ]
                        ),
                    ],
                    align='center',
                    width=12,
                ),
            ],
            ),
            html.Br(),
            # Fundamental and Technical Analysis selection cards.
            dbc.Row(
                [
                    dbc.Col(
                        children=[
                            html.Div(
                                children=
                                [
                                    html.H2("Fundamental and Technical Analysis"),
                                    html.P(
                                        """
                                        Fundamental Analysis and Technical Analysis are of two differing schools of thought,
                                        however their disciplines tend to overlap quite often when it comes to making
                                        financially sound decisions.
                                        """
                                    ),
                                    html.P(
                                        """
                                        
                                        """
                                    ),
                                    html.Div(utils.get_sidebar("", companies_df, page_stock_info_ids)),
                                    html.Hr(),

                                    # Quick indicators from the latest db data if possible on the stock selected.
                                    dbc.CardGroup(
                                        children=[
                                            dbc.Card(
                                                className="card",
                                                children=[
                                                    html.H4("Liquidity", className='p-2'),
                                                    # dbc.CardImg(src="assets/img/technicalAnalysis.png"),
                                                    utils.loading_wrapper(
                                                        utils,
                                                        dcc.Graph(
                                                            id='liquidity-kpi',  # figure=[],
                                                            style={
                                                                'height': '200px',
                                                                'padding': '2px'
                                                            }

                                                        ),
                                                    )
                                                    # dbc.CardBody(
                                                    #     children=[
                                                    #         html.H4("Technical Analysis"),
                                                    #         html.P(
                                                    #             "Fundamental Analysis is a method of measuring a security's intrinsic value "
                                                    #             "by examining related economic and financial factors"
                                                    #             ""),
                                                    #     ]
                                                    # ),
                                                ],
                                            ),
                                            dbc.Card(
                                                className="card",
                                                children=[
                                                    html.H4("Solvency", className='p-2'),
                                                    # dbc.CardImg(src="assets/img/technicalAnalysis.png"),
                                                    utils.loading_wrapper(
                                                        utils,
                                                        dcc.Graph(
                                                            id='solvency-kpi',
                                                            # figure=[],
                                                            style={
                                                                'height': '200px',
                                                                'padding': '2px'
                                                            }
                                                        ), )
                                                    # dbc.CardBody(
                                                    #     children=[
                                                    #         html.H4("Technical Analysis"),
                                                    #         html.P(
                                                    #             "Fundamental Analysis is a method of measuring a security's intrinsic value "
                                                    #             "by examining related economic and financial factors"
                                                    #             ""),
                                                    #     ]
                                                    # ),
                                                ],
                                            ),
                                            dbc.Card(
                                                className="card",
                                                children=[
                                                    html.H4("Activity", className='p-2'),
                                                    utils.loading_wrapper(utils,
                                                                          dcc.Graph(
                                                                              id='activity-kpi',
                                                                              # figure=[],
                                                                              style={
                                                                                  'height': '200px',
                                                                                  'padding': '2px'
                                                                              }
                                                                          ), )
                                                ],
                                            ),
                                            dbc.Card(
                                                className="card",
                                                children=[
                                                    html.H4("Profitability", className='p-2'),
                                                    # dbc.CardImg(src="assets/img/technicalAnalysis.png"),
                                                    utils.loading_wrapper(
                                                        utils,
                                                        dcc.Graph(
                                                            id='profitability-kpi',
                                                            # figure=[],
                                                            style={
                                                                'height': '200px',
                                                                'padding': '2px'
                                                            }
                                                        ),
                                                    )
                                                    # dbc.CardBody(
                                                    #     children=[
                                                    #         html.H4("Technical Analysis"),
                                                    #         html.P(
                                                    #             "Fundamental Analysis is a method of measuring a security's intrinsic value "
                                                    #             "by examining related economic and financial factors"
                                                    #             ""),
                                                    #     ]
                                                    # ),
                                                ],
                                            ),
                                        ],
                                        className='p-5'
                                    ),
                                ],
                                id='fun-tech-info-wrapper',
                                className='mb-1 p-5',
                            ),

                            # Deeper Analysis of the selected stock.
                            dbc.CardGroup(
                                children=[
                                    dbc.Card(
                                        className="card",
                                        children=[
                                            dbc.CardImg(
                                                src="assets/img/towfiqu-barbhuiya-nApaSgkzaxg-unsplash.jpg",
                                                top=True,
                                                alt="Picture of man checking through and going over fundamental numbers for an investment. Image was provided by Towfiqu Barbhuiy from Unsplash.com"
                                            ),
                                            dbc.CardBody(
                                                # className='cardbody',
                                                children=[
                                                    html.H4("Fundamental Analysis"),
                                                    html.P(
                                                        ["Fundamental Analysis is a method of measuring a security's "
                                                         "intrinsic value or fair market value."
                                                         "by examining related economic and financial factors"
                                                         ""]),
                                                ]
                                            ),
                                            html.A(className="btn btn-primary", href="/fundamental-analysis",
                                                   children=["Fundamental Analysis"]),

                                        ],

                                    ),
                                    dbc.Card(
                                        className="card",
                                        children=[
                                            dbc.CardImg(
                                                src="assets/img/adam-nowakowski-MFms-wkv3Ow-unsplash.jpg",
                                                top=True,
                                                alt="Image of a man performing technical stock analysis on two screens. Image was provided by adam-nowakowski from Upsplash",
                                            ),
                                            dbc.CardBody(
                                                # className ='cardbody',
                                                children=[
                                                    html.H4("Technical Analysis"),
                                                    html.P(
                                                        "Fundamental Analysis is a method of measuring a security's intrinsic value "
                                                        "by examining related economic and financial factors"
                                                        ""),
                                                ]
                                            ),
                                            html.A(className="btn btn-primary", href="/technical-analysis",
                                                   children=["Technical Analysis"]),
                                            # dbc.CardLink("Card link", href="/pages/technical"),
                                        ],

                                    ),
                                ],
                                className='p-5'
                            ),
                        ],
                        align='center',
                        # width=12,
                    ),
                ]),
            html.Br(),
            dbc.Row(
                [
                    # dbc.Col(
                    #     children=[
                    #         html.Div(
                    #             children=[
                    #                 dcc.Loading(
                    #                     children=[
                    #                         dbc.Card(
                    #                             id='chart-pattern-card',
                    #                             className="card",
                    #                             children=[
                    #                                 html.Div(id='chart-pattern-container'),
                    #                                 html.Center(
                    #                                     html.Div(
                    #                                         dcc.Graph(
                    #                                             id='empty',
                    #                                             figure={}
                    #                                         ),
                    #                                         style={'display': 'none'},
                    #                                     ),
                    #                                 ),
                    #                             ],
                    #                             style={
                    #                                 'width': '100%',
                    #                                 # 'height': '25vh',
                    #                             }
                    #                         )
                    #                     ],
                    #                     type='circle',
                    #                     color=ATBDEFAULTTHEME.CADETBLUE,
                    #                 ),
                    #
                    #             ]
                    #         ),
                    #     ],
                    #     align='center',
                    #     width=12,
                    # ),
                ]
            ),
            html.Br(),

        ]
    )


layout = serve_layout()


@callback(
    Output('liquidity-kpi', 'figure'),
    Output('solvency-kpi', 'figure'),
    Output('activity-kpi', 'figure'),
    Output('profitability-kpi', 'figure'),
    Input('companies_dropdown', 'value')
)
def update_quick_kpis(stock_symbol):
    liquidity_kpi_fig = make_subplots(rows=2, cols=1, )
    solvency_kpi_fig = make_subplots(rows=2, cols=1, )
    activity_kpi_fig = make_subplots(rows=2, cols=1, )
    profitability_kpi_fig = make_subplots(rows=2, cols=1, )

    if stock_symbol is not None and stock_symbol != 'Company Ticker Symbol':
        conn = None
        try:
            conn = dbObj.create_connection(db_file=DB_FILE)
            # stock_price_df = pd.read_sql('SELECT * FROM stock_price, stock WHERE stock_id= stock.id', conn)
        except Error as e:
            logging.error(f"Error Occurred when Trying to connect to the Database | {e}")

        # stock_financials = f"""
        #     SELECT stock.id, stock.symbol, stock_balance_sheet.*
        #     FROM stock, stock_financials, stock_balance_sheet
        #     WHERE
        #     stock.company = '{stock_symbol}'
        #     --AND stock.id = stock_financials.stock_id
        #     AND stock.id = stock_balance_sheet.stock_id
        #     GROUP BY stock_balance_sheet.year
        #     --AND stock_balance_sheet.year >=2020
        # """
        stock_financials = dbObj.create_sql_string('./data/SQL/read/company_information/QuickRatios.sql')
        stock_financials += f"\nAND company='{stock_symbol}'"
        stock_financials = pd.read_sql(stock_financials, conn)

        max_year = stock_financials['year'].max()
        stock_financials = stock_financials[stock_financials['year'] == max_year].fillna(1)

        if 'Current_Ratio' in stock_financials.columns and len(stock_financials) > 0:
            curr_ratio = stock_financials['Current_Ratio']

            if len(curr_ratio) < 1:
                curr_ratio = pd.Series(data={0: 1})

            curr_ratio_go = go.Indicator(
                value=curr_ratio.iloc[0],
                title='Curr Ratio'
            )
            liquidity_kpi_fig.add_traces(curr_ratio_go)
        else:
            curr_ratio = 1
            curr_ratio_go = go.Indicator(
                value=curr_ratio,
                title='Check Curr Ratio'
            )
            liquidity_kpi_fig.add_traces(curr_ratio_go)

        if 'Debt_to_Equity' in stock_financials.columns:
            # shareholders_equity = stock_financials['Total Assets'] - stock_financials['Total Liab']
            tot_debt_ratio = stock_financials['Debt_to_Equity']

            if len(tot_debt_ratio) < 1:
                tot_debt_ratio = pd.Series(data={0: 1})

            tot_debt_ratio_go = go.Indicator(
                value=tot_debt_ratio.iloc[0],
                title='Debt/Equity Ratio'
            )
            solvency_kpi_fig.add_traces(tot_debt_ratio_go)
        else:
            tot_debt_ratio = 1
            tot_debt_ratio_go = go.Indicator(
                value=tot_debt_ratio,
                title='Check D/E Ratio'
            )
            solvency_kpi_fig.add_traces(tot_debt_ratio_go)

        if 'Asset Turnover' in stock_financials.columns:
            tot_asset_turnover = stock_financials['Asset_Turnover']

            if len(tot_asset_turnover) < 1:
                tot_asset_turnover = pd.Series(data={0: 1})

            tot_asset_turnover_go = go.Indicator(
                value=tot_asset_turnover.iloc[0],
                title='Tot Asset Turnover'
            )
            activity_kpi_fig.add_traces(tot_asset_turnover_go)
        else:
            tot_asset_turnover = 1
            tot_asset_turnover_go = go.Indicator(
                value=tot_asset_turnover,
                title='Tot Asset Turnover'
            )
            activity_kpi_fig.add_traces(tot_asset_turnover_go)

        if 'Profit_Margin' in stock_financials.columns:
            profit_margin = stock_financials['Profit_Margin']

            if len(profit_margin) < 1:
                profit_margin = pd.Series(data={0: 1})

            profit_margin_go = go.Indicator(
                value=profit_margin.iloc[0],
                title='Profit Margin'
            )
            profitability_kpi_fig.add_traces(profit_margin_go)
        elif 'Net Income' in stock_financials.columns and 'Total Assets' in stock_financials.columns:
            # Actually Return on Assets formula but returned in profitability.
            profit_margin = (stock_financials['Net Income']) / stock_financials['Total Assets']
            profit_margin_go = go.Indicator(
                value=profit_margin.iloc[0],
                title='Return on Assets'
            )
            profit_margin_go.add_traces(profit_margin_go)
        else:
            profit_margin = 1
            profit_margin_go = go.Indicator(
                value=profit_margin,
                title='Profit Margin'
            )
            profitability_kpi_fig.add_traces(profit_margin_go)
    else:
        curr_ratio = 0
        curr_ratio_go = go.Indicator(
            value=curr_ratio,
            title='Select Stock from Above'
        )
        liquidity_kpi_fig.add_traces(curr_ratio_go)

        tot_debt_ratio = 0
        tot_debt_ratio_go = go.Indicator(
            value=tot_debt_ratio,
            title='Select Stock from Above'
        )
        solvency_kpi_fig.add_traces(tot_debt_ratio_go)

        tot_asset_turnover = 0
        tot_asset_turnover_go = go.Indicator(
            value=tot_asset_turnover,
            title='Select Stock from Above'
        )
        activity_kpi_fig.add_traces(tot_asset_turnover_go)

        profit_margin = 0
        profit_margin_go = go.Indicator(
            value=profit_margin,
            title='Select Stock from Above'
        )
        profitability_kpi_fig.add_traces(profit_margin_go)

    return liquidity_kpi_fig, solvency_kpi_fig, activity_kpi_fig, profitability_kpi_fig


@callback(
    Output('chart-pattern-container', 'children'),
    [Input('candlestick-pattern-dropdown', 'value')],
    # Input('get-pattern-btn', 'n_clicks'),
    # State('chart-pattern-container', 'children'),

)
def display_candlestick_graph(pattern_value):
    pattern_graphs = []
    if pattern_value is None:
        pass
    else:
        conn = None
        try:
            conn = dbObj.create_connection(db_file=DB_FILE)
            # stock_price_df = pd.read_sql('SELECT * FROM stock_price, stock WHERE stock_id= stock.id', conn)
        except Error as e:
            logging.error(f"Error Occurred when Trying to connect to the Database | {e}")

        # Get only the companies column from the companies_df
        companies = companies_df['company']
        all_price_data = pd.read_sql_query(
            '''
            SELECT stock.company, stock.gics_sector,stock.gics_subsector, stock_price.* 
            FROM stock_price, stock 
            WHERE stock_price.stock_id=stock.id
            ''',
            conn)
        for company in companies:
            # Filter the dataset to only look at the current company and use that for analysis of the candlestick
            # pattern
            logging.info(company)
            price_data = all_price_data[(all_price_data.company == company)]

            # Get the pattern key from the value selected by in the dropdown. Reverse of how this is supposed to work.
            pattern_keys = list(patternsDict.keys())
            pattern_values = list(patternsDict.values())
            pattern_pos = pattern_values.index(pattern_value)
            pattern_key = pattern_keys[pattern_pos]

            # Getting the TALIB function for the pattern that we are interested in checking
            # using abstract api will allow for indicators to be used and passed as well.
            pattern_function = getattr(talib, pattern_key)

            try:
                pattern_data = pattern_function(price_data['Open'], price_data['High'], price_data['Low'],
                                                price_data['Close'])
                pattern_col_name = str(pattern_value).replace(" ", "_").replace("/", "_")
                price_data[pattern_col_name] = pattern_data

                if price_data[pattern_col_name].iloc[-1] != 0:
                    logging.info("{} matches the {} pattern".format(company, pattern_value))
                    new_pattern_graph = create_pattern_chart_card(pattern_value, company, price_data)
                    pattern_graphs.append(new_pattern_graph)

            except Exception as e:
                logging.error(f"Failed to get pattern data {e}")

        if pattern_graphs == [] and pattern_value is not None:
            pattern_graphs.append(
                html.Center(
                    html.P("No matches for the {} pattern were found".format(pattern_value))
                )
            )

    return dcc.Loading(children=[
        html.Div(pattern_graphs)
    ],
        type='circle',
        color=ATBDEFAULTTHEME.DARKCYAN
    )


@callback(
    Output('stock-rois-chart', 'children'),
    Input('heatmap-sector-dropdown', 'value'),
    # State('page-content', 'children')
)
def update_securities_in_sector_chart(pattern_value):
    if pattern_value:
        conn = dbObj.create_connection(dbObj.DB_FILE)
        # all_price_sql = dbObj.create_sql_string('data/SQL/AllStockPricesByCompanyDate.sql')

        stocks_in_sector_sql = dbObj.create_sql_string('./data/SQL/read/company_information/QuickRatios.sql')
        stocks_in_sector_sql += f"\nAND gics_sector = '{pattern_value}' ORDER BY stock_balance_sheet.year DESC"

        '''
        SELECT stock_price.*, stock.company
        FROM stock_price, stock
        WHERE stock_price.stock_id = stock.id
        ORDER BY stock.company    
        '''

        roi_df = pd.read_sql(stocks_in_sector_sql, conn)
        # roi_df = utils.add_daily_return_to_df(roi_df)
        # roi_df['daily_return'] = roi_df['daily_return'] * 100
        #
        # roi_df_copy = roi_df.copy()
        # roi_df_copy['max_date'] = roi_df.groupby(by="company", sort=False).date.transform('max')
        # roi_df_copy['min_date'] = roi_df.groupby(by='company', sort=False).date.transform('min')
        # logging.info(roi_df_copy.head())
        #
        # roi_df_copy = roi_df_copy[['date', 'company', 'adjusted_close', 'daily_return', 'max_date', 'min_date']]
        #
        # roi_df_copy.drop_duplicates(subset=['date', 'company'], inplace=True)
        #
        # min_roi_df = pd.DataFrame()
        # max_roi_df = pd.DataFrame()
        #
        # for index, row in roi_df_copy.iterrows():
        #     if roi_df_copy[(roi_df_copy['date'][index] == row['max_date'])]:
        #         max = roi_df_copy[(roi_df_copy['date'][index] == row['max_date'])][
        #             (roi_df_copy['company'] == row['company'])]
        #         # logging.info(max.head())
        #         max_roi_df = max_roi_df._append(max, ignore_index=True)
        #         logging.info("Max ROI DF\n{}\n".format(max_roi_df.head()))
        #
        #     min = roi_df_copy[(roi_df_copy['date'] == row['min_date'])][(roi_df_copy['company'] == row['company'])]
        #     # logging.info(min.head())
        #     min_roi_df = min_roi_df._append(min, ignore_index=True)
        #     logging.info("Min ROI DF\n{}\n".format(min_roi_df.head()))
        #
        # max_roi_df.drop_duplicates(inplace=True)
        # min_roi_df.drop_duplicates(inplace=True)
        #
        # roi_df_copy = pd.concat([max_roi_df, min_roi_df])
        #
        # roi_df_copy['total_return'] = roi_df_copy.apply(
        #     lambda row: utils.roi_between_dates_df(roi_df_copy, row['company'],
        #                                            row['max_date'],
        #                                            row['min_date']), axis=1)

        roi_heatmap = utils.generate_heatmap(
            utils,
            roi_df,
            title='',
            z_values='Profit_Margin',
            x_column='year',
            y_column='company',
        )
        roi_heatmap_fig = dcc.Graph(
            figure=roi_heatmap,
            animate=True,
            clear_on_unhover=True,
            responsive=True
        )

        roi_df = utils.generate_generic_dash_datatable(
            utils,
            roi_df,
            id='sector-margins-data-table',
        )
        return utils.loading_wrapper(
            utils,
            html.Div(
                [
                    roi_heatmap_fig,
                    html.Br(),
                    roi_df,
                ]
            ),
        )

        # dcc.Loading(
        # children=[roi_df],
        # type='circle',
        # color='lightseagreen')
    else:
        conn = dbObj.create_connection(dbObj.DB_FILE)
        # all_price_sql = dbObj.create_sql_string('data/SQL/AllStockPricesByCompanyDate.sql')

        stocks_in_sector_sql = dbObj.create_sql_string('./data/SQL/read/company_information/QuickRatios.sql')
        stocks_in_sector_sql += f"\nAND gics_sector = 'Energy' ORDER BY stock_balance_sheet.year DESC"

        '''
                SELECT stock_price.*, stock.company
                FROM stock_price, stock
                WHERE stock_price.stock_id = stock.id 
                AND gics_sector = "Energy"
                ORDER BY stock.company
                AND stock_price.date    
                '''

        roi_df = pd.read_sql(stocks_in_sector_sql, conn)
        # roi_df = utils.add_daily_return_to_df(roi_df)
        # roi_df['daily_return'] = roi_df['daily_return'] * 100
        #
        # roi_df_copy = roi_df.copy()
        # roi_df_copy['max_date'] = roi_df.groupby(by="company", sort=False).date.transform('max')
        # roi_df_copy['min_date'] = roi_df.groupby(by='company', sort=False).date.transform('min')
        # logging.info(f"RoI DF Data \n {roi_df_copy.head()}")
        #
        # roi_df_copy = roi_df_copy[['date', 'company', 'adjusted_close', 'daily_return', 'max_date', 'min_date']]
        #
        # roi_df_copy.drop_duplicates(subset=['date', 'company'], inplace=True)
        #
        # min_roi_df = pd.DataFrame()
        # max_roi_df = pd.DataFrame()
        #
        # for index, row in roi_df_copy.iterrows():
        #     if (roi_df_copy['date'][index] == row['max_date']):
        #         max = roi_df_copy[(roi_df_copy['date'] == row['max_date'])][(roi_df_copy['company'] == row['company'])]
        #         # logging.info(max.head())
        #         max_roi_df = max_roi_df._append(max, ignore_index=True)
        #         logging.info(f"Max RoI DF\n{max_roi_df.head()}\n")
        #
        #     min = roi_df_copy[(roi_df_copy['date'] == row['min_date'])][(roi_df_copy['company'] == row['company'])]
        #     # logging.info(min.head())
        #     min_roi_df = min_roi_df._append(min, ignore_index=True)
        #     logging.info(f"Min RoI DF\n{min_roi_df.head()}\n")
        #
        # max_roi_df.drop_duplicates(inplace=True)
        # min_roi_df.drop_duplicates(inplace=True)
        #
        # roi_df_copy = pd.concat([max_roi_df, min_roi_df])
        #
        # roi_df_copy['total_return'] = roi_df_copy.apply(
        #     lambda row: utils.roi_between_dates_df(roi_df_copy, row['company'],
        #                                            row['max_date'],
        #                                            row['min_date']), axis=1)

        roi_heatmap = utils.generate_heatmap(
            utils,
            roi_df,
            title='',
            z_values='Profit_Margin',
            x_column='year',
            y_column='company',
        )
        roi_heatmap_fig = dcc.Graph(
            figure=roi_heatmap,
            animate=True,
            clear_on_unhover=True,
            responsive=True
        )

        roi_df = utils.generate_generic_dash_datatable(
            utils,
            roi_df,
            id='sector-margins-data-table',
        )

        return utils.loading_wrapper(
            utils,
            html.Div(
                [
                    roi_heatmap_fig,
                    html.Br(),
                    roi_df,
                ]
            ),
        )


@callback(
    Output('sector-margins-chart', 'children'),
    Input('heatmap-sector-dropdown', 'value'),
    # State('page-content', 'children')
)
def update_sector_chart(sector):
    if sector and sector is not None:
        conn = dbObj.create_connection(dbObj.DB_FILE)
        # sector_balancesheet_sql = dbObj.create_sql_string(
        #     'data/SQL/create/sector_analysis/SectorandSubsectorTotalsTable.sql')
        # sector_earnings_sql = dbObj.create_sql_string('data/SQL/read/sector_analysis/SectorandSubsectorEarnings.sql')
        #
        # sector_balancesheet_sql = '''
        # SELECT * FROM sector_subsector_totals;
        # '''

        sector_balancesheet_sql = dbObj.create_sql_string('./data/SQL/read/sector_analysis/SectorQuickRatios.sql')
        sector_balancesheet_sql += f"\nAND gics_sector ='{sector}' GROUP BY stock_balance_sheet.year"
        sector_bs_df = pd.read_sql(sector_balancesheet_sql, conn)
        # sector_earn_df = pd.read_sql(sector_earnings_sql, conn)
        # roi_df = pd.melt(frames=[sector_bs_df, sector_earn_df],)
        roi_df = sector_bs_df

        roi_heatmap = utils.generate_heatmap(
            utils,
            roi_df,
            title='',
            z_values='Profit_Margin',
            x_column='year',
            y_column='gics_sector',
        )
        roi_heatmap_fig = dcc.Graph(
            figure=roi_heatmap,
            animate=True,
            clear_on_unhover=True,
            responsive=True
        )

        roi_df = utils.generate_generic_dash_datatable(
            utils,
            roi_df,
            id='sector-margins-data-table',
        )

        return dcc.Loading(
            children=[
                html.Div(
                    [
                        roi_heatmap_fig
                    ],
                    # style={'height': '25vh'}

                )
            ],
            type='circle',
            color=utils.get_random_color(utils, )
        )
    else:
        conn = dbObj.create_connection(dbObj.DB_FILE)
        # sector_balancesheet_sql = dbObj.create_sql_string(
        #     'data/SQL/create/sector_analysis/SectorandSubsectorTotalsTable.sql')
        # sector_earnings_sql = dbObj.create_sql_string('data/SQL/read/sector_analysis/SectorandSubsectorEarnings.sql')

        sector_balancesheet_sql = dbObj.create_sql_string('./data/SQL/read/sector_analysis/SectorQuickRatios.sql')
        sector_balancesheet_sql += f"\n ORDER BY stock_balance_sheet.year AND gics_sector"
        sector_bs_df = pd.read_sql(sector_balancesheet_sql, conn)
        # sector_earn_df = pd.read_sql(sector_earnings_sql, conn)
        # roi_df = pd.melt(frames=[sector_bs_df, sector_earn_df],)
        roi_df = sector_bs_df
        roi_heatmap = utils.generate_heatmap(
            utils,
            roi_df,
            title='',
            z_values='Profit_Margin',
            x_column='year',
            y_column='gics_sector')

        roi_df = utils.generate_generic_dash_datatable(
            utils,
            roi_df,
            id='sector-margins-data-table',
        )

        roi_heatmap_fig = dcc.Graph(
            figure=roi_heatmap,
            animate=True,
            clear_on_unhover=True,
            responsive=True
        )
        return dcc.Loading(
            children=[
                html.Div(
                    [
                        roi_heatmap_fig,
                        html.Br(),
                        roi_df,
                    ]
                )
            ],
            type='circle',
            color=utils.get_random_color(utils, )
        )
