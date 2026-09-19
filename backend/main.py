import os
import sys
import numpy as np
import pandas as pd
from typing import Optional
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# Add project root to sys.path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

from config.config import PROCESSED_CSV
from src.data_processing.data_processor import prepare_smartcanteen_dataset
from src.ml.demand_model import predict_preparation_units, train_and_evaluate_ml_model, MODEL_PATH

app = FastAPI(
    title="SmartCanteen Big Data & ML Backend API",
    description="FastAPI Backend for SmartCanteen Food Demand & Wastage Analytics",
    version="2.0.0"
)

# Enable CORS for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load dataset into memory
df_cache = None

def get_dataset():
    global df_cache
    if df_cache is None:
        if not os.path.exists(PROCESSED_CSV):
            df_cache = prepare_smartcanteen_dataset()
        else:
            df_cache = pd.read_csv(PROCESSED_CSV)
    return df_cache

def apply_filters(
    df: pd.DataFrame,
    center_id: Optional[str] = None,
    category: Optional[str] = None,
    cuisine: Optional[str] = None,
    min_week: Optional[int] = None,
    max_week: Optional[int] = None
):
    filtered = df.copy()
    if min_week is not None and max_week is not None:
        filtered = filtered[(filtered["week"] >= min_week) & (filtered["week"] <= max_week)]
    if center_id and center_id != "all":
        try:
            cid = int(center_id)
            filtered = filtered[filtered["center_id"] == cid]
        except ValueError:
            pass
    if category and category != "all":
        filtered = filtered[filtered["category"] == category]
    if cuisine and cuisine != "all":
        filtered = filtered[filtered["cuisine"] == cuisine]
    return filtered

@app.get("/api/options")
def get_filter_options():
    df = get_dataset()
    centers = sorted([int(c) for c in df["center_id"].unique()])
    categories = sorted(list(df["category"].unique()))
    cuisines = sorted(list(df["cuisine"].unique()))
    min_w = int(df["week"].min())
    max_w = int(df["week"].max())
    
    return {
        "centers": centers,
        "categories": categories,
        "cuisines": cuisines,
        "min_week": min_w,
        "max_week": max_w
    }

@app.get("/api/kpis")
def get_kpis(
    center_id: str = "all",
    category: str = "all",
    cuisine: str = "all",
    min_week: int = 1,
    max_week: int = 145
):
    df = get_dataset()
    f_df = apply_filters(df, center_id, category, cuisine, min_week, max_week)

    total_orders = int(f_df["quantity_sold"].sum())
    total_revenue = float(f_df["revenue"].sum())
    total_waste = int(f_df["food_waste"].sum())
    avg_waste_pct = float(f_df["waste_percentage"].mean()) if len(f_df) > 0 else 0.0
    avg_daily_demand = int(round(f_df.groupby("week")["quantity_sold"].sum().mean() / 7)) if len(f_df) > 0 else 0

    return {
        "total_orders": total_orders,
        "total_revenue": round(total_revenue, 2),
        "total_waste": total_waste,
        "total_waste_kg": int(total_waste * 0.35),
        "avg_waste_pct": round(avg_waste_pct, 1),
        "avg_daily_demand": avg_daily_demand
    }

@app.get("/api/demand-patterns")
def get_demand_patterns(
    center_id: str = "all",
    category: str = "all",
    cuisine: str = "all",
    min_week: int = 1,
    max_week: int = 145
):
    df = get_dataset()
    f_df = apply_filters(df, center_id, category, cuisine, min_week, max_week)

    # 1. Weekly Demand Trend
    weekly = f_df.groupby("week")["quantity_sold"].sum().reset_index()
    weekly_trend = weekly.to_dict(orient="records")

    # 2. Top 10 Popular Dishes
    top_dishes = f_df.groupby("food_item")["quantity_sold"].sum().reset_index()
    top_dishes = top_dishes.sort_values(by="quantity_sold", ascending=False).head(10).to_dict(orient="records")

    # 3. Day of Week Demand
    day_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    day_df = f_df.groupby("day_of_week")["quantity_sold"].sum().reindex(day_order).fillna(0).reset_index()
    day_demand = day_df.to_dict(orient="records")

    # 4. Category Breakdown
    cat_df = f_df.groupby("category")["quantity_sold"].sum().reset_index()
    cat_breakdown = cat_df.to_dict(orient="records")

    return {
        "weekly_trend": weekly_trend,
        "top_dishes": top_dishes,
        "day_demand": day_demand,
        "category_breakdown": cat_breakdown
    }

