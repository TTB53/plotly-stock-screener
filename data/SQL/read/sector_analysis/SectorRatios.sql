SELECT 
DISTINCT
	stock_financials.year,  gics_sector,
	(SUM("Gross Profit")/ SUM("Total Revenue"))*100 as gross_profit_margin, 
	(SUM("Net Income")/SUM("Total Revenue"))*100 as profit_margin, 
	(SUM("Operating Income")/SUM("Total Revenue"))*100 as operating_margin,
	(SUM("Net Income")/SUM("Total Assets"))*100 as return_on_assets, 
	(SUM("Net Income")/(SUM("Total Assets")-SUM("Total Liab"))) *100 as return_on_equity
FROM 
	stock, stock_financials, stock_balance_sheet
WHERE 
	stock.id = stock_financials.stock_id=stock_balance_sheet.stock_id
GROUP BY 
	stock_financials.year, gics_sector 
ORDER BY 
	gics_sector ASC, stock_financials.year ASC