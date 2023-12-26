"""

Fundamental Analysis

------------------------------------------------------------------------------
Program Description
-------------------------------------------------------------------------------

Analyze the long-term viability of a company based on their financials reported
to various sources and determines based on your personal criteria, whether they are
actually good companies, and if so, how, and when we should enter a position in them
if they are suitable for our strategies.

----------------------------------------------------------------------------------

"""
from sqlite3 import Error
import logging

import dash
import dash_bootstrap_components as dbc
from dash import html, dcc
import pandas as pd
import yfinance
from dash import callback
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate

# import app
import db
from utils import Utils as utils
from stock import MyStock

# Object that interacts with the Database
dbObj = db.DBConnection

# DB Queries
INDUSTRY_RATIOS = "./data/IndustryRatios_Aug22_2021.csv"
SECTOR_RATIOS = "./data/SQL/read/sector_analysis/SectorRatios.sql"

# Interacts with the yFinance API and deals with the Stock related information
StockObj = MyStock()
conn = None

# Connect to DB and Load Data
DB_FILE = dbObj.DB_FILE

try:
    conn = dbObj.create_connection(dbObj, db_file=DB_FILE)
    logging.info("Successfully Connected to the DB from Fundamental Analysis Page.")
    # stock_price_df = pd.read_sql('SELECT * FROM stock_price, stock WHERE stock_id= stock.id', conn)
except Error as e:
    logging.error(f"Error Occurred while connecting {DB_FILE} from the Fundamental Analysis Page | {e}")

# TODO Feature Enhancement add ability to automatically show how security of interest does against whatever the industry
#  3 year rolling averages are. Similar to Grad School Corp Finance Project.
companies_df = dbObj.select_table_data(dbObj, conn=conn, table_name='stock')
logging.info(f"Companies Dataframe {companies_df.head(20)}\n{companies_df.tail(20)}")

options = {'options': [], 'option_dates': []}

calls = []
puts = []
financials = []
balanceSheet = []
cashflows = []
earnings = []
stock_info = {}
stock_symbol = None

page_stock_info_ids = {}
page_stock_info_ids['stock-name'] = 'fundamentals-stock-name'
page_stock_info_ids['stock-title'] = 'fundamentals-stock-title'
page_stock_info_ids['stock-price'] = 'fundamentals-stock-price'
page_stock_info_ids['stock-sector'] = 'fundamentals-stock-sector'
page_stock_info_ids['stock-subsector'] = 'fundamentals-stock-subsector'

'''
This function will get the desired stock information from the API/DB and build the charts, graphs and tables needed.

:param stock_symbol is the Stock's ticker symbol
:returns All the data needed to update the dashboard with the choosen stock information
'''

# Registering the Dash Page
dash.register_page(__name__,
                   path='/fundamental-analysis',
                   name='Fundamental Analysis',
                   title='Stock Screener - Fundamental Analysis - ATB Analytics Group',
                   description='Fundamental Analysis of Stocks'
                   )

'''
Layout of our Dash Application - the Bones of the App 

'''

