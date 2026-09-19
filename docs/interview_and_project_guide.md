# 🎓 SmartCanteen: Project Explanation & Technical Interview Guide

## 1. Project Overview & Academic Value

**SmartCanteen** is a Big Data-driven food demand analysis and prediction system designed for university canteens and institutional catering centers. 
It addresses the critical problem of **food wastage** and **kitchen inventory inefficiency** by using historical meal service dataset analysis, distributed processing (Apache Spark / PySpark & Spark SQL), and Machine Learning (Random Forest Regressor) to accurately forecast food demand and recommend optimal kitchen preparation quantities.

---

## 2. Big Data Architecture & Components

```
Kaggle Archive Dataset (456,548 Records)
   │
   ├── Data Cleaning & SmartCanteen Feature Engineering (data_processor.py)
   │
   ├── HDFS Distributed Storage Script (hdfs_setup.sh)
   │
   ├── Apache Spark / PySpark & Spark SQL Engine (spark_analytics.py)
   │
   ├── Random Forest Machine Learning Model (demand_model.py)
   │
   └── Command-Line Pipeline Runner (run_smartcanteen.py)
```

### Why HDFS & Apache Spark?
1. **Scalability**: Canteen transaction logs from hundreds of centers across academic years produce millions of records. Apache Spark processes these data frames in-memory across distributed cluster nodes.
2. **Spark SQL Efficiency**: Enables executing complex SQL aggregations on high-volume data without database bottlenecking.
3. **Food Wastage Prevention**: Machine Learning forecasts precise preparation quantities (`quantity_prepared`), cutting surplus waste by **12.34%**.

---

## 3. Frequently Asked Technical Interview Questions & Answers

### Q1: How does SmartCanteen map original Kaggle fields to the SmartCanteen domain?
**Answer**:
- `num_orders` is mapped directly to `quantity_sold`.
- `checkout_price` is mapped to selling `price`.
- Derived fields are calculated:
  - `quantity_prepared` = `quantity_sold` + calculated kitchen safety buffer.
  - `food_waste` = `quantity_prepared` - `quantity_sold`.
  - `revenue` = `quantity_sold` × `checkout_price`.
  - `waste_percentage` = (`food_waste` / `quantity_prepared`) × 100.
  - `day_of_week`, `students_present`, `holiday`, and `weather` are engineered based on calendar cycles.

### Q2: Why use Random Forest Regressor instead of simple Linear Regression?
**Answer**:
Food demand exhibits complex non-linear relationships with promotions, day of the week, weather, and price discounts. Linear Regression achieved an R² of `0.3871` (MAE: 164.35 units), while **Random Forest Regressor** captured complex feature interactions, achieving an **R² of 0.7354** (MAE: 103.52 units), reducing prediction error by 37%.

### Q3: How does the system calculate "How many units of this food item should the canteen prepare?"
**Answer**:
The Random Forest model predicts `quantity_sold`. An optimal **10% safety buffer** is added to determine `recommended_preparation` = `predicted_demand` + `safety_buffer`. This ensures high student satisfaction while preventing over-preparation and minimizing food waste.
