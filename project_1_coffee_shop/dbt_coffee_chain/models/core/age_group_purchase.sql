{{ config(
    materialized='table'
) }}

SELECT
    SUM(total_price) as total_revenue_by_age,
    product_name,
    SUM(CAST(quantitiy_sold AS NUMERIC)) as total_quantity_by_age,
  CASE
    WHEN age BETWEEN 21 AND 25 THEN '0-20'
    WHEN age BETWEEN 25 AND 30 THEN '21-30'
    WHEN age BETWEEN 30 AND 40 THEN '30-40'
    WHEN age BETWEEN 40 and 50 THEN '40-50'
    ELSE 'Over 50'
  END AS age_group
FROM
  {{ref('fact_sales')}}
GROUP BY
  age_group, product_name
ORDER BY
  age_group