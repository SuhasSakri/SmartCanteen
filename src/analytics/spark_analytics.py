import os
import sys

# Add root directory to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from config.config import PROCESSED_CSV

def run_pyspark_smartcanteen_analytics():
    """
    Phase 4 & Phase 5: PySpark Distributed Data Processing & Spark SQL Analytics.
    Executes 12 core analytical queries on the 456,548 record SmartCanteen dataset.
    """
    print("================================================================================")
    print("   PHASE 4 & 5: PYSPARK DISTRIBUTED PROCESSING & SPARK SQL ANALYTICS   ")
    print("================================================================================\n")

    try:
        from pyspark.sql import SparkSession
        from pyspark.sql import functions as F

        # 1. Initialize PySpark Session
        print("[1/3] Initializing Apache Spark Session...")
        spark = SparkSession.builder \
            .appName("SmartCanteen-BigData-Analytics") \
            .config("spark.driver.memory", "4g") \
            .master("local[*]") \
            .getOrCreate()

        spark.sparkContext.setLogLevel("ERROR")
        print(f"  - Spark Version : {spark.version}")
        print(f"  - Master Node   : {spark.sparkContext.master}\n")

        # 2. Ingest Dataset into Spark DataFrame
        print("[2/3] Loading processed dataset into PySpark DataFrame...")
        df_spark = spark.read.csv(PROCESSED_CSV, header=True, inferSchema=True)
        total_records = df_spark.count()
        print(f"  - Spark DataFrame Loaded: {total_records:,} rows")

        # Register Spark SQL Temp View
        df_spark.createOrReplaceTempView("smartcanteen")

        # 3. Execute Spark SQL Analytical Queries
        print("\n[3/3] Executing Spark SQL Analytics Engine...\n")

        queries = [
            ("Query 1: Top 5 Most Popular Food Items", """
                SELECT category, cuisine, SUM(quantity_sold) AS total_orders_sold, ROUND(SUM(revenue), 2) AS total_revenue
                FROM smartcanteen
                GROUP BY category, cuisine
                ORDER BY total_orders_sold DESC
                LIMIT 5
            """),
            ("Query 2: Least Popular Food Categories", """
                SELECT category, SUM(quantity_sold) AS total_orders_sold, ROUND(AVG(quantity_sold), 2) AS avg_orders
                FROM smartcanteen
                GROUP BY category
                ORDER BY total_orders_sold ASC
                LIMIT 5
            """),
            ("Query 3: Food Demand by Day of the Week", """
                SELECT day_of_week, SUM(quantity_sold) AS total_daily_demand, ROUND(AVG(quantity_sold), 2) AS avg_daily_demand
                FROM smartcanteen
                GROUP BY day_of_week
                ORDER BY total_daily_demand DESC
            """),
            ("Query 4: Demand Trend Across Weeks (First 10 Weeks Sample)", """
                SELECT week, SUM(quantity_sold) AS weekly_demand, ROUND(SUM(revenue), 2) AS weekly_revenue
                FROM smartcanteen
                WHERE week <= 10
                GROUP BY week
                ORDER BY week ASC
            """),
            ("Query 5: Monthly Demand Blocks (4-Week Aggregations)", """
                SELECT CAST(CEIL(week / 4) AS INT) AS month_block, SUM(quantity_sold) AS monthly_demand, ROUND(SUM(revenue), 2) AS monthly_revenue
                FROM smartcanteen
                WHERE week <= 20
                GROUP BY CAST(CEIL(week / 4) AS INT)
                ORDER BY month_block ASC
            """),
            ("Query 6: Peak Demand Periods (Promotions + Weather Impact)", """
                SELECT day_of_week, weather, promotion, ROUND(AVG(quantity_sold), 2) AS avg_demand
                FROM smartcanteen
                GROUP BY day_of_week, weather, promotion
                ORDER BY avg_demand DESC
                LIMIT 5
            """),
            ("Query 7: Top Revenue Generating Food Categories", """
                SELECT category, SUM(quantity_sold) AS units_sold, ROUND(SUM(revenue), 2) AS total_revenue
                FROM smartcanteen
                GROUP BY category
                ORDER BY total_revenue DESC
                LIMIT 5
            """),
            ("Query 8: Revenue by Cuisine Type", """
                SELECT cuisine, COUNT(DISTINCT meal_id) AS total_meals, SUM(quantity_sold) AS units_sold, ROUND(SUM(revenue), 2) AS total_revenue
                FROM smartcanteen
                GROUP BY cuisine
                ORDER BY total_revenue DESC
            """),
            ("Query 9: Canteen Food Wastage Analysis (Top 5 Highest Waste Centers)", """
                SELECT center_id, SUM(quantity_prepared) AS total_prepared, SUM(quantity_sold) AS total_sold, SUM(food_waste) AS total_waste_units, ROUND(AVG(waste_percentage), 2) AS avg_waste_pct
                FROM smartcanteen
                GROUP BY center_id
                ORDER BY avg_waste_pct DESC
                LIMIT 5
            """),
            ("Query 10: Promotion vs Non-Promotion Demand Impact", """
                SELECT promotion, COUNT(transaction_id) AS total_transactions, SUM(quantity_sold) AS total_orders, ROUND(AVG(quantity_sold), 2) AS avg_orders_per_tx
                FROM smartcanteen
                GROUP BY promotion
            """),
            ("Query 11: Price Bucket vs Average Demand", """
                SELECT CAST(ROUND(price / 100) * 100 AS INT) AS price_bucket, ROUND(AVG(quantity_sold), 2) AS avg_demand, COUNT(transaction_id) AS total_tx
                FROM smartcanteen
                GROUP BY CAST(ROUND(price / 100) * 100 AS INT)
                ORDER BY price_bucket ASC
            """),
            ("Query 12: Canteen / Center-Wise Demand Leaderboard (Top 5 Centers)", """
                SELECT center_id, center_type, SUM(quantity_sold) AS center_demand, ROUND(SUM(revenue), 2) AS center_revenue, ROUND(AVG(waste_percentage), 2) AS avg_waste_pct
                FROM smartcanteen
                GROUP BY center_id, center_type
                ORDER BY center_demand DESC
                LIMIT 5
            """)
        ]

        for title, query in queries:
            print(f"--- {title} ---")
            spark.sql(query).show(truncate=False)

        print("================================================================================")
        print(" PHASES 4 & 5 SPARK ANALYTICS COMPLETED SUCCESSFULLY ")
        print("================================================================================")

        spark.stop()
        return True

    except Exception as e:
        print(f"PySpark Error / Environment Check: {e}")
        return False

if __name__ == "__main__":
    run_pyspark_smartcanteen_analytics()
