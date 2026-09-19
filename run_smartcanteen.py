import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.data_processing.inspect_dataset import inspect_kaggle_dataset
from src.data_processing.data_processor import prepare_smartcanteen_dataset
from src.analytics.spark_analytics import run_pyspark_smartcanteen_analytics
from src.analytics.pandas_analytics import run_pandas_smartcanteen_analytics
from src.ml.demand_model import train_and_evaluate_ml_model, predict_preparation_units

def main():
    """
    SmartCanteen Terminal Pipeline Runner (CLI).
    Runs dataset inspection, PySpark analytics, ML training, and food demand predictions.
    """
    print("""
================================================================================
  ____  ____  __  __   _   ____ _____ _____  ____    _    _   _ _____ _____ _____ _   _ 
 / ___||  _ \|  \/  | / \ |  _ \_   _/ ___|  / ___|  / \  | \ | |_   _| ____| ____| \ | |
 \___ \| |_) | |\/| |/ _ \| |_) || || |     | |     / _ \ |  \| | | | |  _| |  _| |  \| |
  ___) |  __/| |  | / ___ \  _ < | || |___  | |___ / ___ \| |\  | | | | |___| |___| |\  |
 |____/|_|   |_|  |_/_/   \_\_| \_\|_|\____|  \____/_/   \_\_| \_| |_| |_____|_____|_| \_|
                                                                                         
           Big Data-Driven Food Demand Analysis and Prediction System
================================================================================
""")

    print("Executing End-to-End SmartCanteen Pipeline on Kaggle Archive Dataset (456,548 Records)...")
    print("--------------------------------------------------------------------------------")

    # Phase 1
    inspect_kaggle_dataset()

    # Phase 2
    prepare_smartcanteen_dataset()

    # Phase 4 & 5
    print("\nExecuting Analytics Engine...")
    success = run_pyspark_smartcanteen_analytics()
    if not success:
        print("Falling back to local Pandas Analytics Engine...")
        run_pandas_smartcanteen_analytics()

    # Phase 7
    train_and_evaluate_ml_model()

    # Phase 8 Sample Prediction Query
    print("\n--- Running Sample Prediction Query ---")
    res = predict_preparation_units(
        category="Main Course",
        cuisine="Indian",
        day_of_week="Monday",
        weather="Sunny",
        center_id=55,
        week=10,
        price=180.0,
        promotion=1,
        holiday=0,
        students_present=2500
    )

    print("\n================================================================================")
    print("                 SMARTCANTEEN FOOD DEMAND FORECAST RESULT                      ")
    print("================================================================================")
    print(f"Target Item            : Main Course (Indian Cuisine)")
    print(f"Canteen Location       : Main Campus Canteen (Center 55)")
    print(f"Predicted Food Demand  : {res['predicted_demand']} units")
    print(f"Recommended Preparation: {res['recommended_preparation']} units (Includes {res['safety_buffer_units']} units safety buffer)")
    print(f"Estimated Waste Saved  : ~{res['estimated_waste_saved_kg']} kg")
    print("================================================================================\n")

if __name__ == "__main__":
    main()
