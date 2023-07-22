SELECT DISTINCT stock_earnings.year, gics_sector, gics_subsector,  SUM(stock_earnings.Revenue) OVER(
PARTITION BY gics_sector, stock_earnings.Year 
order by gics_sector, gics_subsector) as Revenue
FROM stock, stock_earnings
WHERE stock_earnings.id = stock.id
GROUP BY gics_sector, stock_earnings.year
