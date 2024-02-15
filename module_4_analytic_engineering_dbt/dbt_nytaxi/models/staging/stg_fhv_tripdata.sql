{{ config(materialized='view') }}

select *,
from {{ source('staging','fhv_tripdata') }}
where EXTRACT(YEAR FROM pickup_datetime) = 2019

-- dbt build --m <model.sql> --var 'is_test_run: false'
{% if var('is_test_run', default=true) %}

  limit 100

{% endif %}