----------------------------------------------------------------------
-- CREATE earnings table yFinance.
-- V2.0
-- Anthony Thomas-Bell
--
-- Create Earnings table, used to be separate table but can now be calculated from Financials Table.
----------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS "stock_earnings"(
"id" INTEGER PRIMARY KEY, 
"stock_id" INTEGER,
"Year" INTEGER,
"Earnings" REAL, 
"Revenue" REAL,
"date" TIMESTAMP,
Foreign Key (stock_id) references stock(id)
)

SELECT