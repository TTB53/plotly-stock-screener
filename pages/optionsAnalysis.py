"""

Options Analysis

------------------------------------------------------------------------------
Program Description
-------------------------------------------------------------------------------

Analyze the Calls and Puts on the Option Market.


For Trading Options

When buying calls you do not want to get the shares assigned, and want to close it out ITM before expiration,
when selling calls you want them to expire worthless, you get to keep premimum and you 100 shares.

******* BEFORE BUYING OPTIONS MAKE SURE TO CHECK EX-DIV DATE ************

Extrinsic Value - Time Value. This is important for Out of the Money (OTM) options.

Intrinsic Value - The difference between the current price and the strike price. Priced into the option price.

Strike Price -  The price at which you will purchase the underlying given your option contract.

Expiration Date - Date that the option will expire,

Know the Greeks for Options

Delta - How much the option value changes with a $1.00 increase/decrease in the share price.
    Calls - 0 and 1
    Puts - 0 and -1

    Like Owning the Shares without actually owning the share.
    positive delta bullish on the market, negative delta is bearish on the market

    Roughly the % Chance of this option becoming in the money (ITM) at some point before expiration,
    which helps you hedge risk.

    Speed at which options prices change

Gamma - How fast the delta changes with a $1 change in share price.
    accelerates delta in a positive or negative way, so they are correlated.

    When Buying High Gamma can be your friend if you forecast its direction correctly, converse is true when selling,
    high gamma is not your friend.


Theta - How much option value is going to decrease (Time decay) everyday keeping the price and implied volitality (IV)
        constant. The option's value decrease increases as time inches closer to expiration. Like a ball rolling downhill,
        your monies getting further and further away (if your the buyer) until its gone.

        This is ENEMY NUMBER UNO for options buyer's as it decreases the value down to nothing as time gets closer to
        expiration date. Again, this is converse for the Option seller as they not only get to keep their underlying,
        but gain a premium as well.

        at-the-money options have the most sensitivity to theta because they have the biggest time-value built into thier
        premiums making their risk higher.


Vega - How much options value will change with a 1% Change to Implied Volatility
    if IV dies that is how much vega is going to hurt and cost you money even when the stock price goes up
    Do not fall victim to the IV Crush usually around earnings - DO NOT BUY calls right before Earnings
    The lower the IV the less vega will effect option premium

Rho - How much the option value is going to change with 1% Change in interest rate, T-Bonds, etc. This usually only comes
into play with LEAPS because if interest rates rise that makes borrowing money more expensive i.e smaller growth.

Options Strategum:
Short Condor Strategy - works on securites with High Volatility (Price Swings)
----------------------------------------------------------------------------------

"""
from sqlite3 import Error
import logging

import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
import pandas as pd
import yfinance
from dash import callback
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate

import db
from utils import Utils as utils
from stock import MyStock

# Object that interacts with the Database
dbObj = db.DBConnection

# Interacts with the yFinance API and deals with the Stock related information
StockObj = MyStock()
conn = None

# Connect to DB and Load Data
DB_FILE = dbObj.DB_FILE

try:
    conn = dbObj.create_connection(dbObj, db_file=DB_FILE)
    logging.info("Successfully Connected to the DB from Options Analysis Page.")
    # stock_price_df = pd.read_sql('SELECT * FROM stock_price, stock WHERE stock_id= stock.id', conn)
except Error as e:
    logging.error(f"Error Occurred while trying to connect {DB_FILE} from the Options Analysis Page | {e}")

companies_df = dbObj.select_table_data(dbObj, conn=conn, table_name='stock')
logging.info(f"Companies Dataframe {companies_df.head(20)}\n{companies_df.tail(20)}")

options = {'options': [], 'option_dates': []}
calls = []
puts = []

stock_info = {}
stock_symbol = None
stock_name = None

page_stock_info_ids = {}
page_stock_info_ids['stock-name'] = 'options-stock-name'
page_stock_info_ids['stock-title'] = 'options-stock-title'
page_stock_info_ids['stock-price'] = 'options-stock-price'
page_stock_info_ids['stock-sector'] = 'options-stock-sector'
page_stock_info_ids['stock-subsector'] = 'options-stock-subsector'

dash.register_page(__name__,
                   path="/options-analysis",
                   name='Options Analysis',
                   title='Stock Screener - Options Analysis - ATB Analytics Group',
                   description='Stock Options Analysis'

                   )

