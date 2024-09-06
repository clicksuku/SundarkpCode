{{ config(
    materialized='table',
    partition_by={
      "field": "orderPurchasedDate",
      "data_type": "timestamp",
      "granularity": "day"
    }
) }}


with sellers as (
    select * from 
    {{ ref('stg_olist_sellers_dataset') }}     
),
orders as (
    select * from 
    {{ ref('stg_olist_orders_dataset') }}
),
orderItems as (
    select * from 
    {{ ref('stg_olist_order_items_dataset') }}
),
products as (
    select * from 
    {{ ref('stg_olist_products_dataset') }}
),
products_categoryname_english as (
    select * from 
    {{ ref('stg_product_category_name_translation') }}
)

select o.order_id, o.orderPurchasedDate, 
       oi.order_item_id, oi.seller_id, oi.product_id, 
       p.product_category_name, pc.product_category_name_english  
from orders o
    inner join orderItems oi
    on o.order_id = oi.order_id
    inner join sellers s
    on oi.seller_id = s.seller_id
    inner join products p
    on oi.product_id = p.product_id
    inner join products_categoryname_english pc
    on pc.product_category_name = p.product_category_name     