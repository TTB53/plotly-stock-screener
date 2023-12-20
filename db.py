'''

DB Connection

------------------------------------------------------------------------------
Program Description
-------------------------------------------------------------------------------

Class that does the majority of the interacting with the database

----------------------------------------------------------------------------------
'''
import sqlite3
from sqlite3 import Error
import logging

import pandas as pd
import sqlalchemy
from sqlalchemy import create_engine, inspect, text
from sqlalchemy.orm import sessionmaker

import config


def open_and_read_sql(filename):
    f = open(filename, 'r')
    read_sql_file = f.read()
    f.close()

    return read_sql_file


# Create Table SQL statements

DB_FILE = config.ScreenerConfig.database_defaults['sqlite']['DB_FILE_SA_SQLITE']
# DB = 'sqlite'
# DB_FILE_FULL = f'{DB}:///{DB_FILE}'
SnP500_FILE = "./data/s&p500_stocks_Jun18_2021.csv"

balance_sheet_table_sql = "./data/SQL/create/balance_sheet/BalanceSheet.sql"
basic_info_table_sql = "./data/SQL/create/company_information/CompanyInfo.sql"
cashflow_table_sql = "./data/SQL/create/cashflow/Cashflow.sql"
earnings_table_sql = "./data/SQL/create/financial/Earnings.sql"
financials_table_sql = "./data/SQL/create/financial/Financials.sql"
prices_table_sql = "./data/SQL/create/Prices.sql"
stock_table_sql = "./data/SQL/create/Stock.sql"
sector_ratios_sql = "./data/SQL/read/sector_analysis/SectorRatios.sql"

basic_info_table_insert = "./data/SQL/update/company_information/companyInformationInsert.sql"

insert_stock_table_data = """
INSERT INTO stock(symbol, company, nasdaq_sector, gcis_sector,gcis_subsector,headquarters,date_added,CIK,founded) 
VALUES (?,?,?.?,?,?,?,?,?,);
"""

insert_stock_price_table_data = """
INSERT INTO stock_price(date, Open, High, Low, Close, adjusted_close,Volume, stock_id) 
VALUES (?,?,?.?,?,?,?,)
"""

insert_stock_balance_sheet_data = open_and_read_sql('./data/SQL/update/balance_sheet/balanceSheetInsert.sql')

"""
INSERT INTO stock_balance_sheet(stock_id, year,'Intangible Assets', 'Capital Surplus', 'Total Liab',
'Total Stockholder Equity','Minority Interest','Other Current Liab','Total Assets','Common Stock','Other Current Assets'
, 'Retained Earnings','Other Liab','Good Will','Treasury Stock','Other Assets','Cash','Total Current Liabilities',
'Deferred Long Term Assets Charges','Short Long Term Debt','Other Stockholder Equity','Property Plant Equipment',
'Total Current Assets','Long Term Investments','Net Tangible Assets','Short Term Investments','Net Receivables',
'Long Term Debt','Accounts Payable','Deferred Long Terms Liab','Inventory', 'date',) 
VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,)
"""

# TODO need to find out where to get some of this information as it is no longer included in the Yahoo Finance API.
insert_stock_basic_info_data = open_and_read_sql('./data/SQL/update/company_information/CompanyInformationInsert.sql')
"""
INSERT INTO stock_basic_info(stock_id,sector,fullTimeEmployees,longBusinessSummary,website,city, state, zip,industry,
targetLowPrice, targetMeanPrice, targetHighPrice, shortName, longName,quoteType,symbol,fiftyTwoWeekChange, 
sharesOutstanding, sharesShort, SandP52WeekChange, yield, beta, lastDividendDate, twoHundredDayAverage, divdendRate,
 exDividendDate, fiftyTwoWeekHigh, fiftyTwoWeekLow, dividendYield, nextFiscalYearEnd, date) 
VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,)
"""

