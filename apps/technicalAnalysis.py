import random
from sqlite3 import Error
import logging

import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate

import db
import utils
from app import app
from stock import MyStock

# from app import app  # Needed for making app multi-page

# Interacts with the Database
dbObj = db.DBConnection()

# Interacts with the yFinance API
StockObj = MyStock()
conn = None

# Connect to DB and  Load Data
DB_FILE = "./stock-db.db"

try:
    conn = dbObj.create_connection(db_file=DB_FILE)
    # stock_price_df = pd.read_sql('SELECT * FROM stock_price, stock WHERE stock_id= stock.id', conn)
except Error as e:
    logging.error(e)

# TODO Feature Enhancement add ability to automatically show how security of interest does against whatever the industry
#  3 year rolling averages are. Similar to Grad School Corp Finance Project.

# Random stock symbols on the S&P500 as of June 2021
stock_symbols = ['AMGN', 'NKE', 'DE', 'MCK', 'HIG', 'VLO', 'STX']
stock = random.randrange(0, len(stock_symbols))
stock_symbol = stock_symbols[stock]

companies_df = dbObj.select_table_data(conn=conn, table_name='stock')

options = {'options': [], 'option_dates': []}

calls = []
puts = []
financials = []
balanceSheet = []
cashflows = []
earnings = []
stock_info = []

'''
Converts Timestamp column's to only be the year.
:param: Pandas Dataframe Object containing the Data
:param: inplace if you want the columns conversions to be done inplace.
:returns: the Dataframe with the converted timestamps to year

'''


