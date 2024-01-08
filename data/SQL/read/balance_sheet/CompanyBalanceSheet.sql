----------------------------------------------------------------------
-- SELECT Company Balance Sheet
-- V2.0
-- Anthony Thomas-Bell
--
--Used for selecting the balance sheet data for the selected stock via the stock_id
----------------------------------------------------------------------
SELECT
* FROM stock_balance_sheet WHERE stock_id = {}
UNION ALL
SELECT NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL,
       NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL,
       NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL,
       NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL,
       NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL,
       NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL,
       NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL,
       NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL,
       NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL,
       NULL, NULL, NULL, NULL
WHERE NOT EXISTS (SELECT 1 FROM stock_balance_sheet WHERE stock_id = {});