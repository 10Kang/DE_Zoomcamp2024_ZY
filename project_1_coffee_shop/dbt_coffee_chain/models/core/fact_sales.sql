{{ config(materialized='table') }}

with sales_data as (
    select *
    from {{ ref('stg_sales') }}
), 
customer_data as (
    select * 
    from {{ ref('stg_customer') }}
), 
product_data as (
    select * 
    from {{ ref('product') }}
),
outlet_data as (
    select *
    from {{ ref('outlet')}}
)
select sales_data.invoice_no, 
    sales_data.purchase_date_time, 
    customer_data.customer_id as customer_id,
    outlet_data.outlet_id as outlet_id,
    product_data.product_id as product_id,
    sales_data.quantitiy_sold,
    sales_data.month,
    sales_data.year,
    product_data.product_name,
    CAST(REGEXP_EXTRACT(product_data.product_price, r'(\d+\.\d+)') AS NUMERIC) as product_price,
    CAST(sales_data.quantitiy_sold AS NUMERIC) *CAST(REGEXP_EXTRACT(product_data.product_price, r'(\d+\.\d+)') AS NUMERIC) as total_price,
    outlet_data.outlet_name,
    outlet_data.outlet_address,
    outlet_data.outlet_state,
    outlet_data.postcode as outlet_postcode,
    outlet_data.district as outlet_district,
    customer_data.first_name,
    customer_data.last_name,
    customer_data.gender,
    customer_data.birthday,
    customer_data.email,
    customer_data.phone_no,
    customer_data.age
from sales_data
inner join customer_data 
on sales_data.customer_id_sales = customer_data.customer_id
inner join outlet_data 
on sales_data.outlet_id_sales = outlet_data.outlet_id
inner join product_data
on sales_data.product_id_sales = product_data.product_id