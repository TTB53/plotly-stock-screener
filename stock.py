# Raw data comes from yfinance - add any other packages that provide data here
# yfinance documentation https://pypi.org/project/yfinance/
# Plotly  Documentation https://plotly.com/python/
import datetime as dt
import sys
from sqlite3 import Error
import logging

import pandas as pd
import talib as ta
import yfinance as yf

import db
import utils

'''
Technical Analysis V1.0 
Author - Anthony Thomas - Bell 
Version 1.0
May 13th 2021

------------------------------------------------------------------------------
Program Description
-------------------------------------------------------------------------------

Quick Program to analyze stock price to learn how to perform technical analysis
for trading securities better. Also, because I am extra and want to turn this into something 
to help me learn to identify patterns and trends we are going to make it into a dashboard using plotly
and serve it either using Django or Flask maybe pull in some sentiment analysis 
from current news articles and searching thelayoff and blind.com reviews, as well as how 
that security is performing against its industry as well as the overall market.

----------------------------------------------------------------------------------
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
'''

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
    ST_PERIOD = 20
    LG_PERIOD = 50
    BB_MULTIPLIER = 1.96

    RSI_PERIOD = 14

    MA50 = 50
    MA72 = 72
    MA200 = 200

    MACD_FAST_PD = 12
    MACD_SLOW_PD = 26
    MACD_SIGNAL_LINE = 9

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

    # TODO Move this to the DB Connection Object

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
    options, financials, cashflows, earnings, and balance sheets.

    :param stock_symbol:
    :param options:
    :param financials:
    :param cashflows:
    :param earnings:
    :param balanceSheet:
    :param save_data:
    :return:

        :returns a Dictionary for the Options( Dict holds puts and calls, and the exp dates), financials,
        cashflows, earnings, and balanceSheet are all pandas dataframes


    '''

    def get_ticker_additional_information(self, stock_symbol='^GSPC', options=True, financials=True, cashflows=True,
                                          earnings=True, balanceSheet=True, stock_info=False, save_data=False,
                                          stock_id=None, conn=None):

        data = yf.Ticker(ticker=stock_symbol)

        # Note as of yFinance 0.2.22 earnings is now lumped into the financials, so instead of being separate,
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
                    logging.error(e)

                financials = data.financials
                cashflows = data.cashflow
                if financials is not None:
                    # Need to get the revenue and after-tax net income to match the pervious earnings information
                    earnings = financials.loc[['Net Income', 'Total Revenue']]
                    earnings = earnings.rename({'Net Income': 'earnings', 'Total Revenue': 'revenue'})
                # earnings = data.earnings
                balanceSheet = data.balance_sheet

                if stock_info:
                    stock_info = {}
                    stock_info = data.fast_info  # can also use basic_info
                    stock_info_cpy = stock_info

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
                    stock_info_cpy.rename(index={'52WeekChange': 'fiftyTwoWeekChange'}, inplace=True)
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
                    except Error as e:
                        logging.error(e)
                        conn = db.DBConnection.create_connection()

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
                            stock_info_cpy.to_sql('stock_basic_info', conn, index=False, if_exists='append')
                            logging.info("Earnings records appended to the database.")
                        except Error as e:
                            logging.error("Error occured when appending to the database")
                            logging.error(e)

                    try:
                        balanceSheet_cpy.to_sql('stock_balance_sheet', conn, index=False, if_exists='append')
                        logging.info("Balance Sheet records appended to the database.")
                    except Error as e:
                        logging.error("Error Occurred when trying to update/append the balance sheet.")
                        logging.error(e)
                        # balanceSheet_cpy.to_sql('stock_balance_sheet', conn, index=False, if_exists='append',)
                    finally:
                        logging.info("Balance Sheet Insertion Completed.")
                        pass

                    try:
                        cashflows_cpy.to_sql('stock_cashflows', conn, index=False, if_exists='append')
                        logging.info("Cash Flow records appended to the database.")
                    except Error as e:
                        logging.error("Error Occurred when trying to update/append the cashflow sheet.")
                        logging.error(e)
                        # balanceSheet_cpy.to_sql('stock_balance_sheet', conn, index=False, if_exists='append',)
                    finally:
                        logging.info("Cash Flow Insertion Completed.")
                        pass

                    try:
                        financials_cpy.to_sql('stock_financials', conn, index=False, if_exists='append')
                        logging.info("Financials records appended to the database.")
                    except Error as e:
                        logging.error("Error Occurred when trying to update/append the financials.")
                        # balanceSheet_cpy.to_sql('stock_balance_sheet', conn, index=False, if_exists='append',)
                        logging.error(e)
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
                        logging.info("Earnings records appended to the database.")
                    except Error as e:
                        logging.error("Error Occurred when trying to update/append to earnings.")
                        # balanceSheet_cpy.to_sql('stock_balance_sheet', conn, index=False, if_exists='append',)
                        logging.error(e)
                    finally:
                        logging.info("Earnings Insertion Completed.")
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
                    logging.error(e)

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

            max_date = dt.datetime.strptime(str(dataframe['date'].max()), '%Y-%m-%d %H:%M:%S')
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
                dataframe = utils.add_daily_return_to_df(dataframe)
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
