{{
    config(
        materialized='table'
    )
}}

with olist_sellers_dataset as (

    select * from {{ source('staging', 'olist_sellers_dataset') }}

)

select
    seller_id,
    seller_zip_code_prefix,
    seller_city,
    seller_state

from olist_sellers_dataset