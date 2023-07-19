----------------------------------------------------------------------
-- Financials from yFinance API
-- V2.0
-- Anthony Thomas-Bell
--
--
----------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS "stock_financials"(
"id" INTEGER PRIMARY KEY, 
"stock_id" INTEGER,
"Year" INTEGER,
"Tax Effect Of Unusual Items" REAL,
"Tax Rate for Calcs" REAL,
"Normalized EBTIDA" REAL,
"Total Unusual Items" REAL,
"Total Unusual Items Excluding Goodwill" REAL,
"Reconciled Depreciation" REAL,
"Reconciled Cost Of Revenue" REAL,
"EBIT" REAL,
"Normalized Income" REAL, 
"Net Income From Continuing And Discontinued Operation" REAL,
"Total Expenses" REAL,
"Total Operating Income As Reported" REAL,
"Diluted Average Shares" REAL,
"Basic Average Shares" REAL,
"Diluted EPS" REAL,
"Basic EPS" REAL,
"Diluted NI Availto Com Stockholders" REAL,
"Net Income Commmon Stockholders" REAL,
"Net Income" REAL,
"Net Income Including Noncontrolling Interests" REAL,
"Net Income Continuous Operations" REAL,
"Tax Provision" REAL,
"Pretax Income" REAL,
"Other Income Expense" REAL,
"Other Non Operating Income Expenses" REAL,
"Special Income Charges" REAL,
"Other Special Charges" REAL,
"Write Off" REAL,
"Restructuring And Mergern Acquisition" REAL,
"Gain On Sale Of Security" REAL,
"Operating Income" REAL,
"Operating Expense" REAL,
"Research And Development" REAL,
"Selling And General Administration" REAL,
"Selling And Marketing Expense" REAL,
"General And Administrative Expense" REAL,
"Other Gand A" REAL,
"Gross Profit" REAL,
"Cost of Revenue" REAL,
"Total Revenue" REAL,
"Operating Revenue" REAL,
--These were the original columns for the yFinance API at the time of V1.0 development(2021)
"Effects Of Accounting Charges" REAL, -- No Longer Needed/Used in yFinance 0.2
"Income Before Tax" REAL, -- No Longer Needed/Used in yFinance 0.2
"Minority Interest" REAL, -- No Longer Needed/Used in yFinance 0.2
"Other Operating Expenses" REAL, -- No Longer Needed/Used in yFinance 0.2
"Interest Expense" REAL, -- No Longer Needed/Used in yFinance 0.2
"Extraordinary Items" REAL, -- No Longer Needed/Used in yFinance 0.2
"Non Recurring" REAL, -- No Longer Needed/Used in yFinance 0.2
"Other Items" REAL, -- No Longer Needed/Used in yFinance 0.2
"Income Tax Expense" REAL, -- No Longer Needed/Used in yFinance 0.2
"Total Revenue" REAL, -- No Longer Needed/Used in yFinance 0.2
"Total Operating Expenses" REAL, -- No Longer Needed/Used in yFinance 0.2
"Total Other Income Expense Net" REAL, -- No Longer Needed/Used in yFinance 0.2
"Total Current Assets" REAL, -- No Longer Needed/Used in yFinance 0.2
"Discontinued Operations" REAL, -- No Longer Needed/Used in yFinance 0.2
"Net Income From Continuing Ops" REAL, -- No Longer Needed/Used in yFinance 0.2
"Net Income Applicable To Common Shares" REAL, -- No Longer Needed/Used in yFinance 0.2
"date" TIMESTAMP,
Foreign Key (stock_id) references stock(id)
)