----------------------------------------------------------------------
-- INSERT INTO Company Information table.
-- V2.0
-- Anthony Thomas-Bell
--
-- add new data into Company Information - partial query since the dynamic part is done via python.
----------------------------------------------------------------------
INSERT INTO stock_basic_info(stock_id,sector,fullTimeEmployees,longBusinessSummary,website,city, state, zip,industry,
targetLowPrice, targetMeanPrice, targetHighPrice, shortName, longName,quoteType,symbol,fiftyTwoWeekChange,
sharesOutstanding, sharesShort, SandP52WeekChange, yield, beta, lastDividendDate, twoHundredDayAverage, divdendRate,
 exDividendDate, fiftyTwoWeekHigh, fiftyTwoWeekLow, dividendYield, nextFiscalYearEnd, date)
VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,)