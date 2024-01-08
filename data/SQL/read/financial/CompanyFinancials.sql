----------------------------------------------------------------------
-- SELECT Company Financial Statement
-- V2.0
-- Anthony Thomas-Bell
--
--Used for selecting the Financial Statement data for the selected stock via the stock_id
----------------------------------------------------------------------
SELECT
* FROM stock_financials WHERE stock_id = {}
UNION ALL
SELECT NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL,
       NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL,
       NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL,
       NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL,
       NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL,
       NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL,
       NULL, NULL
WHERE NOT EXISTS (SELECT 1 FROM stock_financials WHERE stock_id = {});