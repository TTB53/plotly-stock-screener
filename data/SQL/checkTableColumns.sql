----------------------------------------------------------------------
-- Utility Query to check if a column name exists in a table.
-- V2.0
-- Anthony Thomas-Bell
--
--CHECK IF THE COLUMN_NAME IN TABLENAME EXISTS. WILL RETURN A NUMBER GREATER THAN 0 IF IT DOES.
-- partial query since the dynamic part is done via python.
----------------------------------------------------------------------


SELECT COUNT(*) AS CNTREC FROM pragma_table_info('tablename') WHERE name='column_name';