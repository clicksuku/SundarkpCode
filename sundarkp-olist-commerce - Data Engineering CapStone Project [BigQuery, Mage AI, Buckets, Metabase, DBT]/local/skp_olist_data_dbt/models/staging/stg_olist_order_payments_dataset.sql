{{
    config(
        materialized='table'
    )
}}

with olist_order_payments_dataset as (

    select * from {{ source('staging', 'olist_order_payments_dataset') }}

)
select
    order_id,
    payment_sequential,
    payment_type,
    payment_installments,
    payment_value
from olist_order_payments_dataset