insert_stock_cashflows_data = open_and_read_sql('./data/SQL/update/cashflow/cashflowsInsert.sql')
"""
INSERT INTO stock_cashflows(stock_id, 'Investments','Change To Liabilities','Total Cashflows from Investing Activities',
'Net Borrowings','Total Cash from Financing Activities','Change To Operating Activities','Net Income',
'Change In Cash','Repurchase of Stock','Effect Of Exchange Rate','Total Cash From Operating Activities','Depreciation',
'Other Cashflows From Investing Activities','Dividends Paid','Change To Other Cashflows From Investing Activities',
'Change To Netincome','Capital Expenditures','Change To Inventory','Change to Account Receivables',
'Other Cashflows From Financing Activities','Year','Total Cash From Financing Activities','Issuance Of Stock','date') 
VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,)
"""

insert_earnings_data = open_and_read_sql('./data/SQL/update/financial/earningsInsert.sql')
"""
INSERT INTO stock_earnings(stock_id,Year, Earnings, Revenue, 'date') VALUES(?,?,?,?,?,)
"""

insert_financials_data = open_and_read_sql('./data/SQL/update/financial/financialsInsert.sql')

"""
INSERT INTO stock_financials(stock_id, 'Research Development', 'Effect Of Accounting Charges','Income Before Tax',
'Minority Interest','Net Income','Selling General Administrative','Gross Profit','Ebit','Operating Income',
'Other Operating Expenses','Interest Expense','Extraordinary Items','Non Recurring','Other Items','Income Tax Expense',
'Total Revenue','Total Operating Expenses','Cost of Revenue','Total Other Income Expense Net','Total Current Assets',
'Discontinued Operations','Net Income From Continuing Ops','Net Income Applicable To Common Shares','date','year',) 
VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
"""

drop_stock_sql = """DROP TABLE IF EXISTS stock"""
drop_stock_price_sql = """DROP TABLE IF EXISTS stock_price"""
drop_balance_sheet_sql = """ DROP TABLE IF EXISTS stock_balance_sheet"""
drop_basic_info_sql = """ DROP TABLE IF EXISTS stock_basic_info"""
drop_cashflows_sql = """ DROP TABLE IF EXISTS stock_cashflows"""
drop_earnings_sql = """ DROP TABLE IF EXISTS stock_earnings"""
drop_financials_sql = """ DROP TABLE IF EXISTS stock_financials"""