layout = dbc.Container(
    children=[

        dbc.Row(
            children=[

                html.Div(utils.get_sidebar("", companies_df, page_stock_info_ids)),
                html.Hr(),
                html.H1("Fundamental Analysis "),
                html.Br(),

                # Current Stock info wrapper
                html.Span(
                    id='fundamental-curr-info-wrapper',
                    className='curr-info-wrapper mb-5',
                    children=[
                        html.H2(
                            id='stock-name-fundamental',
                            className='mb-2 '
                        ),
                        html.H2(
                            id='stock-price-fundamental',
                            className='mb-2 '
                        ),
                    ]
                ),
            ]
        ),
        # Stock Price Chart - Candlestick Graph
        dbc.Row(
            children=[
                dbc.Col(
                    className='col-md-12',
                    children=[
                        dbc.Card(
                            className='mb-2 mt-2 pl-2 pr-2',
                            children=[
                                dbc.CardBody(
                                    children=[
                                        dcc.Loading(
                                            children=[
                                                html.H2(children=[f"Price Analysis"]),
                                                html.P(
                                                    children=[
                                                        "Stock Price with Bollinger Band Overlays."
                                                        "The Bollinger Bands act as a way to show, "
                                                        "rising or reversal trends on a security"
                                                    ]
                                                ),
                                                dcc.Graph(
                                                    id='fundamentals-candlestick-graph',
                                                    animate=True,
                                                ),
                                            ],
                                            type="circle",
                                            color=utils.get_random_color(utils)
                                        ),
                                    ]),
                            ]),
                    ]),
            ]
        ),

        dbc.Row(
            children=[
                dbc.Col(
                    dbc.Card(
                        className='col-md-12 mb-2 mt-2',
                        children=[
                            dbc.CardBody(
                                children=[
                                    html.H2(children=[
                                        "Business Summary"
                                    ]),
                                    html.Br(),
                                    dcc.Loading(
                                        children=[
                                            html.P(
                                                id='business-summary',
                                                children=[]
                                            ),
                                        ],
                                        type='circle',
                                        color=utils.get_random_color(utils)
                                    ),
                                ]
                            )

                        ]
                    ),
                    width=12,
                ),

                dbc.Col(
                    children=[
                        dbc.Card(
                            className='col-md-12 mb-2 mt-2',
                            children=[
                                dbc.CardBody(
                                    children=[
                                        html.H2(children=[
                                            "Financial Ratio's"
                                        ]),
                                        html.Br(),
                                        # html.P(
                                        #     children=[
                                        #         "Some Quick Financial Ratios to get Familiar. The value is the current"
                                        #         " value for the company vs the Industry for 2020 - 2015"
                                        #     ]),
                                        dcc.Loading(
                                            id='financial-ratios',
                                            type='circle',
                                            color=utils.get_random_color(utils)
                                        ),
                                    ]),
                            ]),
                    ],
                    width=12,
                ),

                dbc.Col(
                    className='col-md-12 mt-5',
                    children=[
                        dbc.Card(
                            className='mb-2 mt-2',
                            children=[
                                dbc.CardBody(
                                    children=[
                                        dcc.Loading(
                                            children=[
                                                html.H2(children=[
                                                    f"Margin Analysis"
                                                ]),
                                                html.P(
                                                    children=[
                                                        "Some Quick Financial Ratios to get Familiar. The value is the current"
                                                        " value for the company vs the Industry for 2020 - 2015"
                                                    ]),
                                                dcc.Graph(
                                                    id='profit-margin-chart',
                                                    animate=True,
                                                ),
                                            ],
                                            type='circle',
                                            color=utils.get_random_color(utils)
                                        ),
                                    ]),
                            ]),
                    ]),
            ]
        ),

        # Master Financials  - Table
        dbc.Row(
            children=[
                dbc.Col(
                    className="col-md-12",
                    children=[
                        dbc.Card(
                            className='mb-2 mt-2 pl-2 pr-2',
                            children=[
                                dbc.CardBody(
                                    children=[
                                        html.H2(f"Financials"),
                                        html.Br(),
                                        dcc.Loading(
                                            id='master-financial',
                                            type="circle",
                                            color=utils.get_random_color(utils)
                                        ),
                                    ]),
                            ]),
                    ],
                ),
                # dbc.Col(
                #
                #     children=[
                #         html.H2(["Generic Stock Info"]),
                #         utils.generate_generic_dash_datatable(utils, pd.DataFrame.from_dict(stock_info),
                #                                               id='stock-info-table')
                #     ])
            ]
        ),

        # Options
        # dbc.Row([
        #
        #     dbc.Col(
        #         className='col-md-12 mb-5',
        #         children=[
        #             dbc.Card(
        #                 className='mb-2 mt-2 pl-2 pr-2',
        #                 children=[
        #                     dbc.CardBody(
        #                         children=[
        #                             dcc.Loading(
        #                                 id="fundamentals-calls-table",
        #                                 children=[],
        #                                 type="circle",
        #                                  color=utils.get_random_color(utils)
        #                             ),
        #                         ]),
        #                 ]
        #             ),
        #         ]),
        #
        #     dbc.Col(
        #         className='col-md-12 mb-5',
        #         children=[
        #             dbc.Card(
        #                 className='mb-2 mt-2 pl-2 pr-2',
        #                 children=[
        #                     dbc.CardBody(
        #                         children=[
        #                             dcc.Loading(
        #                                 id="fundamentals-puts-table",
        #                                 type="circle",
        #                                  color=utils.get_random_color(utils)
        #                             ),
        #                         ]),
        #                 ]),
        #         ]),
        # ]),

    ]
)


