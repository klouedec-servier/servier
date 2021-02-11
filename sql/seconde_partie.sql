SELECT 
	t.client_id, 
	SUM(IF(p.product_type = 'MEUBLE', t.prod_price * t.prod_qty, 0)) AS ventes_meuble,
	SUM(IF(p.product_type = 'DECO', t.prod_price * t.prod_qty, 0)) AS ventes_deco
FROM TRANSACTION t
INNER JOIN PRODUCT_NOMENCLATURE p
ON t.prod_id = p.product_id
GROUP BY t.client_id
