{{ config(
    materialized='table',
    partition_by={
      "field": "orderPurchasedDate",
      "data_type": "timestamp",
      "granularity": "day"
    }
)}}


with customers as (
    select * from 
    {{ ref('stg_olist_customers_dataset') }}     
),
orders as (
    select * from 
    {{ ref('stg_olist_orders_dataset') }}
    

)

select c.customer_unique_id, c.customer_id, o.order_id, o.orderPurchasedDate from customers c
    inner join orders o
    on c.customer_id = o.customer_id
     