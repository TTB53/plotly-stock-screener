----------------------------------------------------------------------
--CREATE Cash Flows table from yFinance API
-- V2.0
-- Anthony Thomas-Bell
--
--
----------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS "stock_cashflows"(
"id" INTEGER PRIMARY KEY,
"stock_id" INTEGER,
"Free Cash Flow" REAL,
"Repurchase Of Capital Stock" REAL,
"Repayment Of Debt" REAL,
"Issuance of Debt" REAL,
"Capital Expenditure" REAL,
"Interest Paid Supplemental Data" REAL,
"Income Tax Paid Supplemental Data" REAL,
"End Cash Position" REAL,
"Beginning Cash Position" REAL,
"Effect Of Exchange Rate Changes" REAL,
"Changes In Cash" REAL,
"Financing Cash Flow" REAL,
"Cash Flow From Continuing Financing Activities" REAL,
"Net Other Financing Charges" REAL,
"Proceeds From Stock Option Excercised" REAL,
"Net Common Stock Issuance" REAL,
"Long Term Debt Issuance" REAL,
"Investing Cash Flow" REAL,
"Cash Flow From Continuing Investing Activities" REAL,
"Net Investment Purchase And Sale" REAL,
"Sale Of Investment" REAL,
"Purchase Of Investment" REAL,
"Net Business Purchase And Sale" REAL,
"Purchase Of Business" REAL,
"Capital Expenditure Reported" REAL,
"Operating Cash Flow" REAL,
"Cash Flow From Continuing Operating Activities" REAL,
"Change In Working Capital" REAL,
"Change In Other Working Capital" REAL,
"Change In Other Current Liabilities" REAL,
"Change In Payables And Accrrued Expense" REAL,
"Change In Payable" REAL,
"Change In Accounts Payable" REAL,
"Change In Prepaid Assets" REAL,
"Change In Receivables" REAL,
"Changes In Accounts Receivables" REAL,
"Other Non Cash Items" REAL,
"Stock Based Compensation" REAL,
"Deferred Tax" REAL,
"Deferred Income Tax" REAL,
"Depreciation Amortization Depletion" REAL,
"Depreciation And Amortization" REAL,
"Operating Gains Losses" REAL,
"Earnings Losses From Equity Investments" REAL,
"Gain Loss On Sale Of Business" REAL,
"Net Income From Continuing Operations" REAL,

--These were the original columns for the yFinance API at the time of V1.0 development(2021)
"Investments" REAL, -- No Longer Needed/Used in yFinance 0.2
"Change To Liabilities" REAL, -- No Longer Needed/Used in yFinance 0.2
"Total Cashflows From Investing Activities" REAL, -- No Longer Needed/Used in yFinance 0.2
"Net Borrowings" REAL, -- No Longer Needed/Used in yFinance 0.2
"Total Cash From Financing Activites" REAL, -- No Longer Needed/Used in yFinance 0.2
"Change To Operating Activities" REAL, -- No Longer Needed/Used in yFinance 0.2
"Net Income" REAL, -- No Longer Needed/Used in yFinance 0.2
"Change In Cash" REAL, -- No Longer Needed/Used in yFinance 0.2
"Repurchase Of Stock" REAL,-- No Longer Needed/Used in yFinance 0.2
"Effect Of Exchange Rate" REAL, -- No Longer Needed/Used in yFinance 0.2
"Total Cash From Operating Activities" REAL, -- No Longer Needed/Used in yFinance 0.2
"Depreciation" REAL, -- No Longer Needed/Used in yFinance 0.2
"Other Cashflows From Investing Activities" REAL, -- No Longer Needed/Used in yFinance 0.2
"Dividends Paid" REAL, -- No Longer Needed/Used in yFinance 0.2
"Change To Other Cashflows From Investing Activities" REAL, -- No Longer Needed/Used in yFinance 0.2
"Change To Netincome" REAL, -- No Longer Needed/Used in yFinance 0.2
"Capital Expenditures" REAL, -- No Longer Needed/Used in yFinance 0.2
"date" TIMESTAMP,
Foreign Key (stock_id) references stock(id)
)