def update_fundamentals_UI(stock_symbol):
    financials = []
    balanceSheet = []
    cashflows = []
    earnings = []
    master_financials = []
    financial_ratios = {}
    master_financials_df = {}
    candlestick_figure, calls, puts, data, call_datatable, put_datatable, = None, None, None, None, None, None
    company_name, stock_sector, stock_subsector, stock_info, profit_margin_figure = None, None, None, None, None

    # f = open('./data/SQL/read/company_information/CompanyInformation.sql', 'r')
    COMPANY_INFO_QRY = utils.open_and_read_sql(utils, './data/SQL/read/company_information/CompanyInformation.sql')
    logging.info(f"{stock_symbol} will be used with the COMPANY INFO QRY that is being Read\n{COMPANY_INFO_QRY}")
    # f.close()
    # COMPANY_INFO_QRY = "SELECT symbol, id, company, gics_sector, gics_subsector FROM stock"

    if stock_symbol is not None:

        try:
            # Connect to database
            conn = dbObj.create_connection(dbObj, DB_FILE)

            # Getting record for company - If no record returned we create one and get data.
            company_info_df = pd.read_sql_query(
                COMPANY_INFO_QRY + f" WHERE stock.symbol=\"{stock_symbol}\"", conn)

            if company_info_df.empty:
                # This takes us to adding the new symbol to our stocks table in the DB TODO needs to be handled better
                logging.error(
                    f"{COMPANY_INFO_QRY} WHERE stock.symbol = {stock_symbol} Company Info DF is Empty {company_info_df}")
                raise Error
            else:
                company_info_df = company_info_df.query(f'symbol == "{stock_symbol}"')
                stock_id = company_info_df['id'].values[0]
                stock_sector = company_info_df['gics_sector'].values[0]
                stock_subsector = company_info_df['gics_subsector'].values[0]
                company_name = company_info_df['company'].values[0]

            # Getting Stock Price Data from the DB by the Stock ID(FK)
            data = dbObj.select_record(dbObj, conn, 'stock_price', stock_id)

            # Getting the Stock Data for the Stock Symbol that is in our DB, but doesn't have price data.
            if data.empty:
                data = StockObj.get_ticker_all(stock_symbol=stock_symbol, add_ma=False, add_bb=False,
                                               add_mi=False)  # TODO API HIT

            # Adding Most Basic Technical Analysis indicators to Stock Price
            # Data and updating the data to the most current day.
            data = StockObj.get_ticker_all_add_df(dataframe=data, conn=conn, add_ma=True, add_mi=True,
                                                  add_bb=True)

        except Error as e:
            logging.error(f"Error Occurred while trying accessing the database | {e}")

            # Get the Stock Price Data from YFinance for the Newly Entered Ticker
            data = StockObj.get_ticker_all(stock_symbol=stock_symbol, add_ma=False, add_bb=False,
                                           add_mi=False)  # TODO API HIT

            # Gets the stocks info to be used in adding the stock to the master stock table
            stock_info = yfinance.Ticker(stock_symbol).info  # TODO API HIT CHECK IF IN DB FIRST
            stock_info = pd.DataFrame.from_dict(stock_info, orient='index').reset_index()
            stock_info.columns = ["Attribute", "Value"]
            stock_info.set_index('Attribute', inplace=True)

            try:
                sector = stock_info.loc['sector']
                sector = sector[0]
            except:
                try:
                    sector = stock_info.loc['exchange']
                    sector = sector[0]
                except:
                    sector = "SECTOR"

            try:
                company = stock_info.loc['longName']
                company = company[0]
            except:
                company = stock_symbol

            try:
                industry = stock_info.loc['industry']
                industry = industry[0]
            except:
                try:
                    industry = stock_info.loc['category']
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
            dbObj.insert_into_table(dbObj, conn, insert_sql, param_list)  # TODO DB HIT

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

            data.to_sql('stock_price', conn, if_exists='append', index=False)  # TODO DB HIT, check into chunkSizing

            data = StockObj.get_ticker_all_add_df(dataframe=data, conn=conn, stock_id=stock_id)  # TODO API HIT

            data.drop_duplicates(inplace=True)

        # Checking if the stock has data already for the financial if it does
        # it will have the data for all the financial statements.
        COMPANY_FINANCIALS_QRY = utils.open_and_read_sql(utils, './data/SQL/read/financial/CompanyFinancials.sql')
        financials_table_df = pd.read_sql_query(
            COMPANY_FINANCIALS_QRY + f'WHERE stock_financials.stock_id="{stock_id}"', conn)
        # + f" WHERE stock.symbol=\"{stock_symbol}\""

        # Getting and saving the last price that we have for the security
        price = data['Close'][data.shape[0] - 1].min()

        if financials_table_df.empty:

            options, financials, cashflows, earnings, balanceSheet, stock_info = StockObj.get_ticker_additional_information(
                stock_symbol=stock_symbol, stock_info=True, stock_id=stock_id, conn=conn,
                save_data=True)  # TODO API HIT : ALSO MOVE TO OTHER PAGE IN APP
        else:
            financials = financials_table_df
            financials.drop(columns=['stock_id', 'date', 'id'], inplace=True)
            financials.set_index('Year', inplace=True)
            financials = financials.transpose()

            COMPANY_CASHFLOW_QRY = utils.open_and_read_sql(utils, './data/SQL/read/cashflow/CompanyCashflow.sql')
            cashflows = pd.read_sql_query(
                COMPANY_CASHFLOW_QRY + f'WHERE stock_cashflows.stock_id="{stock_id}"', conn)
            cashflows.drop(columns=['stock_id', 'id', 'date'], inplace=True)
            cashflows.set_index('Year', inplace=True)
            cashflows = cashflows.transpose()

            COMAPANY_BALANCE_SHT_QRY = utils.open_and_read_sql(utils,
                                                               './data/SQL/read/balance_sheet/CompanyBalanceSheet.sql')

            balanceSheet = pd.read_sql_query(
                COMAPANY_BALANCE_SHT_QRY + f'WHERE stock_balance_sheet.stock_id="{stock_id}"', conn)
            balanceSheet.drop(columns=['stock_id', 'date', 'id'], inplace=True)
            balanceSheet.set_index('year', inplace=True)
            balanceSheet = balanceSheet.transpose()

            COMPANY_EARNINGS_QRY = utils.open_and_read_sql(utils, './data/SQL/read/financial/CompanyEarnings.sql')
            earnings = pd.read_sql_query(
                COMPANY_EARNINGS_QRY + f'WHERE stock_earnings.stock_id="{stock_id}"', conn)
            earnings.drop(columns=['stock_id', 'date', 'id'], inplace=True)
            earnings.set_index('Year', inplace=True)
            earnings.sort_index(ascending=False, inplace=True)
            earnings = earnings.transpose()

            stock_info = pd.read_sql_query(
                'SELECT * FROM stock_basic_info WHERE stock_basic_info.stock_id="{}"'.format(
                    stock_id), conn)
            stock_info.drop(columns=['stock_id', 'date', 'id'], inplace=True)
            stock_info = stock_info.T
            if len(stock_info) > 1:
                stock_info = stock_info.iloc[:, 0:1]

            stock_info.columns = ['Values']
            stock_info.index.rename('Attributes', inplace=True)

            options = StockObj.get_ticker_additional_information(
                stock_symbol=stock_symbol, stock_info=True, stock_id=stock_id, conn=conn,
                save_data=False, options=True, balanceSheet=False, earnings=False,
                financials=False, cashflows=False, )

        candlestick_figure = utils.generate_candlestick_graph_w_indicators(utils, data, stock_symbol)

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

    # Financials for ETF's will be empty.
    if financials.empty:
        pass
    else:
        master_financials_df = utils.generate_master_financials(utils, financials, balanceSheet, cashflows, earnings,
                                                                master_financials_df)
        master_financials = utils.generate_generic_dash_datatable(utils, master_financials_df,
                                                                  id='master-financial-data')

    # Should be Empty for ETFs

    if len(master_financials_df) > 0:
        master_financials_df.set_index('Financials', inplace=True)
        master_financials_df.sort_index(ascending=True, inplace=True)
        master_financials_df.fillna(0, inplace=True)
        master_financials_df.drop_duplicates(inplace=True)
        mfdf_cols = master_financials_df.columns

        dividendsPaid = 0
        inventory = 0
        sharesOutstanding = 1

        if 'Dividends Paid' in master_financials_df.index:
            dividendsPaid = master_financials_df[mfdf_cols[0]]['Dividends Paid']

        if 'Inventory' in master_financials_df.index:
            inventory = master_financials_df[mfdf_cols[0]]['Inventory']

        print(f"Stock_Info: {stock_info}\nStock_Info DataType: {type(stock_info)}")
        if type(stock_info) is dict:
            stock_info_cpy = stock_info

            keys = ['dayHigh', 'dayLow', 'exchange', 'fiftyDayAverage', 'lastPrice', 'lastVolume', 'marketCap',
                    'open', 'previousClose', 'quoteType', 'regularMarketPreviousClose', 'shares',
                    'tenDayAverageVolume', 'threeMonthAverageVolume', 'timezone', 'twoHundredDayAverage',
                    'yearChange', 'yearHigh', 'yearLow']
            stock_info_cpy = {x: stock_info[x] for x in keys if x in stock_info}
            stock_info_cpy = pd.DataFrame.from_dict(stock_info_cpy, orient='index')
            # stock_info = pd.DataFrame.from_dict(stock_info)
            stock_info_cpy.rename(index={'52WeekChange': 'fiftyTwoWeekChange'}, inplace=True)
            stock_info_cpy.columns = ['Values']
            # stock_info_cpy = stock_info_cpy.transpose()
            # stock_info_cpy.index.rename('Attributes', inplace=True)
            # stock_info_cpy.reset_index(inplace=True)
            stock_info = stock_info_cpy
        elif type(stock_info) is yfinance.scrapers.quote.FastInfo:
            stock_info_cpy = pd.DataFrame(stock_info)
            stock_info_cpy = stock_info_cpy.to_dict()

            keys = ['dayHigh', 'dayLow', 'exchange', 'fiftyDayAverage', 'lastPrice', 'lastVolume', 'marketCap',
                    'open', 'previousClose', 'quoteType', 'regularMarketPreviousClose', 'shares',
                    'tenDayAverageVolume', 'threeMonthAverageVolume', 'timezone', 'twoHundredDayAverage',
                    'yearChange', 'yearHigh', 'yearLow']
            stock_info_cpy = {x: stock_info[x] for x in keys if x in stock_info}
            stock_info_cpy = pd.DataFrame.from_dict(stock_info_cpy, orient='index')
            # stock_info = pd.DataFrame.from_dict(stock_info)
            # stock_info_cpy.rename(index={'52WeekChange': 'fiftyTwoWeekChange'}, inplace=True)
            stock_info_cpy.columns = ['Values']
            # stock_info_cpy = stock_info_cpy.transpose()
            # stock_info_cpy.index.rename('Attributes', inplace=True)
            # stock_info_cpy.reset_index(inplace=True)
            stock_info = stock_info_cpy
        else:
            pass

        if 'shares' in stock_info.index:
            if stock_info['Values']['shares'] == None:
                sharesOutstanding = 1
            else:
                sharesOutstanding = stock_info['Values']['shares']

        ebit = 0
        profit_combined = 0
        depreciation_combined = 0
        total_capex = 0
        revenue_combined = 0
        market_cap = 0
        currentRatio = 0
        returnOnEquity = 0
        returnOnAssets = 0
        bookValue = 0
        priceToBook = 0
        cashRatio = 0
        quickRatio = 0
        grossProfit = 0
        currAccExp = 0
        preTaxIncome = 0
        netIncome = 0
        depreciation = 0
        capEx = 0
        totAssets = 0
        totLiab = 0

        mf_years = master_financials_df.columns.size

        profit_margin_chart_dict = {}

        for col in range(0, mf_years):
            if 'EBIT' in master_financials_df.index or 'Ebit' in master_financials_df.index:
                if 'Ebit' in master_financials_df.index:
                    ebit += master_financials_df[mfdf_cols[col]]['Ebit']
                else:
                    ebit += master_financials_df[mfdf_cols[col]]['EBIT']

            if 'Net Income' in master_financials_df.index:
                netIncome = master_financials_df[mfdf_cols[col]]['Net Income']
            else:
                netIncome = 1

            if 'Depreciation' in master_financials_df.index:
                depreciation = master_financials_df[mfdf_cols[col]]['Depreciation']
                depreciation_combined += depreciation

            if 'Capital Expenditures' in master_financials_df.index:
                capEx = master_financials_df[mfdf_cols[col]]['Capital Expenditures']
                total_capex += capEx

            if 'Revenue' in master_financials_df.index or 'revenue' in master_financials_df.index:
                if 'revenue' in master_financials_df.index:
                    master_financials_df.rename({'revenue': 'Revenue'}, inplace=True)
                    revenue = master_financials_df[mfdf_cols[col]]['Revenue']
                    revenue_combined += revenue
                else:
                    revenue = master_financials_df[mfdf_cols[col]]['Revenue']
                    revenue_combined += revenue
            else:
                revenue = 1

            if 'Gross Profit' in master_financials_df.index:
                grossProfit = master_financials_df[mfdf_cols[col]]['Gross Profit']
                profit_combined += grossProfit
            else:
                if 'Cost of Goods Sold' in master_financials_df.index:
                    grossProfit = revenue - master_financials_df[mfdf_cols[col]]['Cost Of Goods Sold']
                    grossProfit = grossProfit / revenue
                    profit_combined += grossProfit
                else:
                    grossProfit = revenue
                    profit_combined += grossProfit

            if 'Pretax Income' in master_financials_df.index:
                preTaxIncome = master_financials_df[mfdf_cols[col]]['Pretax Income']
            else:
                if 'Income Before Tax' in master_financials_df.index:
                    preTaxIncome = master_financials_df[mfdf_cols[col]]['Income Before Tax']
                else:
                    preTaxIncome = revenue

            profit_margin_chart_dict[mfdf_cols[col]] = {
                'profit margin': (netIncome / revenue) * 100,

                'net profit margin': ((revenue - currAccExp) / revenue) * 100,

                'operating margin':
                    (preTaxIncome / revenue) * 100,
                'gross margin':
                    (grossProfit / revenue) * 100,
            }

        if profit_margin_chart_dict:
            pm_chart_df = pd.DataFrame(profit_margin_chart_dict).transpose()
            pm_chart_df.columns = ['Profit Margin', 'Net Profit Margin', 'Operating Margin', 'Gross Margin']
            pm_chart_df.index.rename('Years', inplace=True)
            pm_chart_df.reset_index(inplace=True)
            pm_chart_df.sort_index(ascending=True, inplace=True)

            sector_pm_sql = dbObj.create_sql_string(dbObj, SECTOR_RATIOS)
            sector_pm_df = pd.read_sql_query(sector_pm_sql, conn)
            sector_pm_df = sector_pm_df.query('gics_sector=="{}"'.format(stock_sector), inplace=False)
            # sector_pm_df = sector_pm_df.transpose()
            sector_pm_df.drop('gics_sector', axis=1, inplace=True)
            sector_pm_df.set_index('Year', inplace=True)
            sector_pm_df.index.rename("Years", inplace=True)
            sector_pm_df.rename(columns={"gross_profit_margin": "Gross Margin", "profit_margin": "Profit Margin",
                                         "operating_margin": "Operating Margin"}, inplace=True)
            sector_pm_df.reset_index(inplace=True)
            sector_pm_df.sort_index(ascending=False, inplace=True)

            # margin_df = [pm_chart_df, sector_pm_df]
            # # margin_df_1 = pd.merge(left=pm_chart_df, right=sector_pm_df, how='inner')
            # margin_df = pd.concat(margin_df, ignore_index=True)
            # margin_df.drop(columns=['return_on_assets', 'return_on_equity'], inplace=True)
            # margin_df.drop_duplicates(subset=['Years'], inplace=True)
            # margin_df.sort_index(ascending=True, inplace=True)

            profit_margin_figure = utils.generate_bar_and_line_graph(utils, pm_chart_df, sector_pm_df,
                                                                     title='Margin Analysis - Company vs Industry',
                                                                     x_column='Years',
                                                                     y_column='Profit Margin')

            # profit_margin_figure = utils.generate_bar_graph(pm_chart_df, title='Margin Analysis', x_column='Years',
            #                                                 y_column='Profit Margin')  # WORKING CODE
        if 'Tax Rate for Calcs' in master_financials_df.index:
            eff_tax_rate = master_financials_df[mfdf_cols[0]]['Tax Rate For Calcs']
        else:
            if 'Income Tax Expense' in master_financials_df.index:
                if 'Earnings' in master_financials_df.index:
                    eff_tax_rate = master_financials_df[mfdf_cols[0]]['Income Tax Expense'] / \
                                   master_financials_df[mfdf_cols[0]]['Earnings']
                elif 'Revenue' in master_financials_df.index:
                    eff_tax_rate = master_financials_df[mfdf_cols[0]]['Income Tax Expense'] / \
                                   master_financials_df[mfdf_cols[0]]['Revenue']
                elif 'Total Revenue' in master_financials_df.index:
                    eff_tax_rate = master_financials_df[mfdf_cols[0]]['Income Tax Expense'] / \
                                   master_financials_df[mfdf_cols[0]]['Total Revenue']

            else:
                eff_tax_rate = 1
        avg_ebit = ebit / mf_years
        avg_profit = profit_combined / mf_years
        avg_depreciation = depreciation_combined / mf_years
        avg_revenue = revenue_combined / mf_years

        if avg_revenue <= 0:
            ebit_margin = avg_ebit / 1
        else:
            ebit_margin = avg_ebit / avg_revenue

        revenueCheck = utils.checkForColinDF(utils, master_financials_df, 'Revenue')
        ebitCheck = utils.checkForColinDF(utils, master_financials_df, 'Ebit') or utils.checkForColinDF(
            utils,
            master_financials_df,
            'EBIT')
        netIncomeCheck = utils.checkForColinDF(utils, master_financials_df, 'Net Income')
        incomeBeforeTax = utils.checkForColinDF(utils, master_financials_df, 'Income Before Tax')

        if revenueCheck:
            income_growth_rate = (((master_financials_df[mfdf_cols[0]]['Revenue'] /
                                    master_financials_df[mfdf_cols[mf_years - 1]]['Revenue']) * (
                                           1 / mf_years)) - 1) * 100
        else:
            if ebitCheck:
                if 'Ebit' in master_financials_df.index:
                    income_growth_rate = (((master_financials_df[mfdf_cols[0]]['Ebit'] /
                                            master_financials_df[mfdf_cols[mf_years - 1]]['Ebit']) * (
                                                   1 / mf_years)) - 1) * 100
                else:
                    income_growth_rate = (((master_financials_df[mfdf_cols[0]]['EBIT'] /
                                            master_financials_df[mfdf_cols[mf_years - 1]]['EBIT']) * (
                                                   1 / mf_years)) - 1) * 100
            elif netIncomeCheck:
                if 'Net Income' in master_financials_df.index:
                    income_growth_rate = (((master_financials_df[mfdf_cols[0]]['Net Income'] /
                                            master_financials_df[mfdf_cols[mf_years - 1]]['Net Income']) * (
                                                   1 / mf_years)) - 1) * 100
            elif incomeBeforeTax:
                income_growth_rate = (((master_financials_df[mfdf_cols[0]]['Income Before Tax'] /
                                        master_financials_df[mfdf_cols[mf_years - 1]]['Income Before Tax']) * (
                                               1 / mf_years)) - 1) * 100
            else:
                income_growth_rate = 1
        if revenueCheck:
            normalized_ebit = master_financials_df[mfdf_cols[0]]['Revenue'] * ebit_margin
        elif ebitCheck:
            if 'Ebit' in master_financials_df.index:
                normalized_ebit = master_financials_df[mfdf_cols[0]]['Ebit'] * ebit_margin
            else:
                normalized_ebit = master_financials_df[mfdf_cols[0]]['EBIT'] * ebit_margin
        elif netIncomeCheck:
            normalized_ebit = master_financials_df[mfdf_cols[0]]['Net Income'] * ebit_margin
        elif incomeBeforeTax:
            normalized_ebit = master_financials_df[mfdf_cols[0]]['Income Before Tax'] * ebit_margin

        after_tax_normalized_ebit = normalized_ebit * (1 - eff_tax_rate)
        adj_depreciation = ((1 / mf_years) * eff_tax_rate) * avg_depreciation
        normalized_profit = after_tax_normalized_ebit + adj_depreciation
        maintenance_Capex = total_capex * (1 - income_growth_rate)
        avg_capex = maintenance_Capex / mf_years

        adj_earnings = normalized_profit - avg_capex

        liabNetMinorityInterest = utils.checkForColinDF(utils, master_financials_df,
                                                        'Total Liabilities Net Minority Interest')
        totAssetsCheck = utils.checkForColinDF(utils, master_financials_df, 'Total Assets')
        totLiabCheck = utils.checkForColinDF(utils, master_financials_df, 'Total Liab')

        if liabNetMinorityInterest and totAssetsCheck:
            totLiab = master_financials_df[mfdf_cols[0]]['Total Liabilities Net Minority Interest']
            total_equity = master_financials_df[mfdf_cols[0]]['Total Assets'] - totLiab  # Shareholders Equity
        elif totAssetsCheck and totLiabCheck:
            totLiab = master_financials_df[mfdf_cols[0]]['Total Liab']
            total_equity = master_financials_df[mfdf_cols[0]]['Total Assets'] - totLiab  # Shareholders Equity
        else:
            totLiab = 1

        if 'Long Term Debt' in master_financials_df.index and 'Short Long Term Debt' in master_financials_df.index:
            total_debt = master_financials_df[mfdf_cols[0]]['Long Term Debt'] + master_financials_df[mfdf_cols[0]][
                'Short Long Term Debt']
        elif 'Long Term Debt' in master_financials_df.index and 'Short Long Term Debt' not in master_financials_df.index:
            total_debt = master_financials_df[mfdf_cols[0]]['Long Term Debt']
        elif 'Short Long Term Debt' in master_financials_df.index and 'Long Term Debt' not in master_financials_df.index:
            total_debt = master_financials_df[mfdf_cols[0]]['Short Long Term Debt']
        else:
            total_debt = 0

        total_value = total_equity + total_debt
        equity_percentage = total_equity / total_value
        debt_percentage = total_debt / total_value
        risk_free_return = 1.425481928  # As of Aug 28 2021 is usually the same as the 10 yr Treasury Bond updated daily

        if stock_info is not None and type(stock_info) != str:
            # beta = stock_info['beta'] if stock_info['beta'] is not None else 0

            if 'Interest Expense' in master_financials_df.index:
                yield_to_maturity = master_financials_df[mfdf_cols[0]]['Interest Expense'] * (1 - eff_tax_rate)
            else:
                yield_to_maturity = 1 * (1 - eff_tax_rate)

            # (E/V x Re)  +  ((D/V x Rd)  x  (1 – T))
            wacc = (equity_percentage * risk_free_return) + ((debt_percentage * yield_to_maturity) * (1 - eff_tax_rate))
            risk_free_return
            gross_earnings_power_val = adj_earnings / wacc
            earnings_power_value = gross_earnings_power_val + total_equity - total_debt

            epvPerShare = earnings_power_value / sharesOutstanding

            market_cap = price * sharesOutstanding

            returnOnInvestedCapital = (netIncome - dividendsPaid) / total_value

            # Financial Ratios that needed to be calculated.
            earningsPerShare = (netIncome + dividendsPaid) / sharesOutstanding
            priceToEarnings = price / earningsPerShare  # Should be < 15

            if stock_info['Values']['quoteType'] != 'ETF':
                if 'Total Current Assets' in master_financials_df.index:
                    if type(master_financials_df[mfdf_cols[0]]['Total Current Assets']) == pd.Series:
                        currentRatio = master_financials_df[mfdf_cols[0]]['Total Current Assets'][1] / \
                                       master_financials_df[mfdf_cols[0]]['Total Current Liabilities']

                        quickRatio = (master_financials_df[mfdf_cols[0]]['Total Current Assets'][1] - inventory) / \
                                     master_financials_df[mfdf_cols[0]][
                                         'Total Current Liabilities']

                        netCurrAssetVal = master_financials_df[mfdf_cols[0]][
                                              'Total Current Assets'][1] - master_financials_df[mfdf_cols[0]][
                                              'Total Current Liabilities'] + dividendsPaid

                    else:
                        if 'Current Assets' in master_financials_df.index:
                            master_financials_df.rename('Current Assets', 'Total Current Assets', inplace=True)

                        currentRatio = master_financials_df[mfdf_cols[0]]['Total Current Assets'] / \
                                       master_financials_df[mfdf_cols[0]]['Total Current Liabilities']

                        quickRatio = (master_financials_df[mfdf_cols[0]]['Total Current Assets'] - inventory) / \
                                     master_financials_df[mfdf_cols[0]][
                                         'Total Current Liabilities']

                        netCurrAssetVal = master_financials_df[mfdf_cols[0]][
                                              'Total Current Assets'] - master_financials_df[mfdf_cols[0]][
                                              'Total Current Liabilities'] + dividendsPaid
                else:
                    if 'Current Assets' in master_financials_df.index:
                        if 'Current Liabilities' in master_financials_df.index:
                            master_financials_df.rename({'Current Assets': 'Total Current Assets',
                                                         'Current Liabilities': 'Total Current Liabilities'},
                                                        inplace=True)
                        else:
                            master_financials_df.rename({'Current Assets': 'Total Current Assets'}, inplace=True)

                        currentRatio = master_financials_df[mfdf_cols[0]]['Total Current Assets'] / \
                                       master_financials_df[mfdf_cols[0]]['Total Current Liabilities']

                        quickRatio = (master_financials_df[mfdf_cols[0]]['Total Current Assets'] - inventory) / \
                                     master_financials_df[mfdf_cols[0]][
                                         'Total Current Liabilities']

                        netCurrAssetVal = master_financials_df[mfdf_cols[0]][
                                              'Total Current Assets'] - master_financials_df[mfdf_cols[0]][
                                              'Total Current Liabilities'] + dividendsPaid

                        cashRatio = master_financials_df[mfdf_cols[0]]['Cash And Cash Equivalents'] / \
                                    master_financials_df[mfdf_cols[0]][
                                        'Total Current Liabilities']
                    else:
                        netCurrAssetVal = 1

            else:

                currentRatio = master_financials_df[mfdf_cols[0]]['Total Current Assets'] / \
                               master_financials_df[mfdf_cols[0]]['Total Current Liabilities']

                quickRatio = (master_financials_df[mfdf_cols[0]]['Total Current Assets'] - inventory) / \
                             master_financials_df[mfdf_cols[0]][
                                 'Total Current Liabilities']

                netCurrAssetVal = master_financials_df[mfdf_cols[0]][
                                      'Total Current Assets'] - master_financials_df[mfdf_cols[0]][
                                      'Total Current Liabilities'] + dividendsPaid

                cashRatio = master_financials_df[mfdf_cols[0]]['Cash'] / master_financials_df[mfdf_cols[0]][
                    'Total Current Liabilities']

            priceToNCAV = netCurrAssetVal / price

            NCAVperShare = netCurrAssetVal / sharesOutstanding
            bookValue = (total_equity / sharesOutstanding)  # Should be < 2
            priceToBook = price / bookValue
            debtToEquity = totLiab / total_equity
            returnOnAssets = netIncome / master_financials_df[mfdf_cols[0]][
                'Total Assets']
            returnOnEquity = netIncome / total_equity

            if not stock_info.empty:

                financial_ratios = {

                    'marketCapitalization': market_cap,

                    'bookValue': bookValue,

                    'currentRatio': currentRatio,

                    'cashRatio': cashRatio,

                    'quickRatio': quickRatio,

                    'priceToBook': priceToBook,

                    'debtToEquity': debtToEquity,

                    'returnOnEquity': returnOnEquity,

                    'returnOnAssets': returnOnAssets,

                    'returnOnInvestedCapital': returnOnInvestedCapital,

                    'earningsPerShare': earningsPerShare,

                    'priceToEarnings': priceToEarnings,

                    'netCurrentAssetValue': netCurrAssetVal,

                    'NCAVperShare': NCAVperShare,

                    'priceToNCAV': priceToNCAV,

                    'wacc': wacc,

                    'earningsPowerValue': earnings_power_value,

                    'epvPerShare': epvPerShare,

                    'effectiveTaxRate': eff_tax_rate,

                }
            else:
                financial_ratios = {}
    else:

        stock_info_cpy = stock_info
        gross_margin = 0
        profit_margin = 0
        operating_margin = 0
        net_profit_margin = 0

        profit_margin_chart_dict = {
            '2021': {
                'gross margin': gross_margin,
                'profit margin': profit_margin,
                'net profit margin': net_profit_margin,
                'operating margin': operating_margin,
            },
        }

        if profit_margin_chart_dict:
            pm_chart_df = pd.DataFrame(profit_margin_chart_dict).transpose()
            pm_chart_df.columns = ['Profit Margin', 'Net Profit Margin', 'Operating Margin', 'Gross Margin']
            pm_chart_df.index.rename('Years', inplace=True)
            pm_chart_df.reset_index(inplace=True)
            pm_chart_df.sort_index(ascending=True, inplace=True)

            profit_margin_figure = utils.generate_bar_graph(utils, pm_chart_df, 'ETF Margin Analysis', x_column='Years',
                                                            y_column='Profit Margin')

        keys = ['sector', 'fullTimeEmployees', 'longBusinessSummary', 'website', 'city', 'state', 'zip',
                'industry', 'targetLowPrice', 'targetMeanPrice', 'targetHighPrice', 'shortName', 'longName',
                'quoteType', 'symbol', '52weekChange', 'sharesOutstanding', 'sharesShort',
                'SandP52WeekChange', 'yield', 'beta', 'lastDividendDate', 'twoHundredDayAverage',
                'dividendRate',
                'exDividendDate', 'fiftyTwoWeekHigh', 'fiftyTwoWeekLow', 'dividendYield',
                'nextFiscalYearEnd']
        stock_info_cpy = {x: stock_info[x] for x in keys if x in stock_info}
        stock_info_cpy = pd.DataFrame.from_dict(stock_info_cpy, orient='index')
        # stock_info = pd.DataFrame.from_dict(stock_info)
        # stock_info_cpy.rename(index={'52WeekChange': 'fiftyTwoWeekChange'}, inplace=True)
        stock_info_cpy.columns = ['Values']
        # stock_info_cpy = stock_info_cpy.T
        # stock_info_cpy.index.rename('Attributes', inplace=True)
        # stock_info_cpy.reset_index(inplace=True)
        stock_info = stock_info_cpy

    financialRatioDF = pd.DataFrame(financial_ratios, index=[0]).transpose()
    financialRatioDF.columns = ['Value']
    financialRatioDF.index.rename('Financials', inplace=True)
    financialRatioDF.reset_index(inplace=True)

    industyRatioDF = pd.read_csv(INDUSTRY_RATIOS)  # TODO Update to 2023 Data.
    financialRatioDF = pd.merge(financialRatioDF, industyRatioDF, how='left', left_on=financialRatioDF['Financials'],
                                right_on=industyRatioDF['Industry Ratios'])

    financialRatioDF.drop(['Industry Ratios', 'key_0'], axis=1, inplace=True)

    financial_ratios = utils.generate_generic_dash_datatable(utils, financialRatioDF, id='financial-ratios-data')

    stock_price = "${:.2f}".format(price)
    business_summary = "Company Business Summary or what they do in their own words. Can be found in Annual Reports."
    if "longBusinessSummary" in stock_info.index:
        business_summary = stock_info['Values']['longBusinessSummary']

    logging.info(
        "{}\n{}\n{}\n{}\n{}".format(company_name, stock_symbol, stock_price, stock_sector, stock_subsector, stock_info))

    logging.info(financialRatioDF)
    # return candlestick_figure, call_datatable, put_datatable, master_financials, financial_ratios, business_summary, profit_margin_figure

    return company_name, stock_price, candlestick_figure, master_financials, financial_ratios, business_summary, profit_margin_figure