layout = dbc.Container(
    children=[
        dbc.Row(
            children=[
                dbc.Col(
                    [
                        html.Div(utils.get_sidebar("", companies_df, page_stock_info_ids)),
                        # Current Stock info wrapper
                        html.Span(
                            id='option-curr-info-wrapper',
                            className='curr-info-wrapper mb-5',
                            children=[
                                html.H2(
                                    id='stock-name-options',
                                    className='mb-2 '
                                ),
                                html.H2(
                                    id='stock-price-options',
                                    className='mb-2 '
                                ),
                            ]
                        ),
                    ],
                    width=12,
                )
            ]),
        html.Br(),
        html.H1("Options Analysis"),
        dbc.Row(
            children=[
                dbc.Col(children=[], width=6),
                dbc.Col(children=[], width=6),
            ]
        ),
        html.Br(),
        dbc.Row(id='stock-options-info',
                children=[
                    # dbc.Col([html.Span([html.H2(id='stock-name-options'), html.H2(id='stock-price-options')])],
                    #         width=6),
                    dbc.Col([html.P("Blurb Blurb Blurb")], width=6),
                ]
                ),

        html.Br(),

        dbc.Row([
            dbc.Col(
                [
                    html.H2("Call Options"),
                    html.P("Call options are options that will come due when ...."),
                    dbc.Card(
                        className='mb-2 mt-2 pl-2 pr-2',
                        children=[
                            dbc.CardBody(
                                children=[
                                    dcc.Loading(
                                        id="calls-table",
                                        children=[],
                                        type="circle",
                                    ),
                                ]),
                        ]
                    ),

                ]
            ),
            dbc.Col(
                [
                    html.H2("Put Options"),
                    html.P("Put options are options that will come due when ...."),

                    dbc.Card(
                        className='mb-2 mt-2 pl-2 pr-2',
                        children=[
                            dbc.CardBody(
                                children=[
                                    dcc.Loading(
                                        id="puts-table",
                                        children=[],
                                        type="circle",
                                    ),
                                ]),
                        ]
                    ),
                ]
            )
        ])
    ]
)


def update_options_UI(stock_symbol):
    call_datatable, put_datatable = None, None
    company_name, stock_sector, stock_subsector, headquarters, data = None, None, None, None, None

    if stock_symbol is not None:
        company_info_df, conn = utils.get_company_info(utils, stock_symbol)

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
            data = dbObj.select_record(dbObj, conn, 'stock_price', stock_id)

        options = StockObj.get_ticker_additional_information(
            stock_symbol=stock_symbol, stock_info=True, stock_id=stock_id, conn=conn,
            save_data=False, options=True, balanceSheet=False, earnings=False,
            financials=False, cashflows=False, )

        # Checking to make sure that the stock has options, sometimes it is hit or miss with yFinance
        if len(options) > 0 and type(options) != str:
            calls = options['options'].calls.drop(
                columns=['contractSymbol', 'lastTradeDate', 'contractSize', 'currency'])
            puts = options['options'].puts.drop(columns=['contractSymbol', 'lastTradeDate', 'contractSize', 'currency'])

            call_datatable = utils.generate_option_dash_datatable(
                utils,
                dataframe=calls,
                id="calls-table-data")
            # data_1 = calls.to_dict('records')
            put_datatable = utils.generate_option_dash_datatable(
                utils,
                dataframe=puts,
                id="puts-table-data")
            # Gets the most recent price in the data for the stock
            logging.info("End of Dataframe \n {}".format(data.tail()))
            logging.info("Total Length of Dataframe \n {}".format(len(data)))
            logging.info("Total Length by Date Column \n {}".format(len(data.date)))
            logging.info("Total Length by Index Column \n {}".format(len(data.index)))

            stock_price = "${:.2f}".format(data['Close'][data.shape[0] - 1].min())

            logging.info(
                "{}\n{}\n{}\n{}\n{}".format(company_name,
                                            stock_symbol,
                                            stock_price,
                                            stock_sector,
                                            stock_subsector))

            return company_name, stock_price, call_datatable, put_datatable


@callback(
    Output('stock-name-options', 'children'),
    Output('stock-price-options', 'children'),
    Output('calls-table', 'children'),
    Output('puts-table', 'children'),
    Input('ticker_input', 'value'),
    Input('companies_dropdown', 'value'),
    Input('stock-storage', 'data'),
    State('ticker_input', 'value'),
    suppress_callback_exceptions=True
)
def update_options_layout(ticker_input_value, companies_dropdown, ticker_input, data):
    # Returns the updated information after entering a Stock Ticker into the Input Box
    if type(ticker_input) is dict:
        data = ticker_input
        ticker_input = None

    if data is not None:
        stock_symbol = data['stock']
    else:
        stock_symbol = utils.generate_random_stock(utils, )

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
                    return update_options_UI(stock_symbol)

            except Error as e:
                logging.error(e)
    elif ticker_input_value is not None:
        return update_options_UI(ticker_input_value)
    # Returns initial data for the UI
    elif stock_symbol is not None:
        return update_options_UI(stock_symbol)
