--CHECK IF THE COLUMN_NAME IN TABLENAME EXISTS. WILL RETURN A NUMBER GREATER THAN 0 IF IT DOES. 
SELECT COUNT(*) AS CNTREC FROM pragma_table_info('tablename') WHERE name='column_name';