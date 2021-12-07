CREATE TABLE IF NOT EXISTS "stock_earnings"(
"id" INTEGER PRIMARY KEY, 
"stock_id" INTEGER,
"Year" INTEGER,
"Earnings" REAL, 
"Revenue" REAL,
"date" TIMESTAMP,
Foreign Key (stock_id) references stock(id)
)