{{ config(
    materialized='table'
) }}

SELECT 
    outlet_state,
    SUM(total_price) as total_revenue_by_product,
    product_name,
    SUM(CAST(quantitiy_sold AS NUMERIC)) as total_quantity_by_product

FROM {{ref("fact_sales")}}

GROUP BY outlet_state,product_name