'''

Dash Callback that allows for interactivity between UI, API and DB

'''


@callback(
    Output('stock-name-heading', 'children'),
    Output('master-financial-heading', 'children'),
    Input('stock-storage', 'data'),
    State('stock-storage', 'data'),
    suppress_callback_exceptions=True
)
def update_layout_w_storage_data(data, data1):
    if data is None or len(data) == 0:
        raise PreventUpdate

    stockNameHeading = data['company']
    masterFinancialsHeading = data['company']

    return stockNameHeading, masterFinancialsHeading


# TODO Break into separate callbacks for each section of the application so
#  if one it doesnt break the entire application.
@callback(
    Output('stock-name-fundamental', 'children'),
    Output('stock-price-fundamental', 'children'),
    Output('fundamentals-candlestick-graph', 'figure'),
    # Output('fundamentals-calls-table', 'children'),
    # Output('fundamentals-puts-table', 'children'),
    # Output('fundamentals-stock-name', 'children'),
    # Output('fundamentals-stock-title', 'children'),
    # Output('fundamentals-stock-price', 'children'),
    # Output('fundamentals-stock-sector', 'children'),
    # Output('fundamentals-stock-subsector', 'children'),
    Output('master-financial', 'children'),
    Output('financial-ratios', 'children'),
    Output('business-summary', 'children'),
    Output('profit-margin-chart', 'figure'),
    # Input('get_stock_btn', 'n_clicks'),
    Input('ticker_input', 'value'),
    Input('companies_dropdown', 'value'),
    Input('stock-storage', 'data'),
    # [Input(str(stock_symbol + "-" + str(options['option_dates'][i])), 'n_clicks') for i in
    #  range(0, len(options['option_dates']))],
    State('ticker_input', 'value'),
    # State('companies-dropdown', 'value'),
    suppress_callback_exceptions=True,
    prevent_initial_callbacks=True,
)
def update_layout(ticker_input_value, companies_dropdown, ticker_input, data):
    # Returns the updated information after entering a Stock Ticker into the Input Box

    if type(ticker_input) is dict:
        logging.info(f"{ticker_input} is a dict, setting data equal to {ticker_input} and ticker_input will be "
                     f"reset to None")
        data = ticker_input
        ticker_input = None

    if data is not None:

        stock_symbol = data['stock']
    else:
        stock_symbol = utils.generate_random_stock(utils)
        # ticker_input = ticker_input

        # NOT needed but keep for ex purposes.access Callback Context information to know which button from the options button list that was generated
        #  and see which button was clicked and get that option chain and data.
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

    if companies_dropdown is not None and companies_dropdown != "Company Ticker Symbol":
        if companies_dropdown:
            stock_id = None

            # TODO DRY is not being followed here this is also in the update_fundamentals_function as well
            try:
                conn = dbObj.create_connection(dbObj, DB_FILE)

                # Getting single record for company - If no record returned we create and get data.
                company_info_df = pd.read_sql_query(
                    'SELECT symbol, id, company FROM stock WHERE stock.company="{}"'.format(companies_dropdown),
                    conn)

                if company_info_df.empty:
                    # This takes us to adding the new symbol to our stocks table in the DB
                    raise Error
                else:
                    stock_symbol = company_info_df['symbol'][0]

                    return update_fundamentals_UI(stock_symbol)

            except Error as e:
                logging.error(f"Error Occurred | {e}")
    elif ticker_input_value is not None:

        return update_fundamentals_UI(ticker_input_value)

        # Returns initial data for the UI
    elif stock_symbol is not None:
        return update_fundamentals_UI(stock_symbol)
