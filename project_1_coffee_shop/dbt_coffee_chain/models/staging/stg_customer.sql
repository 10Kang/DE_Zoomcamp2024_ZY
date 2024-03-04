{{ config(materialized='view') }}

select *,
    DATE_DIFF(CURRENT_DATE(), DATE(birthday),YEAR) AS age
from {{ source('staging','customer') }}

-- dbt build --m <model.sql> --var 'is_test_run: false'
{% if var('is_test_run', default=true) %}

  limit 100

{% endif %}
