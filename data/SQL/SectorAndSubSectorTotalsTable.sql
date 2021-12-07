
CREATE TABLE IF NOT EXISTS sector_subsector_totals AS 
SELECT DISTINCT stock_balance_sheet.year, gics_sector, gics_subsector, 
sum("Total Assets") OVER (PARTITION BY gics_sector, stock_balance_sheet.year ORDER BY gics_sector, gics_subsector) as tot_assets,
sum("Total Current Assets") OVER(PARTITION BY gics_sector,stock_balance_sheet.year ORDER BY gics_sector, gics_subsector) as tot_curr_assets,
sum("Total Liab") OVER(PARTITION BY gics_sector, stock_balance_sheet.year ORDER BY gics_sector, gics_subsector) as tot_liabilities,
sum("Total Current Liabilities") OVER(PARTITION BY gics_sector,stock_balance_sheet.year ORDER BY gics_sector, gics_subsector) as tot_curr_liabilities,
sum("Cash") OVER(PARTITION BY gics_sector,stock_balance_sheet.year ORDER BY gics_sector, gics_subsector) as tot_cash,
sum("Long Term Debt") OVER(PARTITION BY gics_sector,stock_balance_sheet.year ORDER BY gics_sector, gics_subsector)+ sum("Short Long Term Debt") OVER(PARTITION BY gics_sector,stock_balance_sheet.year ORDER BY gics_sector, gics_subsector)as tot_debt  
FROM stock,stock_balance_sheet, stock_earnings 
WHERE stock_balance_sheet.stock_id = stock.id = stock_earnings.stock_id 
GROUP BY stock_balance_sheet.year, gics_sector;