@app.get("/api/revenue-insights")
def get_revenue_insights(
    center_id: str = "all",
    category: str = "all",
    cuisine: str = "all",
    min_week: int = 1,
    max_week: int = 145
):
    df = get_dataset()
    f_df = apply_filters(df, center_id, category, cuisine, min_week, max_week)

    # 1. Category Revenue
    cat_rev = f_df.groupby("category")["revenue"].sum().reset_index().sort_values(by="revenue", ascending=False).to_dict(orient="records")

    # 2. Promotion Impact on Top 8 Dishes
    top_8 = f_df.groupby("food_item")["quantity_sold"].sum().nlargest(8).index
    promo_df = f_df[f_df["food_item"].isin(top_8)].groupby(["food_item", "promotion"])["quantity_sold"].mean().reset_index()
    
    # Pivot promo_df for clean frontend rendering
    pivoted_promo = []
    for dish in top_8:
        sub = promo_df[promo_df["food_item"] == dish]
        reg_val = float(sub[sub["promotion"] == 0]["quantity_sold"].values[0]) if len(sub[sub["promotion"] == 0]) > 0 else 0
        promo_val = float(sub[sub["promotion"] == 1]["quantity_sold"].values[0]) if len(sub[sub["promotion"] == 1]) > 0 else 0
        pivoted_promo.append({
            "food_item": dish,
            "regular_demand": round(reg_val, 1),
            "promo_demand": round(promo_val, 1)
        })

    # 3. Center Revenue Leaderboard
    center_rev = f_df.groupby("center_id")["revenue"].sum().reset_index().sort_values(by="revenue", ascending=False).head(10)
    center_rev["center_name"] = "Center #" + center_rev["center_id"].astype(str)
    center_leaderboard = center_rev.to_dict(orient="records")

    return {
        "category_revenue": cat_rev,
        "promotion_impact": pivoted_promo,
        "center_leaderboard": center_leaderboard
    }

@app.get("/api/food-wastage")
def get_food_wastage(
    center_id: str = "all",
    category: str = "all",
    cuisine: str = "all",
    min_week: int = 1,
    max_week: int = 145
):
    df = get_dataset()
    f_df = apply_filters(df, center_id, category, cuisine, min_week, max_week)

    # 1. Weekly Waste Timeline
    waste_weekly = f_df.groupby("week")[["quantity_prepared", "quantity_sold", "food_waste"]].sum().reset_index()
    weekly_waste = waste_weekly.to_dict(orient="records")

    # 2. Top 10 Canteen Waste Percentage
    waste_center = f_df.groupby("center_id")["waste_percentage"].mean().reset_index().sort_values(by="waste_percentage", ascending=False).head(10)
    waste_center["center_name"] = "Center #" + waste_center["center_id"].astype(str)
    center_waste = waste_center.to_dict(orient="records")

    return {
        "weekly_waste": weekly_waste,
        "center_waste": center_waste
    }

class PredictRequest(BaseModel):
    category: str
    cuisine: str
    day_of_week: str
    weather: str
    center_id: int
    price: float
    promotion: int
    holiday: int
    students_present: int

@app.post("/api/predict")
def predict_demand(req: PredictRequest):
    if not os.path.exists(MODEL_PATH):
        train_and_evaluate_ml_model()

    res = predict_preparation_units(
        category=req.category,
        cuisine=req.cuisine,
        day_of_week=req.day_of_week,
        weather=req.weather,
        center_id=req.center_id,
        week=10,
        price=req.price,
        promotion=req.promotion,
        holiday=req.holiday,
        students_present=req.students_present
    )

    return res

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
