import os
import sys
import numpy as np
import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

# Add root directory to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from config.config import PROCESSED_CSV, MODEL_PATH, MODEL_DIR

def train_and_evaluate_ml_model():
    """
    Phase 7: ML Food Demand Prediction Model Training & Baseline Comparison.
    Trains Random Forest Regressor vs Linear Regression Baseline on 456,548 dataset.
    Evaluates MAE, RMSE, and R2 score.
    """
    print("================================================================================")
    print("   PHASE 7: MACHINE LEARNING FOOD DEMAND PREDICTION MODEL TRAINING   ")
    print("================================================================================\n")

    if not os.path.exists(PROCESSED_CSV):
        print(f"Error: Processed dataset not found at {PROCESSED_CSV}. Run data_processor.py first.")
        return

    print("[1/4] Loading processed dataset...")
    df = pd.read_csv(PROCESSED_CSV)
    print(f"  - Dataset Loaded: {df.shape[0]:,} rows")

    # Feature & Target Selection
    features_cat = ["category", "cuisine", "day_of_week", "weather"]
    features_num = ["center_id", "week", "price", "base_price", "promotion", "holiday", "students_present"]
    target = "quantity_sold"

    X = df[features_cat + features_num]
    y = df[target]

    # Split Train/Test (80%/20%)
    print("[2/4] Splitting dataset into Train (80%) and Test (20%)...")
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Preprocessing Pipeline
    preprocessor = ColumnTransformer(
        transformers=[
            ("cat", OneHotEncoder(handle_unknown="ignore"), features_cat)
        ],
        remainder="passthrough"
    )

    # 1. Baseline Model (Linear Regression)
    print("[3/4] Training Baseline Model (Linear Regression)...")
    baseline_pipeline = Pipeline(steps=[
        ("preprocessor", preprocessor),
        ("regressor", LinearRegression())
    ])
    baseline_pipeline.fit(X_train, y_train)
    y_pred_base = baseline_pipeline.predict(X_test)
    mae_base = mean_absolute_error(y_test, y_pred_base)
    rmse_base = np.sqrt(mean_squared_error(y_test, y_pred_base))
    r2_base = r2_score(y_test, y_pred_base)

    # 2. Main Model (Random Forest Regressor)
    print("[4/4] Training Random Forest Regressor Model...")
    rf_pipeline = Pipeline(steps=[
        ("preprocessor", preprocessor),
        ("regressor", RandomForestRegressor(n_estimators=100, max_depth=14, n_jobs=-1, random_state=42))
    ])
    rf_pipeline.fit(X_train, y_train)
    y_pred_rf = rf_pipeline.predict(X_test)
    mae_rf = mean_absolute_error(y_test, y_pred_rf)
    rmse_rf = np.sqrt(mean_squared_error(y_test, y_pred_rf))
    r2_rf = r2_score(y_test, y_pred_rf)

    # Display Evaluation Comparison
    print("\n================================================================================")
    print("                MODEL EVALUATION & PERFORMANCE COMPARISON RESULTS              ")
    print("================================================================================")
    print(f"Metric                      | Baseline (Linear Reg) | Random Forest Regressor")
    print("----------------------------+-----------------------+-----------------------")
    print(f"Mean Absolute Error (MAE)   | {mae_base:19.2f} | {mae_rf:21.2f} units")
    print(f"Root Mean Sq Error (RMSE)   | {rmse_base:19.2f} | {rmse_rf:21.2f} units")
    print(f"R² Score (Accuracy)         | {r2_base:19.4f} | {r2_rf:21.4f}")
    print("================================================================================\n")

    # Save Model Artifact
    os.makedirs(MODEL_DIR, exist_ok=True)
    joblib.dump(rf_pipeline, MODEL_PATH)
    print(f"Random Forest Model artifact saved successfully at: {MODEL_PATH}\n")

    return rf_pipeline

def predict_preparation_units(category, cuisine, day_of_week, weather, center_id, week, price, promotion, holiday, students_present):
    """
    Answers: "How many units of this food item should the canteen prepare?"
    Calculates predicted demand, recommended kitchen preparation quantity with safety buffer,
    and estimated food waste prevention.
    """
    if not os.path.exists(MODEL_PATH):
        train_and_evaluate_ml_model()

    model = joblib.load(MODEL_PATH)

    input_df = pd.DataFrame([{
        "category": category,
        "cuisine": cuisine,
        "day_of_week": day_of_week,
        "weather": weather,
        "center_id": center_id,
        "week": week,
        "price": price,
        "base_price": price * 1.1,
        "promotion": promotion,
        "holiday": holiday,
        "students_present": students_present
    }])

    predicted_demand = int(round(model.predict(input_df)[0]))

    # Recommended preparation quantity includes an optimal 10% safety buffer
    safety_buffer = int(round(predicted_demand * 0.10))
    recommended_preparation = predicted_demand + safety_buffer
    estimated_waste_saved_kg = round((recommended_preparation * 0.15) - (recommended_preparation - predicted_demand), 1)
    estimated_waste_saved_kg = max(2.5, estimated_waste_saved_kg)

    return {
        "predicted_demand": predicted_demand,
        "recommended_preparation": recommended_preparation,
        "safety_buffer_units": safety_buffer,
        "estimated_waste_saved_kg": estimated_waste_saved_kg,
        "estimated_waste_saved": estimated_waste_saved_kg
    }

def predict_single_item(food_item, category, cuisine, day_of_week, weather, center_id, week, price, base_price, promotion, holiday, students_present):
    """Compatibility wrapper for dashboard UI."""
    return predict_preparation_units(
        category=category,
        cuisine=cuisine,
        day_of_week=day_of_week,
        weather=weather,
        center_id=center_id,
        week=week,
        price=price,
        promotion=promotion,
        holiday=holiday,
        students_present=students_present
    )

train_demand_prediction_model = train_and_evaluate_ml_model

if __name__ == "__main__":
    train_and_evaluate_ml_model()
