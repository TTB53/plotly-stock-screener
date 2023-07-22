----------------------------------------------------------------------
-- SELECT Company Information
-- V2.0
-- Anthony Thomas-Bell
--
--Used for getting the bare minimum for the company of interests information. Is a par
-- query because the dynamic part happens in Python.
----------------------------------------------------------------------
SELECT symbol, id, company, gics_sector, gics_subsector
FROM stock
-- WHERE stock.symbol = symbol_of_interest