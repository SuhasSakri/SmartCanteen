-- ============================================================
-- SmartCanteen Big Data SQL Analytics Queries (Spark SQL / HDFS)
-- ============================================================

-- 1. Most Popular Food Items
SELECT food_item, category, cuisine, SUM(quantity_sold) AS total_orders_sold
FROM smartcanteen
GROUP BY food_item, category, cuisine
ORDER BY total_orders_sold DESC
LIMIT 10;

-- 2. Least Popular Food Items
SELECT food_item, category, cuisine, SUM(quantity_sold) AS total_orders_sold
FROM smartcanteen
GROUP BY food_item, category, cuisine
ORDER BY total_orders_sold ASC
LIMIT 5;

-- 3. Demand by Day of the Week
SELECT day_of_week, SUM(quantity_sold) AS total_daily_demand, ROUND(AVG(quantity_sold), 2) AS avg_daily_demand
FROM smartcanteen
GROUP BY day_of_week
ORDER BY total_daily_demand DESC;

-- 4. Demand by Week
SELECT week, SUM(quantity_sold) AS weekly_demand, ROUND(SUM(revenue), 2) AS weekly_revenue
FROM smartcanteen
GROUP BY week
ORDER BY week ASC;

-- 5. Demand by Month (4-week blocks)
SELECT CEIL(week / 4) AS month_block, SUM(quantity_sold) AS monthly_demand, ROUND(SUM(revenue), 2) AS monthly_revenue
FROM smartcanteen
GROUP BY month_block
ORDER BY month_block ASC;

-- 6. Peak Demand Periods (Promotions + Weather Impact)
SELECT day_of_week, weather, promotion, ROUND(AVG(quantity_sold), 2) AS avg_demand
FROM smartcanteen
GROUP BY day_of_week, weather, promotion
ORDER BY avg_demand DESC
LIMIT 10;

-- 7. Revenue by Food Item
SELECT food_item, SUM(quantity_sold) AS units_sold, ROUND(SUM(revenue), 2) AS total_item_revenue
FROM smartcanteen
GROUP BY food_item
ORDER BY total_item_revenue DESC;

-- 8. Revenue by Category
SELECT category, COUNT(DISTINCT food_item) AS total_items, SUM(quantity_sold) AS units_sold, ROUND(SUM(revenue), 2) AS category_revenue
FROM smartcanteen
GROUP BY category
ORDER BY category_revenue DESC;

-- 9. Food-Wastage Analysis
SELECT center_id, SUM(quantity_prepared) AS total_prepared, SUM(quantity_sold) AS total_sold, SUM(food_waste) AS total_waste_units, ROUND(AVG(waste_percentage), 2) AS avg_waste_pct
FROM smartcanteen
GROUP BY center_id
ORDER BY avg_waste_pct DESC;

-- 10. Promotion vs Non-Promotion Demand
SELECT promotion, COUNT(transaction_id) AS total_transactions, SUM(quantity_sold) AS total_orders, ROUND(AVG(quantity_sold), 2) AS avg_orders_per_tx
FROM smartcanteen
GROUP BY promotion;

-- 11. Price vs Demand Analysis
SELECT price, ROUND(AVG(quantity_sold), 2) AS avg_demand, COUNT(transaction_id) AS record_count
FROM smartcanteen
GROUP BY price
ORDER BY price ASC;

-- 12. Canteen / Center-Wise Demand
SELECT center_id, SUM(quantity_sold) AS total_center_demand, ROUND(SUM(revenue), 2) AS total_center_revenue, ROUND(AVG(waste_percentage), 2) AS avg_waste_pct
FROM smartcanteen
GROUP BY center_id
ORDER BY total_center_demand DESC;