class DBConnection:
    DB_FILE = DB_FILE
    """
    Create an String version of an SQL query or query partial 
    :param sql_file: sql file path
    :return  sql_str: string represntation of SQL file
    """

    def create_sql_string(self, sql_file):
        sql_file = open(sql_file)
        sql_str = sql_file.read()

        return sql_str

    """
    Create a database connection to the database specified by db_file
    :param db_file: database file path
    :return  Connection object or None
    """

    def create_connection(self, db_file=DB_FILE):
        from sqlalchemy.exc import OperationalError

        conn = None
        try:
            conn = create_engine(db_file)

            # Check the connection that was established
            with conn.connect() as connection:
                result = connection.execute(text("SELECT * FROM Stock LIMIT 1"))
                if result.scalar() == 1:
                    logging.info(f"Database Connection was established using the following DB: {db_file}")
        except OperationalError as e:
            logging.error(
                f"SQLAlchemy Operation Error Occurred when connecting "
                f"to the Database check db connection string.{db_file}")

            return conn
        except Error as e:
            logging.info(f"There was an error when trying to connect to {db_file} database | {e}")
        return conn

    """ 
    Drop the table from the database
    :param conn database connection object
    :param drop_table_sql: database connection object
    :return Connection object or None
    """

    def drop_table(self, conn, drop_table_sql):

        try:
            c = conn.cursor()
            c.execute(drop_table_sql)
            logging.info(f"Table was Dropped Successfully using this statement \n{drop_table_sql}\n")

        except Error as e:
            logging.info(
                f"There was an error when trying to drop the table with the following query.\n{drop_table_sql}\n|{e}")

    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """

    def create_table(self, conn, create_table_sql):

        create_table_sql_str = self.create_sql_string(create_table_sql)

        logging.info("Table SQL being created.\n{}\n".format(create_table_sql_str))

        try:
            c = conn.cursor()
            c.executescript(create_table_sql_str)
            conn.commit()
            c.close()
        except Error as e:
            logging.info(f"ERROR OCCURRED WHEN CREATING TABLE----ERROR\n{e}\nClosing Connection to DB")
            conn.close()

    # conn.close()

    """ Insert data from param list into table specified by insert table sql
    :param conn: Database Connection Object
    :param insert_table_sql: SQL Statement for inserting data into the table.
    :param param_list : List of Parameters to be used in inserting data int othe table
    :return  Connection object or None
    """

    def insert_into_table(self, conn, insert_table_sql, param_list=None):

        try:
            c = conn.cursor()

            if param_list is not None:
                c.execute(insert_table_sql, param_list)
                conn.commit()
                logging.info("Data Successfully submitted to DB with the provided paramaters\n{}".format(param_list))
            else:
                c.execute(insert_table_sql)
                conn.commit()
                logging.info("Data Successfully entered into the DB.")
            c.close()

        except Error as e:
            logging.info(e)

    '''
    Select and retrieve all the data for the table name.
    :param conn: database connection object
    :param table_name: database table to get data for.
    :return Data: pandas dataframe that has the data from db or None.
    '''

    def get_all_data(self, conn, table_name=None):

        if conn and table_name:
            c = conn.cursor()
            data = c.execute('''SELECT * FROM {}'''.format(table_name)).getall()
            logging.info(data)
            c.close()

    '''
    Select and retrieve all the data for the table name where passed param is.
    :param conn: database connection object
    :param table_name: database table to get data for.
    :return Data: pandas dataframe that has the data from db or None.
    '''

    def get_all_data_where(self, conn, table_name=None, column=None, param=None):

        if conn and table_name:
            c = conn.cursor()
            data = c.execute('''SELECT * FROM {} where {} = {}'''.format(table_name, column, param)).getall()
            logging.info(data)
            c.close()

    '''
    Get the most recent price data from yFinance for all the companies in the stock price table,
    This was originally populated from the stocks that were in S&P500 in June 2021.
    This will populate the following Tables:
        -Stock Price 
        -Stock Balance Sheet
        -Stock Basic Info
        -Stock Cashflows
        -Stock Earnings
        -Stock Financials

    :param conn: database connection object
    :param table_name: table name where the S&P500 Stocks
    :param db_file: database file path
    :return
    '''

    def get_sp500_data(self, conn, table_name, db_file):
        import time
        import random
        from stock import MyStock

        stockObj = MyStock()

        try:
            # conn = create_connection(db_file)
            stock_df = pd.read_sql_query('SELECT * FROM stock', conn)
            i = 0
            #
            # self.drop_table(self, conn=conn, drop_table_sql=drop_stock_price_sql)
            # self.drop_table(self, conn=conn, drop_table_sql=drop_basic_info_sql)
            # self.drop_table(self, conn=conn, drop_table_sql=drop_balance_sheet_sql)
            # self.drop_table(self, conn=conn, drop_table_sql=drop_cashflows_sql)
            # self.drop_table(self, conn=conn, drop_table_sql=drop_financials_sql)
            # self.drop_table(self, conn=conn, drop_table_sql=drop_earnings_sql)

            # Looping through all the s&p500 companies and dowloading their daily data
            # TODO when updating, split dataframe into multiple sections and slow down hits to server due to
            #  new stocks being added to the DB since last update Look into chunking and batch api calls with yFinance
            for stock in stock_df['symbol']:

                random_number = random.randrange(1, 4)

                stock_id = stock_df['id'][i]
                stock_symbol = stock_df['symbol'][i]
                stock = stockObj.get_ticker_all(stock, add_ma=False, add_bb=False, add_mi=False)

                if stock is not None:
                    stock['date'] = pd.to_datetime(stock.index)
                    stock.rename_axis("Date", axis='index', inplace=True)
                    stock.rename(columns={
                        'Adj Close': 'adjusted_close'
                    }, inplace=True)
                    stock['stock_id'] = stock_id
                    stock.to_sql('stock_price', conn, if_exists='append', index=False)

                    # These are not actually needed, they are returned from the function which saves them to db

                    options, financials, cashflows, earnings, balanceSheet, stock_info = stockObj.get_ticker_additional_information(
                        stock_symbol=stock_symbol, stock_info=True)

                    logging.info("Waiting to get the Other Info\n{}s\n".format(random_number))
                    time.wait(random_number)
                    stock_info = stockObj.get_ticker_additional_information(balanceSheet=False,
                                                                            stock_id=stock_id)
                    logging.info(stock_info)
                    i = i + 1
        except Error as e:
            logging.info(e)

    '''
    Get all the data in a selected SQL table
    :param table_name name of SQL table
    :param conn SQLAlchemy Connection Object
    '''

    def select_table_data(self, conn, table_name):
        try:
            if type(conn) is sqlalchemy.Engine:
                with conn.begin() as connection:
                    result = connection.execute(text(f"SELECT * FROM {table_name}"))
                    data = pd.DataFrame(result)
            else:
                c = conn.cursor()
                data = pd.read_sql_query('''SELECT * from {}'''.format(table_name), conn)
                c.close()
            return data
        except Error as e:
            logging.info(e)
            return None

    '''
    Get a specific record from the table 
    :param table_name name of SQL table
    :param stock_id stock id that you are interested in getting data for
    '''

    def select_record(self, conn, table_names, stock_id):
        try:
            # c = conn.cursor()
            # Will Return Dataframe
            data = pd.read_sql_query('''SELECT * FROM {} WHERE stock_id = {}'''.format(table_names, stock_id), conn, )
            # c.close()
            logging.info(f"the {stock_id} in the {table_names} table(s) produced the following data\n{data}")
            return data
        except Error as e:
            logging.info(e)
            return None

    '''
    
    Check to see if the table is in the SQL database
    
    :param conn a SQLite3 Connection object
    :param table_name Table name for the table of interest
    :return String msg that indicates whether or not the table exists in the database
    
    '''

    def check_for_table(self, conn, table_name):

        msg = f"{table_name} exists. It is good to be used."

        try:
            c = conn.cursor()
            c.execute("Select * FROM {}".format(table_name))

            if c.getone()[0] == 1:
                return msg
        except:
            msg = f"The {table_name} does not exist in the database."

        return msg

    #
    # def main():
    #     database = r"C:\sqlite\db\pythonsqlite.db"
    #
    #     sql_create_projects_table = """ CREATE TABLE IF NOT EXISTS projects (
    #                                         id integer PRIMARY KEY,
    #                                         name text NOT NULL,
    #                                         begin_date text,
    #                                         end_date text
    #                                     ); """
    #
    #     sql_create_tasks_table = """CREATE TABLE IF NOT EXISTS tasks (
    #                                     id integer PRIMARY KEY,
    #                                     name text NOT NULL,
    #                                     priority integer,
    #                                     status_id integer NOT NULL,
    #                                     project_id integer NOT NULL,
    #                                     begin_date text NOT NULL,
    #                                     end_date text NOT NULL,
    #                                     FOREIGN KEY (project_id) REFERENCES projects (id)
    #                                 );"""

    '''
        Populates the initial database with the 
    '''

    def populate_init_db(self):
        # create a database connection
        db_file = self.DB_FILE
        conn = self.create_connection(self, db_file=db_file)
        logging.info(conn)

        # create tables
        if conn is not None:
            # Drop tables if they exists
            self.drop_table(self, conn, drop_stock_sql)
            self.drop_table(self, conn, drop_stock_price_sql)
            self.drop_table(self, conn, drop_balance_sheet_sql)
            self.drop_table(self, conn, drop_basic_info_sql)
            self.drop_table(self, conn, drop_cashflows_sql)
            self.drop_table(self, conn, drop_earnings_sql)
            self.drop_table(self, conn, drop_financials_sql)

            # create tables and check that they are created.

            # stock table
            self.create_table(self, conn, stock_table_sql)
            self.check_table(self, conn, "stock")

            # stock price table
            self.create_table(self, conn, prices_table_sql)
            self.check_table(self, conn, "stock_price")

            # balance sheet table
            self.create_table(self, conn, balance_sheet_table_sql)
            self.check_table(self, conn, "stock_balance_sheet")

            # basic info table
            self.create_table(self, conn, basic_info_table_sql)
            self.check_table(self, conn, "stock_basic_info")

            # cashflows table
            self.create_table(self, conn, cashflow_table_sql)
            self.check_table(self, conn, "stock_cashflows")

            # earnings table
            self.create_table(self, conn, earnings_table_sql)
            self.check_table(self, conn, "stock_earnings")

            # financial table
            self.create_table(self, conn, financials_table_sql)
            self.check_table(self, conn, "stock_financials")

        # Load Initial Data into Stock Table
        sp500 = SnP500_FILE
        sp500_df = pd.read_csv(sp500)
        sp500_df.rename(columns={'Security': 'Company', 'Nasdaq Sectors': 'nasdaq_sector', 'GICS Sector': 'gics_sector',
                                 'GICS Sub-Industry': 'gics_subsector', 'Headquarters Location': 'headquarters',
                                 'Date first added': 'date_added'},
                        inplace=True)

        # Insert Data from CSV into Stock Table
        # conn = self.create_connection(self, db_file)
        sp500_df.to_sql('stock', conn, if_exists='replace', index=False)

        # Print Results to Console
        self.get_all_data(self, conn, 'stock')

        # Populate the Stock_Prices for the past 2years
        self.get_sp500_data(self, conn, 'stock_price', db_file)
        # Print the data results using pandas since we can then use that directly in our charts and UI.
        # Show
        stock_df = pd.read_sql_query('SELECT * FROM stock', conn)
        stock_price_df = pd.read_sql_query('SELECT * FROM stock_price', conn)
        # options_df = pd.read_sql_query('SELECT * FROM options', conn)

        logging.info(stock_df.head())
        logging.info(stock_price_df.head())
        # logging.info(options_df.head())

    def append_data_to_table(self, table_name, conn, dataframe):
        # Creating SQLAlchemy Session bound to our db connection
        Session = sessionmaker(bind=conn)
        session = Session()

        try:
            # Get the db table columns
            inspector = inspect(conn)
            table_cols = [col['name'] for col in inspector.get_columns(table_name)]

            if len(table_cols) > 0:
                logging.info(f"Table columns retrieved successfully!")
                # Check for missing columns between db table and current dataframe data.
                missing_cols = list(set(table_cols) - set(dataframe.columns))

                if len(missing_cols) > 0:
                    logging.info(f"There were {len(missing_cols)} missing columns identified between the db and data")
                    for column in missing_cols:
                        dataframe[column] = None

                ordered_dataframe = dataframe[table_cols]
                logging.info('Dataframe reordered to match DB col order.')

                try:
                    ordered_dataframe.to_sql(table_name, conn, index=False, if_exists='append')
                    logging.info("Data appended to the database Successfully.")
                    session.close()
                except Error as e:
                    session.rollback()
                    logging.error("Error Occurred when trying to update/append the data to the database.")
                    logging.error(e)
                    session.close()

            else:
                logging.error(f"There are no columns for the table that was entered.")
                session.close()

        except Error as e:
            logging.info(e)
            session.close()
