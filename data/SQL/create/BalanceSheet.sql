----------------------------------------------------------------------
-- Balance Sheet from yFinance API
-- V2.0
-- Anthony Thomas-Bell
--
--
----------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS "stock_balance_sheet"(
"id" INTEGER PRIMARY KEY,
"stock_id" INTEGER,
"year" INTEGER,
"Treasury Shares Number" REAL,
"Ordinary Shares Number" REAL,
"Share Issued" REAL,
"Net Debt" REAL,
"Total Debt" REAL,
"Tangible Book Value" REAL,
"Invested Capital" REAL,
"Working Capital" REAL,
"Net Tangible Assets" REAL,
"Capital Lease Obligations" REAL,
"Common Stock Equity" REAL,
"Total Capitalization" REAL,
"Total Equity Gross Minority Interest" REAL,
"Stockholders Equity" REAL,
"Gains Losses Not Affecting Retained Earnings" REAL,
"Other Equity Adjustments" REAL,
"Treasury Stock" REAL,
"Retained Earnings" REAL,
"Additional Paid In Capital" REAL,
"Capital Stock" REAL,
"Common Stock" REAL,
"Preferred Stock" REAL,
"Total Liabilities Net Minority Interest" REAL,
"Total Non Current Liabilities Net Minority Interest" REAL,
"Other Non Current Liabilities" REAL,
"Long Term Debt And Capital Lease Obligation" REAL,
"Long Term Capital Lease Obligation" REAL,
"Long Term Debt" REAL,
"Current Liabilities" REAL,
"Current Deferred Liabilites" REAL,
"Current Deferred Revenue" REAL,
"Current Debt And Capital Lease Obligation" REAL,
"Current Capital Lease Obligation" REAL,
"Current Debt" REAL,
"Other Current Borrowings" REAL,
"Payables And Accrued Expenses" REAL,
"Payables" REAL,
"Accounts Payable" REAL,
"Total Assets" REAL,
"Total Non Current Assets" REAL,
"Other Non Current Assets" REAL,
"Non Current Deferred Taxes Assets" REAL,
"Non Current Deferred Assets" REAL,
"Investments And Advancements" REAL,
"Other Investments" REAL,
"Investmentin Financial Assets" REAL,
"Held To Maturity Securities" REAL,
"Available For Sale Securities" REAL,
"Goodwill And Other Intangible Assets" REAL,
"Goodwill" REAL,
"Net PPE" REAL,
"Accumulated Depreciation" REAL,
"Gross PPE" REAL,
"Leases" REAL,
"Other Properties" REAL,
"Machinery Furniture Equipment" REAL,
"Buildings And Improvements" REAL,
"Land And Improvements" REAL,
"Properties" REAL,
"Current Assets" REAL,
"Other Current Assets" REAL,
"Current Deferred Assets" REAL,
"Prepaid Assets" REAL,
"Receivables" REAL,
"Accounts Receivables" REAL,
"Allowance For Doubtful Accounts Receivable" REAL,
"Gross Accounts Receivable" REAL,
"Cash Cash Equivalents And Short Term Investments" REAL,
"Other Short Term Investments" REAL,
"Cash and Cash Equivalents" REAL,
--These were the original columns for the yFinance API at the time of V1.0 development(2021)
"Intangible Assets" REAL, -- No Longer Needed/Used in yFinance 0.2
"Capital Surplus" REAL, -- No Longer Needed/Used in yFinance 0.2
"Total Liab" REAL, -- No Longer Needed/Used in yFinance 0.2
"Total Stokcholder Equity" REAL, -- No Longer Needed/Used in yFinance 0.2
"Other Current Liab" REAL, -- No Longer Needed/Used in yFinance 0.2
"Other Liab" REAL, -- No Longer Needed/Used in yFinance 0.2
"Good Will" REAL,-- No Longer Needed/Used in yFinance 0.2
"Other Assets" REAL, -- No Longer Needed/Used in yFinance 0.2
"Cash" REAL,-- No Longer Needed/Used in yFinance 0.2
"Total Curent Liabilities" REAL, -- No Longer Needed/Used in yFinance 0.2
"Deferred Long Term Asset Charges" REAL, -- No Longer Needed/Used in yFinance 0.2
"Short Long Term Debt" REAL, -- No Longer Needed/Used in yFinance 0.2
"Other Stockholder Equity" REAL, -- No Longer Needed/Used in yFinance 0.2
"Property Plant Equipment" REAL, -- No Longer Needed/Used in yFinance 0.2
"Total Current Assets" REAL, -- No Longer Needed/Used in yFinance 0.2
"Long Term Investments" REAL, -- No Longer Needed/Used in yFinance 0.2
"Short Term Investments" REAL, -- No Longer Needed/Used in yFinance 0.2`
"Net Recievables" REAL, -- No Longer Needed/Used in yFinance 0.2
"date" TIMESTAMP,
Foreign Key (stock_id) references stock(id)
);
