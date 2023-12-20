# Raw data comes from yfinance - add any other packages that provide data here
# yfinance documentation https://pypi.org/project/yfinance/
# Plotly  Documentation https://plotly.com/python/
"""
Stocks

------------------------------------------------------------------------------
Program Description
-------------------------------------------------------------------------------

This is all about the stocks and interacting with the API's that provide the
data necessary to power our application.

----------------------------------------------------------------------------------


"""
import sqlite3

import sqlalchemy

import config
import datetime as dt
import sys
from sqlite3 import Error
import logging

import pandas as pd
import talib as ta
import yfinance as yf

# import app
import db
import utils

'''
    The My Stock Class has the following responsibilities around the Stock chosen and does all the interacting with the 
    yFinance API. 
    
    The Main Responsibility of this class it to interact with the yFinance API and has the following capabilities.
        - Will Get the Stock Ticker information
        - Add Moving Averages to the Stock Ticker Information
        - Add Bolling Bands to the Stock Ticker Information 
        - Calculate the RSI for the Stock Ticker
    
'''


class MyStock:
    # ST_PERIOD = app.DEFAULTS.stock_defaults['technical']['ST_PERIOD']
    # LG_PERIOD = app.DEFAULTS.stock_defaults['technical']['LG_PERIOD']
    # BB_MULTIPLIER = app.DEFAULTS.stock_defaults['technical']['BB_MULTIPLIER']
    #
    # RSI_PERIOD = app.DEFAULTS.stock_defaults['technical']['RSI_PERIOD']
    #
    # MA50 = 50
    # MA72 = 72
    # MA200 = 200
    #
    # MACD_FAST_PD = 12
    # MACD_SLOW_PD = 26
    # MACD_SIGNAL_LINE = 9

    def __init__(self):
        defaults = config.ScreenerConfig()

        self.ST_PERIOD = defaults.stock_defaults['technical']['ST_PERIOD']
        self.LG_PERIOD = defaults.stock_defaults['technical']['LG_PERIOD']
        self.BB_MULTIPLIER = defaults.stock_defaults['technical']['BB_MULTIPLIER']

        self.RSI_PERIOD = defaults.stock_defaults['technical']['RSI_PERIOD']
        self.MA50 = defaults.stock_defaults['technical']['MA50']
        self.MA72 = defaults.stock_defaults['technical']['MA72']
        self.MA200 = defaults.stock_defaults['technical']['MA200']
        self.MACD_FAST_PD = defaults.stock_defaults['technical']['MACD_FAST_PD']
        self.MACD_SLOW_PD = defaults.stock_defaults['technical']['MACD_SLOW_PD']
        self.MACD_SIGNAL_LINE = defaults.stock_defaults['technical']['MACD_SIGNAL_LINE']

    '''
    Converts Timestamp column's to only be the year.
    :param: Pandas Dataframe Object containing the Data
    :param: inplace if you want the columns conversions to be done inplace.
    :returns: the Dataframe with the converted timestamps to year

    '''

    def convert_timestamp_columns(self, dataframe, inplace=True):
        for c in dataframe.columns:
            if type(c) == pd.Timestamp:
                dataframe.rename(columns={c: str("{}".format(c.year))}, inplace=inplace)
                # dataframe.reset_index()
            else:
                pass

        return dataframe

    '''
    Preps the additional raw data from yFinance to be Transformed and Loaded into the database.
    
    :param add_data: Panadas dataframe that has the additional data to be added to the stock price table
    :param conn: SQLite3 Connection object that has an open connection to database.
    :param stock_id: Id of the stock in the Stock table. 
    
    :returns Pandas dataframe with all data - included newly transformed data
    '''

    def prep_dataframe(self, add_data, conn, stock_id):
        add_data['date'] = pd.to_datetime(add_data.index)
        add_data.rename_axis("Date", axis='index', inplace=True)
        add_data.rename(columns={
            'Adj Close': 'adjusted_close'
        }, inplace=True)
        add_data['stock_id'] = stock_id

        logging.info("{}{}{}".format(add_data.head(), "\\n", add_data.tail()))

        # TODO Utilize the DB Connetion Object for this
        add_data.to_sql('stock_price', conn, if_exists='append', index=False)

        # Getting all data for stock including the recently updated data
        add_data = pd.read_sql_query("SELECT * FROM stock_price WHERE stock_id = '{}'".format(stock_id), conn)

        return add_data

    '''
    :param Pandas Dataframe
    :param stock_id
    
    :returns Pandas Dataframe
    '''

    def prep_dataframe_to_save(self, dataframe, stock_id):
        df_to_save = dataframe.copy()
        df_to_save.fillna(0, inplace=True)
        df_to_save = self.convert_timestamp_columns(df_to_save)
        df_to_save = df_to_save.T
        df_to_save.index.rename("Year", inplace=True)
        df_to_save.reset_index(inplace=True)
        df_to_save['stock_id'] = stock_id
        df_to_save['date'] = pd.Timestamp.now()

        return df_to_save

    '''
    Retrieves the stock ticker symbol to be passed into yFinance
    :param stock_id : Id of the Stock in the Stock table

    :param conn : SQLite3 Connection Object 
    
    :returns Stock Symbol
    '''

    def get_ticker_symbol(self, stock_id, conn):
        stock_symbol = None
        data = pd.read_sql_query("SELECT * FROM STOCK WHERE id='{}'".format(stock_id), con=conn)
        stock_symbol = data['symbol'][0]

        return stock_symbol

    '''
    This function returns all the data that is needed to analyze a stock using the yFinance API, including
    options, financial, cashflows, earnings, and balance sheets.

    :param stock_symbol:
    :param options:
    :param financial:
    :param cashflows:
    :param earnings:
    :param balanceSheet:
    :param save_data:
    :return:

        :returns a Dictionary for the Options( Dict holds puts and calls, and the exp dates), financial,
        cashflows, earnings, and balanceSheet are all pandas dataframes


    '''

    def get_ticker_additional_information(self, stock_symbol='^GSPC', options=True, financials=True, cashflows=True,
                                          earnings=True, balanceSheet=True, stock_info=False, save_data=False,
                                          stock_id=None, conn=None):

        data = yf.Ticker(ticker=stock_symbol)

        # Note as of yFinan ce 0.2.22 earnings is now lumped into the financial, so instead of being separate,
        # it will have to be created from the Financials Data.
        if data is not None:
            if options and financials and cashflows and balanceSheet:
                balanceSheet, cashflows, earnings, financials = {}, {}, {}, {}
                option_chain = {}
                # option_chain = data.option_chain(data.options[0])
                # Get's the option chain expiration dates.

                try:
                    data.options
                    option_chain = data.option_chain()
                    option_chain = {'options': option_chain, 'option_dates': data.options}

                except Exception as e:
                    logging.error(
                        f"Error Occurred when trying to get the option_chain and options from Ticker Data |{e}")

                financials = data.financials
                cashflows = data.cashflow
                if financials is not None and financials.empty is not True:
                    # Need to get the revenue and after-tax net income to match the pervious earnings information
                    earnings = financials.loc[['Net Income', 'Total Revenue']]
                    earnings = earnings.rename({'Net Income': 'earnings', 'Total Revenue': 'revenue'})
                # earnings = data.earnings
                balanceSheet = data.balance_sheet

                if stock_info:
                    stock_info = {}
                    stock_info = data.fast_info  # can also use basic_info or history_metadata
                    stock_info_cpy = stock_info

                    keys = ['dayHigh', 'dayLow', 'exchange', 'fiftyDayAverage', 'lastPrice', 'lastVolume', 'marketCap',
                            'open', 'previousClose', 'quoteType', 'regularMarketPreviousClose', 'shares',
                            'tenDayAverageVolume', 'threeMonthAverageVolume', 'timezone', 'twoHundredDayAverage',
                            'yearChange', 'yearHigh', 'yearLow']
                    stock_info_cpy = {x: stock_info[x] for x in keys if x in stock_info}
                    stock_info_cpy = pd.DataFrame.from_dict(stock_info_cpy, orient='index')
                    stock_info_cpy.loc['symbol', :] = data.history_metadata['symbol']

                    # stock_info = pd.DataFrame.from_dict(stock_info)
                    # stock_info_cpy.rename(index={'52WeekChange': 'fiftyTwoWeekChange'}, inplace=True)
                    stock_info_cpy.columns = ['Values']
                    stock_info_cpy = stock_info_cpy.T
                    stock_info_cpy.index.rename('Attributes', inplace=True)
                    stock_info_cpy.reset_index(inplace=True)
                    stock_info_cpy.drop(['Attributes'], axis=1, inplace=True)
                    stock_info_cpy['stock_id'] = stock_id
                    stock_info_cpy['date'] = pd.Timestamp.now()

                #  Save data to database, will need to get the stock_id from the DB to commit both
                #  price and options data to db

                if save_data and stock_info['quoteType'] != 'ETF':
                    # Establish Connection to DB
                    try:
                        conn
                        logging.info("Connection to database established")
                    except Error as e:
                        logging.error(e)
                        logging.info(f"Trying to establish connection with DB")
                        conn = db.DBConnection.create_connection()
                        if conn is not None:
                            logging.info(f"{conn} was successfully established with db")

                    # Creating a copy of the dataframes to add necessary data before saving into DB
                    balanceSheet_cpy = self.prep_dataframe_to_save(balanceSheet.rename({
                        'Total Liabilities Net Minority Interest': 'Total Liab',
                        'Other Short Term Investments': 'Short Term Investments',
                        'Current Liabilities': 'Total Current Liabilities',
                        'Current Assets': 'Total Current Assets'
                    }), stock_id)
                    cashflows_cpy = self.prep_dataframe_to_save(cashflows, stock_id)
                    financials_cpy = self.prep_dataframe_to_save(financials, stock_id)

                    # COMMIT/APPEND DB Tables
                    if not stock_info_cpy.empty:
                        try:
                            dbObj = db.DBConnection
                            dbObj.append_data_to_table(dbObj, table_name='stock_basic_info', conn=conn,
                                                       dataframe=stock_info_cpy)
                            # stock_info_cpy.to_sql('stock_basic_info', conn, index=False, if_exists='append')
                            logging.info(f"Stock info records appended to the database.\{stock_info_cpy.head()}")
                        except Error as e:
                            logging.error(
                                f"Error occurred when appending {stock_info_cpy.columns} data into stock_basic_info table")
                            logging.error(e)
                        except sqlite3.OperationalError as f:
                            logging.error(
                                "sqlite3 Operational Error occurred when appending {stock_info_cpy.columns} data into stock_basic_info table")
                            logging.error(f)
                            pass
                        except sqlalchemy.exc.OperationalError as g:
                            logging.error(
                                "sqlAlchemy Operational Error occurred when appending {stock_info_cpy.columns} data into stock_basic_info table")
                            logging.error(g)
                            pass
                        finally:
                            logging.info("Stock Info Append/Insert Process Completed.")
                            pass

                    # Balance Sheet
                    try:
                        balanceSheet_cpy.to_sql('stock_balance_sheet', conn, index=False, if_exists='append')
                        logging.info("Balance Sheet records appended to the database.")
                    except Error as e:
                        logging.error("Error Occurred when trying to update/append the balance sheet.")
                        logging.error(e)
                        # balanceSheet_cpy.to_sql('stock_balance_sheet', conn, index=False, if_exists='append',)
                    except sqlite3.OperationalError as f:
                        logging.error(
                            "sqlite3 Operational Error Occurred when trying to update/append the balance sheet.")
                        logging.error(f)
                        pass
                    except sqlalchemy.exc.OperationalError as g:
                        logging.error(
                            "sqlAlchemy Operational Error Occurred when trying to update/append the balance sheet.")
                        logging.error(g)
                        pass
                    finally:
                        logging.info("Balance Sheet Append/Insert Process Completed.")
                        pass


                    # Cashflows
                    try:
                        cashflows_cpy.to_sql('stock_cashflows', conn, index=False, if_exists='append')
                        logging.info("Cash Flow records appended to the database.")
                    except Error as e:
                        logging.error("Error Occurred when trying to update/append the cashflow sheet.")
                        logging.error(e)
                        # balanceSheet_cpy.to_sql('stock_balance_sheet', conn, index=False, if_exists='append',)
                    except sqlite3.OperationalError as f:
                        logging.error(
                            "sqlite3 Operational Error Occurred when trying to update/append the balance sheet.")
                        logging.error(f)
                        pass
                    except sqlalchemy.exc.OperationalError as g:
                        logging.error(
                            "sqlAlchemy Operational Error Occurred when trying to update/append the balance sheet.")
                        logging.error(g)
                        pass
                    finally:
                        logging.info("Cash Flow Append/Insert Process Completed.")
                        pass


                    # Financials
                    try:
                        financials_cpy.to_sql('stock_financials', conn, index=False, if_exists='append')
                        logging.info("Financials records appended to the database.")
                    except Error as e:
                        logging.error("Error Occurred when trying to update/append the financial.")
                        # balanceSheet_cpy.to_sql('stock_balance_sheet', conn, index=False, if_exists='append',)
                        logging.error(e)
                    except sqlite3.OperationalError as f:
                        logging.error(
                            "sqlite3 Operational Error Occurred when trying to update/append the balance sheet.")
                        logging.error(f)
                        pass
                    except sqlalchemy.exc.OperationalError as g:
                        logging.error(
                            "sqlAlchemy Operational Error Occurred when trying to update/append the balance sheet.")
                        logging.error(g)
                        pass
                    finally:
                        logging.info("Financials Insertion Completed.")
                        pass

                    earnings_cpy = earnings.copy().T
                    earnings_cpy.index.rename("Year", inplace=True)
                    earnings_cpy.reset_index(inplace=True)
                    earnings_cpy['stock_id'] = stock_id
                    earnings_cpy['date'] = pd.Timestamp.now()
                    try:
                        earnings_cpy.to_sql('stock_earnings', conn, index=False, if_exists='append')
                        logging.info("Success! Earnings records appended to the database.")
                    except Error as e:
                        logging.error("Error Occurred when trying to update/append to earnings.")
                        # balanceSheet_cpy.to_sql('stock_balance_sheet', conn, index=False, if_exists='append',)
                        logging.error(e)
                    except sqlite3.OperationalError as f:
                        logging.error(
                            "sqlite3 Operational Error Occurred when trying to update/append the balance sheet.")
                        logging.error(f)
                        pass
                    except sqlalchemy.exc.OperationalError as g:
                        logging.error(
                            "sqlAlchemy Operational Error Occurred when trying to update/append the balance sheet.")
                        logging.error(g)
                        pass
                    finally:
                        logging.info("Earnings Append/Insert Process Completed.")
                        pass

                    # Close Connection
                    # Return something indicating status of operation.
                    pass

                # TODO Return this in a dictionary that can then be accessed in a faster, more efficient way
                return option_chain, financials, cashflows, earnings, balanceSheet, stock_info

            if options:
                option_chain = {}
                try:
                    data.options
                    option_chain = data.option_chain()
                    option_chain = {'options': option_chain, 'option_dates': data.options}

                except Exception as e:
                    logging.error(f"Error Occurred while trying to get the Options {e}")

                return option_chain

            if financials:
                financials = data.financials
                return financials

            if balanceSheet:
                balanceSheet = data.balance_sheet
                return balanceSheet

            if cashflows:
                cashflows = data.cashflow
                return cashflows

            if earnings:
                earnings = data.earnings
                return earnings

    '''
    returns: Dataframe with stock information 
    
    period: data period to download (either use period parameter or use start and end) Valid periods are:
    “1d”, “5d”, “1mo”, “3mo”, “6mo”, “1y”, “2y”, “5y”, “10y”, “ytd”, “max”
    
    
    interval: data interval (1m data is only for available for last 7 days, and data interval <1d for the last 60 days) Valid intervals are:
    “1m”, “2m”, “5m”, “15m”, “30m”, “60m”, “90m”, “1h”, “1d”, “5d”, “1wk”, “1mo”, “3mo”
    
    if using start and end as the period, then start = datetime.datetime.now()-datetime.timedelta(days=365), end = datetime.datetime.now()
    '''

    def get_ticker_all(self, stock_symbol='^GSPC', period='2y', interval='1d', add_ma=True, add_bb=True, add_mi=True):

        # download is actually for mass downloading tickers.
        if stock_symbol is list:
            data = yf.download(tickers=stock_symbol, period=period, interval=interval)

            # Send to a function that breakdown the multidex dataframe that will be returned.
        else:
            data = yf.download(tickers=stock_symbol, period=period, interval=interval)
            # data = yf.Ticker(ticker=stock_symbol)

        if data is not None:
            # Overlap Studies
            if add_ma:
                data['STMA'] = data['Close'].rolling(self.ST_PERIOD).mean()
                data['LTMA'] = data['Close'].rolling(self.LG_PERIOD).mean()
                data['EMA'] = ta.EMA(data['Close'], self.ST_PERIOD)

            if add_bb:
                data['Bollinger-Upper'], data['Bollinger-Middle'], data['Bollinger-Lower'] = ta.BBANDS(data['Close'],
                                                                                                       timeperiod=self.ST_PERIOD,
                                                                                                       matype=1)
            # Momemntum and Volatility Indicators
            if add_mi:
                data['RSI'] = ta.RSI(data['Close'], timeperiod=self.ST_PERIOD)
                data['ATR'] = ta.ATR(data['High'], data['Low'], data['Close'], timeperiod=self.ST_PERIOD)

        return data

    '''
    Append the Technical Analysis indicators to the stock dataframe that was populated from the database.
    :param Pandas dataframe
    :param SQLite3 Connection Object 
    :param add_ma boolean value to add the Preset Moving averages to the dataframe
    :param add_bb boolean value to add the Preset Bollinger Bands to the dataframe
    :param add_mi boolean value to add the Preset Momentum Indicators to the dataframe
    '''

    def get_ticker_all_add_df(self, dataframe, conn, add_ma=True, add_bb=True, add_mi=True, stock_id=None):
        if dataframe is not None:
            if 'stock_id' in dataframe.columns:
                stock_id = dataframe['stock_id'][0]
            else:
                dataframe['stock_id'] = stock_id

            logging.info(f"The max date is {dataframe['date'].max()}")
            timestamp_string = str(dataframe['date'].max()).strip()
            contains_mills = '.' in timestamp_string
            if contains_mills:
                max_date = dt.datetime.strptime(str(dataframe['date'].max()).strip(), '%Y-%m-%d %H:%M:%S.%f')
            else:
                max_date = dt.datetime.strptime(str(dataframe['date'].max()).strip(), '%Y-%m-%d %H:%M:%S')
            max_date = max_date.date()
            current_date = dt.datetime.now().date() - dt.timedelta(1)
            logging.info(
                "The maximum date for {} is {}, the current datetime is {}".format(stock_id, max_date, current_date))

            if max_date != current_date or max_date < current_date:
                # Get additional price data that wil be added to the stock price table
                stock_symbol = self.get_ticker_symbol(stock_id=stock_id, conn=conn)
                add_data = yf.download(tickers=stock_symbol, start=max_date, end=current_date)
                dataframe = self.prep_dataframe(add_data=add_data, conn=conn, stock_id=stock_id)

            # Drop Duplicate data in the dataframe, and resetting the index of the rows if
            # there is no duplicates to drop than this has no effect
            dataframe.drop_duplicates(inplace=True, ignore_index=True)
            dataframe.dropna(axis=0, inplace=True)

            # Moving Averages
            if add_ma:
                dataframe['STMA'] = dataframe['Close'].rolling(self.ST_PERIOD).mean()
                dataframe['LTMA'] = dataframe['Close'].rolling(self.LG_PERIOD).mean()
                dataframe['EMA'] = ta.EMA(dataframe['Close'], self.ST_PERIOD)
                dataframe['MA50'] = ta.MA(dataframe['Close'], self.MA50)  # Short-Term Trend
                dataframe['MA72'] = ta.MA(dataframe['Close'], self.MA72)  # Long-Term Trend
                dataframe['MA200'] = ta.MA(dataframe['Close'], self.MA200)  # Long-Term Trend

            # Overlap Studies -- Trend Identifications
            if add_bb:
                dataframe['Bollinger-Upper'], dataframe['Bollinger-Middle'], dataframe['Bollinger-Lower'] = ta.BBANDS(
                    dataframe['Close'],
                    timeperiod=self.ST_PERIOD,
                    matype=1)

            # Momentum and Volatility Indicators
            if add_mi:
                dataframe['RSI'] = ta.RSI(dataframe['Close'], timeperiod=self.RSI_PERIOD)
                dataframe['ATR'] = ta.ATR(dataframe['High'], dataframe['Low'], dataframe['Close'],
                                          timeperiod=self.ST_PERIOD)
                dataframe['macd'], dataframe['macd_signal'], dataframe['macd_hist'] = ta.MACD(
                    dataframe['Close'].values, fastperiod=self.MACD_FAST_PD, slowperiod=self.MACD_SLOW_PD,
                    signalperiod=self.MACD_SIGNAL_LINE
                )
                dataframe['obv'] = ta.OBV(dataframe['Close'], dataframe['Volume'])

                # will return the dataframe with daily return already attached.
                dataframe = utils.Utils.add_daily_return_to_df("", dataframe)
                dataframe['daily_return'].fillna(0, inplace=True)

        return dataframe

    '''
    Get the Company Information from YFinance
    :param stock_symbol
    
    '''

    def get_ticker_stock_info(self, stock_symbol):
        stock_info = yf.Ticker(stock_symbol).info  # TODO API HIT
        stock_info = pd.DataFrame.from_dict(stock_info, orient='index').reset_index()
        stock_info.columns = ["Attribute", "Recent"]
        stock_info.set_index('Attribute', inplace=True)

        if stock_info.empty or stock_info is None:
            return None

        return stock_info

