 SELECT stock_price.*, stock.company, ((adjusted_close-LAG(adjusted_close) OVER(ORDER BY company)) /LAG(adjusted_close) OVER(ORDER BY company)) *100 as ROI
FROM stock_price, stock
WHERE stock_price.stock_id = stock.id
ORDER BY company
LIMIT 300000
