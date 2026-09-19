import os
import sys
import pandas as pd

# Add root directory to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from config.config import TRAIN_CSV, MEAL_INFO_CSV, CENTER_INFO_CSV, TEST_CSV

def inspect_kaggle_dataset():
    """
    Phase 1: Inspects the real Kaggle Food Demand dataset files in archive/foodDemand_train/.
    Prints schema details, row counts, missing values, duplicate checks, and field statistics.
    """
    print("================================================================================")
    print("   PHASE 1: KAGGLE FOOD DEMAND DATASET INSPECTION & UNDERSTANDING   ")
    print("================================================================ drop_emojis=True\n")

    # 1. Load Raw Datasets
    print("[1/4] Loading Raw Datasets from archive/...")
    train_df = pd.read_csv(TRAIN_CSV)
    meal_df = pd.read_csv(MEAL_INFO_CSV)
    center_df = pd.read_csv(CENTER_INFO_CSV)
    test_df = pd.read_csv(TEST_CSV)

    print(f"  - train.csv                  : {train_df.shape[0]:,} rows | {train_df.shape[1]} columns")
    print(f"  - meal_info.csv              : {meal_df.shape[0]:,} rows | {meal_df.shape[1]} columns")
    print(f"  - fulfilment_center_info.csv : {center_df.shape[0]:,} rows | {center_df.shape[1]} columns")
    print(f"  - food_Demand_test.csv       : {test_df.shape[0]:,} rows | {test_df.shape[1]} columns\n")

    # 2. Schema Inspection & Data Types
    print("[2/4] Inspecting Data Types & Schemas:")
    print("\n--- train.csv Schema ---")
    print(train_df.dtypes.to_string())

    print("\n--- meal_info.csv Schema ---")
    print(meal_df.dtypes.to_string())

    print("\n--- fulfilment_center_info.csv Schema ---")
    print(center_df.dtypes.to_string())

    # 3. Missing Value & Duplicate Inspection
    print("\n[3/4] Checking Missing Values & Duplicates:")
    print(f"  - train.csv Missing Values        : {train_df.isnull().sum().sum()}")
    print(f"  - train.csv Duplicates            : {train_df.duplicated().sum()}")
    print(f"  - meal_info.csv Missing Values    : {meal_df.isnull().sum().sum()}")
    print(f"  - fulfilment_center_info Missing  : {center_df.isnull().sum().sum()}")

    # 4. Statistical Summary & Unique Values
    print("\n[4/4] Data Range & Field Distribution Summary:")
    print(f"  - Weeks Covered in Train Dataset   : Week {train_df['week'].min()} to Week {train_df['week'].max()} ({train_df['week'].nunique()} total weeks)")
    print(f"  - Total Unique Canteen Centers     : {train_df['center_id'].nunique()} centers")
    print(f"  - Total Unique Meals / Dishes      : {train_df['meal_id'].nunique()} meals")
    print(f"  - Food Categories Available        : {list(meal_df['category'].unique())}")
    print(f"  - Cuisines Available               : {list(meal_df['cuisine'].unique())}")
    print(f"  - Center Types Available           : {list(center_df['center_type'].unique())}")
    print(f"  - Checkout Price Range             : Rs. {train_df['checkout_price'].min():.2f} - Rs. {train_df['checkout_price'].max():.2f}")
    print(f"  - Base Price Range                 : Rs. {train_df['base_price'].min():.2f} - Rs. {train_df['base_price'].max():.2f}")
    print(f"  - Order Demand (num_orders) Range  : {train_df['num_orders'].min()} - {train_df['num_orders'].max()} units (Mean: {train_df['num_orders'].mean():.1f} units)")
    print(f"  - Emailer Promotion Transactions   : {train_df['emailer_for_promotion'].sum():,} ({train_df['emailer_for_promotion'].mean()*100:.2f}%)")
    print(f"  - Homepage Featured Transactions   : {train_df['homepage_featured'].sum():,} ({train_df['homepage_featured'].mean()*100:.2f}%)\n")

    print("================================================================================")
    print(" PHASE 1 DATASET INSPECTION COMPLETED SUCCESSFULLY ")
    print("================================================================================")

    return train_df, meal_df, center_df

if __name__ == "__main__":
    inspect_kaggle_dataset()
