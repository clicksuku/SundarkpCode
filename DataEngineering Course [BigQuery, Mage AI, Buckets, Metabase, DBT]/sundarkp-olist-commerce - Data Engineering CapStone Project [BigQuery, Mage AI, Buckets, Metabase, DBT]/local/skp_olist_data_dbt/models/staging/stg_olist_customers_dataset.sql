{{
    config(
        materialized='table'
    )
}}

with olist_customers_dataset as (

    select * from {{ source('staging', 'olist_customers_dataset') }}

)
select
    customer_id,
    customer_unique_id,
    customer_zip_code_prefix,
    customer_city,
    customer_state
from olist_customers_dataset