def update_UI(stock_symbol):
    candlestick_figure, ATR, RSI, macd_figure, ATR_layout, RSI_layout, calls, puts, data, call_datatable, put_datatable, = None, None, None, None, None, None, None, \
                                                                                                                           None, None, None, None
    company_name, stock_sector, stock_subsector, headquarters, data = None, None, None, None, None

    if stock_symbol is not None:
        company_info_df, conn = utils.get_company_info(stock_symbol)

        if company_info_df is None or company_info_df.empty:
            # This takes us to adding the new symbol to our stocks table in the DB
            # raise Error
            data = StockObj.get_ticker_all(stock_symbol=stock_symbol, add_ma=False, add_bb=False,
                                           add_mi=False)  # TODO API HIT

            stock_info = StockObj.get_ticker_stock_info(stock_symbol=stock_symbol)  # TODO API HIT

            try:
                sector = stock_info.loc['sector']
                sector = sector[0]
            except:
                sector = "SECTOR"

            try:
                company = stock_info.loc['shortName']
                company = company[0]
            except:
                company = stock_symbol

            try:
                industry = stock_info.loc['industry']
                industry = industry[0]
            except:
                industry = "INDUSTRY"

            try:
                city = stock_info.loc['city']
                city = city[0]
            except:
                city = "CITY"

            try:
                state = stock_info.loc['state']
                state = state[0]
            except:
                state = "STATE"

            headquarters = city + "," + state

            # Must be a tuple to be passed as VALUES in DB
            param_list = (stock_symbol, company, sector, sector, industry, headquarters,)

            # Insert basic Stock Information into DB
            insert_sql = """ INSERT INTO stock(symbol, company, nasdaq_sector, gics_sector,gics_subsector,headquarters) VALUES (?,?,?,?,?,?);"""
            dbObj.insert_into_table(conn, insert_sql, param_list)  # TODO DB HIT

            # Insert stock_price data into the stock price by newly created companies stock_id
            companies_df = pd.read_sql_query('SELECT * from stock', conn)  # TODO DB HIT
            companies_df.query("symbol == '{}'".format(stock_symbol), inplace=True)
            stock_id = companies_df['id'].reset_index()
            stock_id = stock_id['id'][0]

            data['date'] = pd.to_datetime(data.index)
            data.rename_axis("Date", axis='index', inplace=True)
            data.rename(columns={
                'Adj Close': 'adjusted_close'
            }, inplace=True)
            data['stock_id'] = stock_id

            data.to_sql('stock_price', conn, if_exists='append', index=False)  # TODO DB HIT

            # TODO Remove weekends and holidays from teh dataframe since there is no trading on those days.
            data = StockObj.get_ticker_all_add_df(StockObj, data)  # TODO API HIT

            data.drop_duplicates(inplace=True)
        else:
            stock_id = company_info_df['id'][0]
            stock_sector = company_info_df['gics_sector'][0]
            stock_subsector = company_info_df['gics_subsector'][0]
            company_name = company_info_df['company'][0]
            headquarters = company_info_df['headquarters'][0]

            # Getting Stock Price Data from the DB by the Stock ID(FK)
            data = dbObj.select_record(conn, 'stock_price', stock_id)

        # Getting the Stock Data for the Stock Symbol that is in our DB, but doesn't have price data.
        if data is None and type(data) is not pd.DataFrame:
            data = StockObj.get_ticker_all(stock_symbol=stock_symbol, add_ma=False, add_bb=False,
                                           add_mi=False)  # TODO API HIT
            data['date'] = pd.to_datetime(data.index)
            data.rename_axis("Date", axis='index', inplace=True)
            data.rename(columns={
                'Adj Close': 'adjusted_close'
            }, inplace=True)
            data['stock_id'] = stock_id

            data.to_sql('stock_price', conn, if_exists='append', index=False)
            data = StockObj.prep_dataframe(data, conn)
        else:
            data = StockObj.get_ticker_all_add_df(dataframe=data, conn=conn, add_ma=False, add_mi=False,
                                                  add_bb=False)
            # appending the newest stock prices for the security to the database.
            data.to_sql('stock_price', conn, if_exists='append', index=False)

        # Adding Technical Analysis indicators to Stock Price Data and updating the data to the most current day.
        data = StockObj.get_ticker_all_add_df(dataframe=data, conn=conn, add_ma=True, add_mi=True,
                                              add_bb=True)

    options, financials, cashflows, earnings, balanceSheet, stock_info = StockObj.get_ticker_additional_information(
        stock_symbol=stock_symbol, stock_info=True)  # TODO API HIT : ALSO MOVE TO OTHER PAGE IN APP

    candlestick_figure = utils.generate_candlestick_graph_w_indicators(data, stock_symbol)

    # Checking to make sure that the stock has options, someitmes it is hit or miss with yFinance
    if len(options) > 0:
        calls = options['options'].calls.drop(
            columns=['contractSymbol', 'lastTradeDate', 'contractSize', 'currency'])
        puts = options['options'].puts.drop(columns=['contractSymbol', 'lastTradeDate', 'contractSize', 'currency'])

        call_datatable = utils.generate_option_dash_datatable(
            dataframe=calls,
            id="calls-table-data")
        # data_1 = calls.to_dict('records')
        put_datatable = utils.generate_option_dash_datatable(
            dataframe=puts,
            id="puts-table-data")
        # data_2 = puts.to_dict('records')

    # OBV Chart which is a leading indicator can be paired with a lagging indicator like (BB, MA, ATR,MACD)
    obv_chart = utils.generate_scatter_graph_no_bar(dataframe=data, x_column='date', y_column='obv',
                                                    secondary_y_column='Close',
                                                    title="OBV (On Balance Volume)", upper_bound=0, lower_bound=0,
                                                    candlestick=True)

    # ATR Chart
    atr_chart = utils.generate_scatter_graph(dataframe=data, x_column='date', y_column='ATR',
                                             secondary_y_column='Volume',
                                             title="ATR (Average True Range)", upper_bound=0, lower_bound=0)

    macd_figure = utils.generate_macd_chart(dataframe=data)

    # Gets the most recent price in the data for the stock
    logging.info("End of Dataframe \n {}".format(data.tail()))
    logging.info("Total Length of Dataframe \n {}".format(len(data)))
    logging.info("Total Length by Date Column \n {}".format(len(data.date)))
    logging.info("Total Length by Index Column \n {}".format(len(data.index)))

    stock_price = "${:.2f}".format(data['Close'][data.shape[0] - 1].min())

    logging.info(
        "{}\n{}\n{}\n{}\n{}".format(company_name, stock_symbol, stock_price, stock_sector, stock_subsector, stock_info))

    return candlestick_figure, obv_chart, atr_chart, macd_figure, call_datatable, put_datatable, company_name, stock_symbol, stock_price, stock_sector, stock_subsector


# Constant styles for componenets
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

CONTENT_STYLE = {
    "margin-left": "20%",
    "margin-right": "2rem",
    "min-width": "80%",
    "padding": "2rem 1rem",
}

'''
Layout of our Dash Application - the Bones of the App 

'''

page_stock_info_ids = {}
page_stock_info_ids['stock-name'] = 'stock-name'
page_stock_info_ids['stock-title'] = 'stock-title'
page_stock_info_ids['stock-price'] = 'stock-price'
page_stock_info_ids['stock-sector'] = 'stock-sector'
page_stock_info_ids['stock-subsector'] = 'stock-subsector'

