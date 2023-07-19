----------------------------------------------------------------------
-- Institutional Holders from yFinance API
-- V2.0
-- Anthony Thomas-Bell
--
--
----------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS "stock_institution_holders"(
"id" INTEGER PRIMARY KEY,
"stock_id" INTEGER,
"Holder" TEXT,
"Shares" INTEGER,
"Date Reported" INTEGER,
"% Out" REAL,
"Value" INTEGER,
"date" TIMESTAMP
Foreign Key (stock_id) references stock(id)
)