{{
    config(
        materialized='table'
    )
}}

with olist_orders_dataset as (

    select * from {{ source('staging', 'olist_orders_dataset') }}

)
select
    order_id,
    customer_id,
    order_status,
    cast(order_purchase_timestamp as timestamp) as orderPurchasedDate,
    cast(order_approved_at as timestamp) as orderApprovedDate,
    cast(order_delivered_carrier_date as timestamp) as orderCarrierPickupDate,
    cast(order_delivered_customer_date as timestamp) as orderDeliveredDate,
    cast(order_estimated_delivery_date as timestamp) as orderEstimatedDate
from olist_orders_dataset