technical_page_layout = dbc.Container(
    # id='page-content',
    # className='col-md-12',
    children=[
        utils.get_sidebar(app, companies_df, page_stock_info_ids),

        dbc.Row([
            # Company Name
            html.H1(
                id='stock-name-heading-tech',
                className='mb-5'
                          "{} About".format(stock_symbol)
            ),
            # Company information
            dbc.Col(
                className='col-md-12 mt-5',
                children=[
                    html.H2(
                        id='stock-price-heading',
                        children=[
                            "Price Analysis".format(stock_symbol)
                        ]),

                    dbc.Card(
                        className='mb-2 mt-2 pl-2 pr-2',
                        children=[
                            dbc.CardBody(
                                children=[
                                    html.P(
                                        children=[
                                            "Stock Price with Bollinger Band Overlays."
                                            "The Bollinger Bands act as a way to show, "
                                            "rising or reversal trends on a security. The wider"
                                            "the band the more likely a reversal is to happen"
                                        ]
                                    ),
                                    dcc.Loading(
                                        children=[
                                            dcc.Graph(
                                                id='candlestick-graph',
                                                animate=True,
                                            ),
                                        ],
                                        type='circle',
                                        color='lightseagreen'
                                    ),

                                ]),
                        ]),
                ],
                width=12,
            ),

            dbc.Row(
                children=[
                    dbc.Col(
                        # className='col-md-4 mt-5',
                        children=[
                            dbc.Card(
                                className='mb-2 mt-2 pl-2 pr-2',
                                children=[
                                    dbc.CardHeader(children=[
                                        html.H3("On Balance Volume - OBV"),
                                    ]),
                                    dbc.CardBody(
                                        children=[
                                            html.P(
                                                children=[

                                                    "On-balance volume (OBV) is a technical indicator of momentum, "
                                                    "using volume changes to make price predictions. OBV shows crowd "
                                                    "sentiment that can predict a bullish or bearish outcome."
                                                    ""
                                                    "The actual value of the OBV is unimportant; concentrate on its "
                                                    "direction."
                                                    "When both price and OBV are making higher peaks and higher "
                                                    "troughs, the upward trend is likely to continue. When both price "
                                                    "and OBV are making lower peaks and lower troughs, the downward "
                                                    "trend is likely to continue. During a trading range, "
                                                    "if the OBV is rising, accumulation may be taking place—a "
                                                    "warning of an upward breakout. During a trading range, if the "
                                                    "OBV is falling, distribution may be taking place—a warning "
                                                    "of a downward breakout. When price continues to make higher peaks "
                                                    "and OBV fails to make higher peaks, the upward trend is likely "
                                                    "to stall or fail. This is called a negative divergence. When "
                                                    "price continues to make lower troughs and OBV fails to make "
                                                    "lower troughs, the downward trend is likely to stall or fail. "
                                                    "This is called a positive divergence."
                                                    ""
                                                ]
                                            ),
                                        ]),
                                ]),

                            dbc.Card(
                                className='mb-2 mt-2 pl-2 pr-2',
                                children=[
                                    dbc.CardBody(
                                        children=[
                                            dcc.Loading(children=[
                                                dcc.Graph(
                                                    id='obv-chart',
                                                    animate=True,
                                                ),
                                            ],
                                                type='circle',
                                            ),
                                        ]),
                                ]),

                        ],
                        width=12,
                    ),

                ],
            ),
            dbc.Row([

                dbc.Col(
                    className='col-md-8 mt-5',
                    children=[
                        dbc.Card(
                            className='mb-2 mt-2 pl-2 pr-2',
                            children=[
                                dbc.CardBody(
                                    children=[

                                        dcc.Loading(
                                            children=[
                                                dcc.Graph(
                                                    id='atr-chart',
                                                    animate=True,
                                                ),
                                            ],
                                            type='circle',
                                        ),

                                    ]),
                            ]),
                    ]),

                dbc.Col(
                    className='col-md-4 mt-5',
                    children=[
                        dbc.Card(
                            className='mb-2 mt-2 pl-2 pr-2',
                            children=[
                                dbc.CardHeader(children=[
                                    html.H3("Average True Range - ATR"),
                                ]),
                                dbc.CardBody(
                                    children=[
                                        html.P(
                                            children=[
                                                "Average True Range measures the Volatility in Price. Average True "
                                                "Range (ATR) is the average of true ranges over the specified period. "
                                                "ATR measures volatility, taking into account any gaps in the price "
                                                "movement. Typically, the ATR calculation is based on 14 periods, "
                                                "which can be intraday, daily, weekly, or monthly. "
                                                ""
                                                "An expanding ATR indicates increased volatility in the market, with the"
                                                " range of each bar getting larger. A reversal in price with an "
                                                "increase in ATR would indicate strength behind that move. ATR is not "
                                                "directional so an expanding ATR can indicate selling pressure or "
                                                "buying pressure. High ATR values usually result from a sharp advance "
                                                "or decline and are unlikely to be sustained for extended period"

                                            ]
                                        ),

                                    ]),
                            ]),
                    ]),
            ]
            ),

            dbc.Row(
                children=[
                    dbc.Col(
                        className='col-md-12 mt-5',
                        children=[
                            dbc.Card(
                                className='mb-2 mt-2 pl-2 pr-2',
                                children=[
                                    dbc.CardBody(
                                        children=[
                                            dcc.Loading(
                                                children=[
                                                    html.P(
                                                        children=[
                                                            "Moving Average Convergence Divergence measures the "
                                                            "Volatility in Price. Although it is an oscillator, "
                                                            "it is not typically used to identify over bought or "
                                                            "oversold conditions. It appears on the chart as two "
                                                            "lines which oscillate without boundaries. The crossover "
                                                            "of the two lines give trading signals similar to a two "
                                                            "moving average system."

                                                        ]
                                                    ),
                                                    dcc.Graph(
                                                        id='macd-graph',
                                                        animate=True,
                                                    ),
                                                ],
                                                type='circle',
                                                color='lightseagreen'
                                            ),
                                        ]),
                                ]),
                        ]
                    ),
                ]
            ),

        ]),

        dcc.Loading(
            id="calls-table",
            type="circle",
        ),

        dcc.Loading(
            id="puts-table",
            type="circle",
        ),
    ]

)

