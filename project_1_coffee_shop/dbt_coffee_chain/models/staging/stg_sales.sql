SELECT
  invoice_no AS invoice_no,
  date_time AS purchase_date_time,
  customer_id AS customer_id_sales,
  outlet AS outlet_id_sales,
  product AS product_id_sales,
  quantity AS quantitiy_sold,
  month AS month,
  EXTRACT(YEAR FROM date_time) AS year,
from {{ source('staging','sales') }}
WHERE invoice_no is NOT NULL