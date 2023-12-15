"""
Config

------------------------------------------------------------------------------
Program Description
-------------------------------------------------------------------------------

Class for setting and controlling defaults for the Screener Application.

----------------------------------------------------------------------------------


"""


class ScreenerConfig:

    # Connection URLs to various DB's
    database_defaults = {
        "sqlite": {
            "DB_FILE": "./stock-db.db",
            "DB_FILE_SA_SQLITE": "sqlite:///./stock-db.db",
            "USERNAME": "",
            "PASSWORD": "",
        },
        "mysql": {
            "host": "localhost",
            "user": "root",
            "passwd": "my secret password",
            "db": "db-name",
        },
        "postgres": {
            'drivername': 'postgres',
            'username': 'postgres',
            'password': 'postgres',
            'host': '192.168.99.100',
            'port': 5432
        },
        "oracle": {

        },
        "mssqlserver": {

        },
    }

    # Defaults for Stocks things such as days in a year, bollinger band pds etc.
    stock_defaults = {
        "ratios": {
            "INDUSTRY_RATIOS": "./data/IndustryRatios_Aug22_2021.csv",
            "SECTOR_RATIOS": "./data/SQL/read/sector_analysis/SectorRatios.sql",
        },
        "fundamental": {
            'fiscal_days_in_year': 365,
        },
        "technical": {
            "ST_PERIOD": 20,
            "LG_PERIOD": 50,
            "BB_MULTIPLIER": 1.96,
            "RSI_PERIOD": 14,
            "MA50": 50,
            "MA72": 72,
            "MA200": 200,
            "MACD_FAST_PD": 12,
            "MACD_SLOW_PD": 26,
            "MACD_SIGNAL_LINE": 9,
        },
        "options": {

        }
    }

    # Logging information Default
    logging = {
        'basic_logger': {
            'level': '',
            'encoding': 'utf-8',
            'filename': 'path/to/log/file.name',
            'filemode': 'w',
            'format': "%(asctime)s - %(levelname)s - %(lineno)d | %(message)s "

        }
    }