'''

    Dash Callback that allows for interactivity between UI, API and DB

    '''


@app.callback(
    Output('stock-name-heading-tech', 'children'),
    Output('stock-price-heading', 'children'),
    Input('stock-storage', 'data'),
    State('stock-storage', 'data')
)
def update_layout_w_storage_data(data, dataState):
    if data is None:
        raise PreventUpdate

    stockNameHeading = data['company']
    stockPriceHeading = data['company']

    return stockNameHeading, stockPriceHeading


@app.callback(Output('candlestick-graph', 'figure'),
              Output('obv-chart', 'figure'),
              Output('atr-chart', 'figure'),
              Output('macd-graph', 'figure'),
              Output('calls-table', 'children'),
              Output('puts-table', 'children'),
              Output('stock-name', 'children'),
              Output('stock-title', 'children'),
              Output('stock-price', 'children'),
              Output('stock-sector', 'children'),
              Output('stock-subsector', 'children'),
              Input('get_stock_btn', 'n_clicks'),
              Input('ticker_input', 'value'),
              Input('companies_dropdown', 'value'),
              Input('stock-storage', 'data'),
              # [Input(str(stock_symbol + "-" + str(options['option_dates'][i])), 'n_clicks') for i in
              #  range(0, len(options['option_dates']))],
              State('ticker_input', 'value'),
              # State('companies-dropdown', 'value'),
              )
def update_layout(n_clicks, ticker_input_value, companies_dropdown, ticker_input, data):
    # Returns the updated information after entering a Stock Ticker into the Input Box
    if type(ticker_input) is dict:
        data = ticker_input
        ticker_input = None

    if data is not None:
        stock_symbol = data['stock']
    else:
        stock_symbol = utils.generate_random_stock()

    # TODO access Callback Context information to know which button from the options button list that was generated
    #  and see which button was clicked and get that option chain and data. NEEDS FIXED

    # user_click = dash.callback_context.triggered[0]['prop_id'].split('.')[0]
    # callback_states = dash.callback_context.states.values()
    # callback_inputs = dash.callback_context.inputs.values()
    #
    # if user_click != '' and user_click != 'get_stock_btn' and user_click != 'companies_dropdown':
    #     ctx = dash.callback_context
    #
    #     if not ctx.triggered:
    #         optExDate = ""
    #     else:
    #         # Button Id will be in form of stocksymbol-mm-dd-yyyy format splitting on the second - gives us the option
    #         # date of interest
    #         optExDate = user_click
    #         K = 2
    #         optExDate = optExDate.split("-", K)

    # TODO add in dropdown selection option
    if companies_dropdown is not None and companies_dropdown != "Company Ticker Symbol":
        if companies_dropdown:
            stock_id = None
            try:
                conn = dbObj.create_connection(DB_FILE)

                # Getting single record for company - If no record returned we create and get data.
                company_info_df = pd.read_sql_query(
                    'SELECT symbol, id, company FROM stock WHERE stock.company="{}"'.format(companies_dropdown),
                    conn)

                if company_info_df.empty:
                    # This takes us to adding the new symobl to our stocks table in the DB
                    raise Error
                else:
                    stock_symbol = company_info_df['symbol'][0]
                    return update_UI(stock_symbol)

            except Error as e:
                logging.error(e)
    elif ticker_input_value is not None:
        return update_UI(ticker_input_value)
    # Returns initial data for the UI
    elif stock_symbol is not None:
        return update_UI(stock_symbol)
