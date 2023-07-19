----------------------------------------------------------------------
-- Major Shareholders from yFinance API
-- V2.0
-- Anthony Thomas-Bell
--
--
----------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS "stock_major_holders"(
"id" INTEGER PRIMARY KEY,
"stock_id" INTEGER,
"% of Shares Held by All Insider" REAL,
"% of Shares Held by Institutions" REAL,
"% of Float Held by Institutions" REAL,
"Number of Institutions Holding Shares" INTEGER,
"date" TIMESTAMP
Foreign Key (stock_id) references stock(id)
)