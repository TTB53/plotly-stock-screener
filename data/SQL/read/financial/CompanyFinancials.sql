----------------------------------------------------------------------
-- SELECT Company Financial Statement
-- V2.0
-- Anthony Thomas-Bell
--
--Used for selecting the Financial Statement data for the selected stock via the stock_id
----------------------------------------------------------------------
SELECT DISTINCT *
FROM
stock_financials
--WHERE stock_balance_sheet.stock_id=