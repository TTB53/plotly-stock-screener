SELECT stock_price.date, company, printf('%.2f',Close) as Close, gics_sector,printf('%.3f',(LAG(Close, 1, 0 ) OVER ( 
		PARTITION BY company
		ORDER BY stock_price.stock_id, company)-Close)/Close)*100 as DailyPercentChange FROM stock, stock_price where stock_price.stock_id = stock.id;