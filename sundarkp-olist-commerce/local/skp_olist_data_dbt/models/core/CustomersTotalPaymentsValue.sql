{{ config(
    materialized='table'
)}}

with customersnorders as (
    select * from 
    {{ ref('customersandorders') }}     
),
payments as (
    select * from 
    {{ ref('stg_olist_order_payments_dataset') }}
)

SELECT
  co.customer_unique_id, 
  SUM(
     pymt.`payment_value`
  ) AS `sum`
    FROM
        customersnorders co
    LEFT JOIN payments pymt ON co.order_id = pymt.order_id
    GROUP BY
        co.customer_unique_id
    ORDER BY
    `sum` DESC,
    co.customer_unique_id ASC
