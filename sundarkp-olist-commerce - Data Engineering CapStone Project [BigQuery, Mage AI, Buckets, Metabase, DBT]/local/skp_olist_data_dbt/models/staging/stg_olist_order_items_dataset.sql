{{
    config(
        materialized='table'
    )
}}

with olist_order_items_dataset as (

    select * from {{ source('staging', 'olist_order_items_dataset') }}

)

select
    order_id,
    order_item_id,
    product_id,
    seller_id,
    shipping_limit_date,
    price,
    freight_value

from olist_order_items_dataset