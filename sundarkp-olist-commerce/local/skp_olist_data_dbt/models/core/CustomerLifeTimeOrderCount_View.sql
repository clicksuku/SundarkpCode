{{ config(
    materialized='table'
) }}

with CustomerLTVOrders as (
    select * from 
    {{ ref('customersandorders') }}     
),
CustomerTotalOrders as(    
    SELECT customer_unique_id, COUNT(order_id) AS TotalOrders
        FROM
        {{ ref('customersandorders') }}     
        GROUP BY customer_unique_id
)

SELECT  CO.TotalOrders, count(distinct CS.Customer_Unique_ID) as CustomersCount
    from CustomerLTVOrders CS
    inner join
    CustomerTotalOrders CO
    on CS.Customer_Unique_ID = CO.Customer_Unique_ID
    GROUP BY CO.TotalOrders
