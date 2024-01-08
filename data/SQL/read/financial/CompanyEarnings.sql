----------------------------------------------------------------------
-- SELECT Company Earnings
-- V2.0
-- Anthony Thomas-Bell
--
--Used for selecting the earnings data for the selected stock via the stock_id
----------------------------------------------------------------------
SELECT
* FROM stock_earnings WHERE stock_id = {}
UNION ALL
SELECT NULL, NULL, NULL, NULL, NULL, NULL  -- Placeholder for columns to match the structure
WHERE NOT EXISTS (SELECT 1 FROM stock_earnings WHERE stock_id = {});