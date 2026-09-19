import os
import sys
import pandas as pd

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from config.config import PROCESSED_CSV

def run_pandas_smartcanteen_analytics():
    """
    Executes the 12 core Big Data SmartCanteen analytics queries on the 456,548 dataset
    using high-performance Pandas aggregation engine as a fast local alternative.
    """
    print("================================================================================")
    print("   BIG DATA SMARTCANTEEN ANALYTICS ENGINE (456,548 RECORDS)   ")
    print("================================================================ drop_emojis=True\n")

    if not os.path.exists(PROCESSED_CSV):
        print(f"Error: Processed dataset not found at {PROCESSED_CSV}")
        return

    df = pd.read_csv(PROCESSED_CSV)
    print(f"Dataset Loaded: {len(df):,} total canteen transactions.\n")

    # 1. Most Popular Food Items
    print("--- Query 1: Top 5 Most Popular Food Items ---")
    q1 = df.groupby(["category", "cuisine"])["quantity_sold"].sum().reset_index().sort_values(by="quantity_sold", ascending=False).head(5)
    print(q1.to_string(index=False))

    # 2. Least Popular Food Categories
    print("\n--- Query 2: Least Popular Food Categories ---")
    q2 = df.groupby("category")["quantity_sold"].sum().reset_index().sort_values(by="quantity_sold", ascending=True).head(5)
    print(q2.to_string(index=False))

    # 3. Demand by Day of the Week
    print("\n--- Query 3: Food Demand by Day of the Week ---")
    q3 = df.groupby("day_of_week")["quantity_sold"].agg(["sum", "mean"]).reset_index()
    q3.columns = ["day_of_week", "total_demand", "avg_demand"]
    print(q3.to_string(index=False))

    # 4. Demand Trend Across Weeks (First 5 Weeks Sample)
    print("\n--- Query 4: Weekly Demand Trend (First 5 Weeks) ---")
    q4 = df[df["week"] <= 5].groupby("week")[["quantity_sold", "revenue"]].sum().reset_index()
    print(q4.to_string(index=False))

    # 5. Peak Demand Periods (Promotions + Weather)
    print("\n--- Query 5: Peak Demand Periods (Promotions + Weather Impact) ---")
    q5 = df.groupby(["day_of_week", "weather", "promotion"])["quantity_sold"].mean().reset_index().sort_values(by="quantity_sold", ascending=False).head(5)
    print(q5.to_string(index=False))

    # 6. Revenue by Category
    print("\n--- Query 6: Total Revenue Realized by Category ---")
    q6 = df.groupby("category")[["quantity_sold", "revenue"]].sum().reset_index().sort_values(by="revenue", ascending=False)
    print(q6.to_string(index=False))

    # 7. Food Wastage Analysis (Top 5 Wastage Centers)
    print("\n--- Query 7: Food Wastage Analysis (Top 5 Highest Waste Canteens) ---")
    q7 = df.groupby("center_id")[["quantity_prepared", "quantity_sold", "food_waste", "waste_percentage"]].mean().reset_index().sort_values(by="waste_percentage", ascending=False).head(5)
    print(q7.to_string(index=False))

    # 8. Promotion vs Non-Promotion Demand
    print("\n--- Query 8: Promotion vs Non-Promotion Demand Impact ---")
    q8 = df.groupby("promotion").agg(
        total_tx=("transaction_id", "count"),
        total_orders=("quantity_sold", "sum"),
        avg_orders_per_tx=("quantity_sold", "mean")
    ).reset_index()
    print(q8.to_string(index=False))

    # 9. Center-Wise Demand Leaderboard (Top 5 Centers)
    print("\n--- Query 9: Canteen Center Leaderboard (Top 5 Centers) ---")
    q9 = df.groupby(["center_id", "center_type"])[["quantity_sold", "revenue", "waste_percentage"]].sum().reset_index().sort_values(by="quantity_sold", ascending=False).head(5)
    print(q9.to_string(index=False))

    print("\n================================================================================")
    print(" ANALYTICS ENGINE COMPLETED SUCCESSFULLY ")
    print("================================================================================\n")

if __name__ == "__main__":
    run_pandas_smartcanteen_analytics()
