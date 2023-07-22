----------------------------------------------------------------------
--CREATE Company Info from yFinance API
-- V2.0
-- Anthony Thomas-Bell
--
--Create the Company Info Table if it doesn't exist. Currently comes from yFinance but might have to come
--From a mix of sources to get all the information.
----------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS "stock_basic_info"(
"id" INTEGER PRIMARY KEY, 
"stock_id" INTEGER,
"currency" TEXT,
"dayHigh" REAL,
"dayLow" REAL,
"exchange" TEXT,
"fiftyDayAverage" REAL,
"lastPrice" REAL,
"lastVolume" REAL,
"marketCap" REAL,
"open" REAL,
"previousClose" REAL,
"quoteType" TEXT,
"regularMarketPreviousClose" REAL,
"shares" INTEGER,
"tenDayAverageVolume" INTEGER,
"timezone" TEXT,
"twoHundredDayAverage" REAL,
"yearChange" REAL,
"yearHigh" REAL,
"yearLow" REAL,
"symbol" TEXT,
--These were the original columns for the yFinance API at the time of V1.0 development(2021)
"sector" TEXT, -- No Longer Needed/Used in yFinance 0.2
"fullTimeEmployees" INTEGER, -- No Longer Needed/Used in yFinance 0.2
"longBusinessSummary" TEXT, -- No Longer Needed/Used in yFinance 0.2
"website" TEXT, -- No Longer Needed/Used in yFinance 0.2
"city" TEXT, -- No Longer Needed/Used in yFinance 0.2
"state" TEXT, -- No Longer Needed/Used in yFinance 0.2
"zip" INTEGER, -- No Longer Needed/Used in yFinance 0.2
"industry" TEXT, -- No Longer Needed/Used in yFinance 0.2
"targetLowPrice" REAL, -- No Longer Needed/Used in yFinance 0.2
"targetMeanPrice" REAL, -- No Longer Needed/Used in yFinance 0.2
"targetHighPrice" REAL, -- No Longer Needed/Used in yFinance 0.2
"shortName" TEXT, -- No Longer Needed/Used in yFinance 0.2
"longName" TEXT, -- No Longer Needed/Used in yFinance 0.2
"quoteType" TEXT, -- No Longer Needed/Used in yFinance 0.2
"fiftyTwoWeekChange" REAL, -- No Longer Needed/Used in yFinance 0.2
"sharesOutstanding" REAL, -- No Longer Needed/Used in yFinance 0.2
"sharesShort" REAL, -- No Longer Needed/Used in yFinance 0.2
"SandP52WeekChange" REAL, -- No Longer Needed/Used in yFinance 0.2
"yield" REAL, -- No Longer Needed/Used in yFinance 0.2
"beta" REAL, -- No Longer Needed/Used in yFinance 0.2
"lastDividendDate" DATE, -- No Longer Needed/Used in yFinance 0.2
"twoHundredDayAverage" REAL, -- No Longer Needed/Used in yFinance 0.2
"dividendRate" REAL, -- No Longer Needed/Used in yFinance 0.2
"exDividendDate" DATE, -- No Longer Needed/Used in yFinance 0.2
"fiftyTwoWeekHigh" REAL, -- No Longer Needed/Used in yFinance 0.2
"fiftyTwoWeekLow" REAL, -- No Longer Needed/Used in yFinance 0.2
"dividendYield" REAL,-- No Longer Needed/Used in yFinance 0.2
"nextFiscalYearEnd" DATE,-- No Longer Needed/Used in yFinance 0.2
"date" TIMESTAMP,
Foreign Key (stock_id) references stock(id)
)