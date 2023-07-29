----------------------------------------------------------------------
-- SELECT All Prices.
-- V2.0
-- Anthony Thomas-Bell
--
-- Query to get the Prices for the stocks in the database.
----------------------------------------------------------------------
SELECT stock.company, stock.gics_sector,stock.gics_subsector, stock_price.*
FROM stock_price, stock
WHERE stock_price.stock_id=stock.id