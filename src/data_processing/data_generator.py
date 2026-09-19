import os
import sys
import numpy as np
import pandas as pd

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from config.config import (
    RAW_DATA_DIR, PROCESSED_DATA_DIR, TRAIN_CSV, MEAL_INFO_CSV, 
    CENTER_INFO_CSV, PROCESSED_CSV, DISH_MAPPING, CENTER_MAPPING
)

def generate_smartcanteen_dataset(num_weeks=20, seed=42):
    """
    Generates synthetic dataset following Kaggle Food Demand dataset structure
    and computes SmartCanteen derived domain metrics.
    """
    np.random.seed(seed)
    os.makedirs(RAW_DATA_DIR, exist_ok=True)
    os.makedirs(PROCESSED_DATA_DIR, exist_ok=True)

    # 1. Create meal_info.csv
    meal_rows = []
    for m_id, info in DISH_MAPPING.items():
        meal_rows.append({
            "meal_id": m_id,
            "category": info["category"],
            "cuisine": info["cuisine"]
        })
    df_meal_info = pd.DataFrame(meal_rows)
    df_meal_info.to_csv(MEAL_INFO_CSV, index=False)

    # 2. Create fulfilment_center_info.csv
    center_rows = [
        {"center_id": 55, "city_code": 647, "region_code": 56, "center_type": "TYPE_A", "op_area": 3.7},
        {"center_id": 24, "city_code": 590, "region_code": 56, "center_type": "TYPE_B", "op_area": 4.0},
        {"center_id": 11, "city_code": 526, "region_code": 34, "center_type": "TYPE_A", "op_area": 4.5},
        {"center_id": 52, "city_code": 682, "region_code": 56, "center_type": "TYPE_C", "op_area": 2.8},
        {"center_id": 86, "city_code": 699, "region_code": 77, "center_type": "TYPE_C", "op_area": 3.0},
    ]
    df_center_info = pd.DataFrame(center_rows)
    df_center_info.to_csv(CENTER_INFO_CSV, index=False)

    # 3. Generate train.csv (Kaggle Raw Transactions)
    days_map = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    weather_options = ["Sunny", "Rainy", "Cold", "Hot"]

    records = []
    tx_id = 1000000

    for week in range(1, num_weeks + 1):
        for day_idx, day_name in enumerate(days_map):
            is_weekend = 1 if day_name in ["Saturday", "Sunday"] else 0
            is_holiday = 1 if (is_weekend or np.random.rand() < 0.08) else 0

            # Campus attendance varies by day and holiday status
            if is_holiday:
                base_students = np.random.randint(200, 600)
            else:
                base_students = np.random.randint(1800, 3200)

            day_weather = np.random.choice(weather_options, p=[0.5, 0.2, 0.15, 0.15])

            for c_id in CENTER_MAPPING.keys():
                for m_id, dish_info in DISH_MAPPING.items():
                    tx_id += 1
                    base_p = np.random.choice([120, 150, 180, 220, 250, 80, 60, 40])
                    
                    emailer_promo = 1 if np.random.rand() < 0.12 else 0
                    homepage_feat = 1 if np.random.rand() < 0.15 else 0

                    discount = 0.0
                    if emailer_promo or homepage_feat:
                        discount = np.random.uniform(0.1, 0.25)
                    
                    checkout_p = round(base_p * (1 - discount), 2)
                    promo_flag = 1 if (emailer_promo or homepage_feat) else 0

                    # Calculate demand (quantity_sold)
                    demand_mult = 1.3 if promo_flag else 1.0
                    if is_holiday:
                        demand_mult *= 0.4
                    if day_weather == "Rainy":
                        demand_mult *= 1.15 if dish_info["category"] in ["Snacks", "Beverages"] else 0.9

                    base_demand = int((base_students / 40) * (300 / base_p) * demand_mult)
                    quantity_sold = max(10, base_demand + np.random.randint(-15, 20))

                    # Simulation of kitchen prep buffer & food waste
                    prep_buffer_pct = np.random.uniform(0.08, 0.25)
                    quantity_prepared = int(quantity_sold * (1 + prep_buffer_pct))
                    food_waste = quantity_prepared - quantity_sold
                    revenue = round(quantity_sold * checkout_p, 2)
                    waste_pct = round((food_waste / quantity_prepared) * 100, 2)

                    records.append({
                        # Original Kaggle Fields
                        "id": tx_id,
                        "week": week,
                        "center_id": c_id,
                        "meal_id": m_id,
                        "checkout_price": checkout_p,
                        "base_price": base_p,
                        "emailer_for_promotion": emailer_promo,
                        "homepage_featured": homepage_feat,
                        "num_orders": quantity_sold,

                        # SmartCanteen Mapped & Derived Fields
                        "transaction_id": f"TXN-{tx_id}",
                        "day_of_week": day_name,
                        "food_item": dish_info["food_item"],
                        "category": dish_info["category"],
                        "cuisine": dish_info["cuisine"],
                        "price": checkout_p,
                        "promotion": promo_flag,
                        "students_present": base_students,
                        "holiday": is_holiday,
                        "weather": day_weather,
                        "quantity_prepared": quantity_prepared,
                        "quantity_sold": quantity_sold,
                        "food_waste": food_waste,
                        "revenue": revenue,
                        "waste_percentage": waste_pct
                    })

    df_full = pd.DataFrame(records)

    # Save raw Kaggle dataset equivalent
    kaggle_raw_df = df_full[[
        "id", "week", "center_id", "meal_id", "checkout_price", 
        "base_price", "emailer_for_promotion", "homepage_featured", "num_orders"
    ]]
    kaggle_raw_df.to_csv(TRAIN_CSV, index=False)

    # Save full SmartCanteen processed dataset
    df_full.to_csv(PROCESSED_CSV, index=False)
    print(f"Generated Raw Kaggle Dataset: {len(kaggle_raw_df)} rows at {TRAIN_CSV}")
    print(f"Generated Processed SmartCanteen Dataset: {len(df_full)} rows at {PROCESSED_CSV}")
    return df_full

if __name__ == "__main__":
    generate_smartcanteen_dataset()
