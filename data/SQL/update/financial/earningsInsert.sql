----------------------------------------------------------------------
-- INSERT INTO Earnings table.
-- V2.0
-- Anthony Thomas-Bell
--
-- add new data into Earnings - partial query since the dynamic part is done via python.
----------------------------------------------------------------------
INSERT INTO stock_earnings(
stock_id,
Year,
Earnings,
Revenue,
'date'
)
VALUES(
?,?,?,?,?,
)
