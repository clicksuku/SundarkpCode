{{
    config(
        materialized='table'
    )
}}

with product_category_name_translation as (

    select * from {{ source('staging', 'product_category_name_translation') }}

)
select
    product_category_name,
    product_category_name_english
from product_category_name_translation