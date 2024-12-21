# Customer Analytics Visualizations

**<u>Total Orders X Total Customers View</u>**

> SELECT
> \`olist.CustomerLifeTimeOrderCount_View\`.\`TotalOrders\` AS
> \`TotalOrders\`,
>
> \`olist.CustomerLifeTimeOrderCount_View\`.\`CustomersCount\` AS
> \`CustomersCount\`
>
> FROM
>
> \`olist.CustomerLifeTimeOrderCount_View\`

<img src="https://github.com/clicksuku/sundarkp-olist-commerce/blob/main/Visualizations/Customer%20Lifetime%20OrderCount.png" style="width:6.26806in;height:2.56111in"
alt="A graph with a line Description automatically generated with medium confidence" />

**<u>Orders Count grouped by Purchase Dates</u>**

> SELECT
>
> TIMESTAMP_TRUNC(
>
> \`olist.customersandorders\`.\`orderPurchasedDate\`,
>
> day
>
> ) AS \`orderPurchasedDate\`,
>
> COUNT(\*) AS \`count\`
>
> FROM
>
> \`olist.customersandorders\`
>
> GROUP BY
>
> \`orderPurchasedDate\`
>
> ORDER BY
>
> \`orderPurchasedDate\` ASC

<img src="https://github.com/clicksuku/sundarkp-olist-commerce/blob/main/Visualizations/Orders%20Count%20grouped%20by%20Purchase%20Dates.png" style="width:6.86157in;height:2.49802in"
alt="A graph showing a line Description automatically generated with medium confidence" />

**Customer LTV Ranges**

> select sum(case when ctv.sum \<= 500 then 1 else 0 end) as
> \`LessThan500\`,
>
> sum(case when ctv.sum \> 501 and ctv.sum \<= 1000 then 1 else 0 end)
> as \`500To1000\`,
>
> sum(case when ctv.sum \> 1001 and ctv.sum \<= 10000 then 1 else 0 end)
> as \`1KTo10K\`,
>
> sum(case when ctv.sum \> 10001 then 1 else 0 end) as \`GT10K\`
>
> from \`olist.CustomersTotalPaymentsValue\` ctv;

<img src="https://github.com/clicksuku/sundarkp-olist-commerce/blob/main/Visualizations/Customer%20LifeTime%20Value%20Ranges.png" style="width:6.26806in;height:1.1375in"
alt="A screenshot of a cellphone Description automatically generated" />

**OList Store Distribution**

<img src="https://github.com/clicksuku/sundarkp-olist-commerce/blob/main/Visualizations/Olist.jpg" style="width:6.26806in;height:4.05208in"
alt="A screenshot of a map Description automatically generated" />
