import os
import sys
import numpy as np
import pandas as pd

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from config.config import TRAIN_CSV, MEAL_INFO_CSV, CENTER_INFO_CSV, PROCESSED_CSV, PROCESSED_DATA_DIR

def prepare_smartcanteen_dataset(seed=42):
    """
    Phase 2: Merges raw Kaggle datasets (train.csv, meal_info.csv, fulfilment_center_info.csv)
    and derives SmartCanteen domain metrics:
    - transaction_id
    - day_of_week & calendar metrics
    - students_present
    - holiday
    - weather
    - quantity_sold (from num_orders)
    - quantity_prepared
    - food_waste
    - revenue
    - waste_percentage
    """
    np.random.seed(seed)
    print("================================================================================")
    print("   PHASE 2: DATASET PREPARATION, MERGING & DERIVED FEATURE ENGINEERING   ")
    print("================================================================================\n")

    # 1. Load Datasets
    print("[1/5] Ingesting raw Kaggle CSV files...")
    train_df = pd.read_csv(TRAIN_CSV)
    meal_df = pd.read_csv(MEAL_INFO_CSV)
    center_df = pd.read_csv(CENTER_INFO_CSV)

    # 2. Merge Datasets
    print("[2/5] Merging train.csv with meal_info.csv and fulfilment_center_info.csv...")
    df = train_df.merge(meal_df, on="meal_id", how="left")
    df = df.merge(center_df, on="center_id", how="left")
    print(f"  - Merged Dataframe Shape: {df.shape[0]:,} rows × {df.shape[1]} columns")

    # 3. Data Cleaning & Type Conversions
    print("[3/5] Cleaning data and verifying zero missing/duplicate records...")
    df.drop_duplicates(inplace=True)
    df.fillna(method="ffill", inplace=True)

    # 4. Feature Engineering & SmartCanteen Domain Derivations
    print("[4/5] Engineering SmartCanteen domain metrics...")
    
    # Map transaction_id
    df["transaction_id"] = "TXN-" + df["id"].astype(str)
    
    # Map calendar day of week from week index
    days_list = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    df["day_of_week"] = df["id"].apply(lambda x: days_list[x % 7])
    df["holiday"] = df["day_of_week"].apply(lambda d: 1 if d in ["Saturday", "Sunday"] else 0)

    # Weather simulation based on center & week
    weather_choices = ["Sunny", "Rainy", "Cold", "Hot"]
    df["weather"] = np.random.choice(weather_choices, size=len(df), p=[0.45, 0.25, 0.15, 0.15])

    # Estimated student attendance based on day type & op_area
    df["students_present"] = np.where(
        df["holiday"] == 1,
        (df["op_area"] * 120 + np.random.randint(100, 300, size=len(df))).astype(int),
        (df["op_area"] * 500 + np.random.randint(800, 1500, size=len(df))).astype(int)
    )

    # Promotion flag
    df["promotion"] = np.where((df["emailer_for_promotion"] == 1) | (df["homepage_featured"] == 1), 1, 0)

    # Quantity sold = Kaggle num_orders
    df["quantity_sold"] = df["num_orders"]

    # Quantity prepared = quantity_sold + kitchen buffer (simulating actual preparation)
    buffer_percentages = np.random.uniform(0.08, 0.22, size=len(df))
    df["quantity_prepared"] = (df["quantity_sold"] * (1 + buffer_percentages)).astype(int)

    # Derived domain metrics
    df["food_waste"] = df["quantity_prepared"] - df["quantity_sold"]
    df["price"] = df["checkout_price"]
    df["revenue"] = (df["quantity_sold"] * df["price"]).round(2)
    df["waste_percentage"] = ((df["food_waste"] / df["quantity_prepared"]) * 100).round(2)
    from config.config import FULL_MEAL_NAMES
    df["food_item"] = df["meal_id"].map(FULL_MEAL_NAMES).fillna(df["category"] + " #" + df["meal_id"].astype(str))

    # Organize final column layout
    final_columns = [
        "transaction_id", "id", "week", "day_of_week", "center_id", "meal_id",
        "food_item", "category", "cuisine", "center_type", "op_area", "city_code", "region_code",
        "price", "base_price", "emailer_for_promotion", "homepage_featured", "promotion",
        "students_present", "holiday", "weather",
        "quantity_prepared", "quantity_sold", "food_waste", "revenue", "waste_percentage"
    ]
    processed_df = df[final_columns]

    # 5. Export Processed Dataset
    print("[5/5] Exporting processed dataset...")
    os.makedirs(PROCESSED_DATA_DIR, exist_ok=True)
    processed_df.to_csv(PROCESSED_CSV, index=False)
    print(f"  - SavedProcessed SmartCanteen Dataset: {processed_df.shape[0]:,} rows at {PROCESSED_CSV}")
    print(f"  - Total Calculated Revenue: Rs. {processed_df['revenue'].sum():,.2f}")
    print(f"  - Total Prepared Quantity : {processed_df['quantity_prepared'].sum():,} units")
    print(f"  - Total Quantity Sold     : {processed_df['quantity_sold'].sum():,} units")
    print(f"  - Total Food Waste        : {processed_df['food_waste'].sum():,} units ({processed_df['waste_percentage'].mean():.2f}% avg waste)")

    print("================================================================================")
    print(" PHASE 2 COMPLETED SUCCESSFULLY ")
    print("================================================================================")

    return processed_df

if __name__ == "__main__":
    prepare_smartcanteen_dataset()
