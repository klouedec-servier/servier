SELECT
	t.date,
       	SUM(t.prod_price * t.prod_qty) AS ventes
FROM TRANSACTION t
WHERE t.date between '01/01/19' AND '31/12/19'
GROUP BY t.date
ORDER BY t.date
