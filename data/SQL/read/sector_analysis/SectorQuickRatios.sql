----------------------------------------------------------------------
-- SELECT Sector Quick Ratios
-- V2.0
-- Anthony Thomas-Bell
--
--Used for getting the quick and dirty ratios for each category that denotes a healthy business.
--Activity, Solvency, Liquidity, Profitiability, and if you want to include it, Market Values
-- This is a partial to be completed in python
----------------------------------------------------------------------
SELECT
--stock_balance_sheet.stock_id,
stock_balance_sheet."year",
gics_sector,
-- ("Total Assets" - "Total Liab") is Shareholders_Equity,
(stock_balance_sheet."Total Current Assets"/stock_balance_sheet."Total Current Liabilities") as Current_Ratio,
("Total Assets" - ("Total Assets" - "Total Liab"))/"Total Assets" as Debt_to_Equity,
("Total Revenue"/"Total Assets") as Asset_Turnover,
(stock_financials."Net Income"/ "Total Revenue") as Profit_Margin,
(stock_financials."Net Income"/("Total Assets" - "Total Liab")) as Return_on_Equity
FROM
stock_balance_sheet
LEFT JOIN
stock_financials, stock
WHERE
stock_balance_sheet.stock_id = stock_financials.stock_id
AND stock_balance_sheet.stock_id = stock.id
--AND gics_sector = 'Utilities'
--GROUP BY gics_sector and stock_balance_sheet.year
-- AND stock_balance_sheet.stock_id = 33
-- GROUP BY stock_balance_sheet.year