# 🍱 SmartCanteen: Big Data-Driven Food Demand Analysis & Prediction

**SmartCanteen** is an enterprise-grade Big Data & Artificial Intelligence solution engineered for university canteens, corporate dining halls, and large-scale meal service centers. 

The system leverages **Apache Hadoop HDFS**, **Apache Spark / PySpark**, **Spark SQL**, **Random Forest Machine Learning**, a **FastAPI REST Service**, and a modern **React 18 + TypeScript Web Dashboard** to analyze demand patterns, optimize kitchen preparation quantities, and minimize food wastage.

---

## 📌 Technical Architecture

```
                                ┌─────────────────────────┐
                                │   Kaggle Dataset        │
                                │ (train, meal_info, etc) │
                                └────────────┬────────────┘
                                             │ Ingestion & Cleaning
                                             ▼
                                ┌─────────────────────────┐
                                │   Apache Hadoop HDFS    │
                                │  (/smartcanteen/data)   │
                                └────────────┬────────────┘
                                             │ PySpark DataFrames
                                             ▼
                                ┌─────────────────────────┐
                                │  Apache Spark Engine    │
                                │  (Transform & Metrics)  │
                                └────────────┬────────────┘
                                             │ Spark SQL & Analytics
                                             ▼
                                ┌─────────────────────────┐
                                │ Random Forest Regressor │
                                │ (Food Demand Predictor) │
                                └────────────┬────────────┘
                                             │ ML Inference API
                                             ▼
                                ┌─────────────────────────┐
                                │ FastAPI REST Backend API│
                                │ (Python / Uvicorn :8000)│
                                └────────────┬────────────┘
                                             │ REST JSON API
                                             ▼
                                ┌─────────────────────────┐
                                │ React 18 + Vite Web App │
                                │(TypeScript/Recharts :5173│
                                └─────────────────────────┘
```

---

## ✨ Features & Technology Stack

| Domain | Technology | Key Capabilities |
| :--- | :--- | :--- |
| **Big Data Storage** | Apache Hadoop HDFS | Distributed directory partitioning (`/smartcanteen/data/raw`, `/smartcanteen/data/processed`) & script automation via [hdfs_setup.sh](file:///c:/Users/HP/OneDrive/Desktop/suhas/smartcanteen/hdfs/scripts/hdfs_setup.sh). |
| **Data Processing** | Apache Spark / PySpark 3.4+ & Spark SQL | High-throughput distributed data frame transformations, metric aggregations, and custom SQL analytics queries. |
| **Machine Learning** | Scikit-Learn (Random Forest Regressor) | Forecasts food demand based on price, promotion, weather, day of week, and attendance footfall ($R^2 = 0.7354$). |
| **Backend REST API** | FastAPI + Uvicorn | Asynchronous RESTful JSON endpoints delivering filtered KPI metrics, analytics data, and live ML inference. |
| **Modern Web UI** | React 18, TypeScript, Vite, Recharts, Lucide Icons | Premium glassmorphism dark theme dashboard featuring full X-axis label integrity (`interval={0}`), dynamic filters, and real-time buffer calculators. |

---

## 🗂️ Dataset & Domain Schema Mapping

Raw Kaggle Food Demand records are cleaned and mapped into operational canteen domain entities:

| Kaggle Original Field | SmartCanteen Mapped Field | Description & Business Logic |
| :--- | :--- | :--- |
| `id` | `transaction_id` | Unique transaction reference ID (`TXN-xxxx`) |
| `week` | `week` & `day_of_week` | Academic calendar week index and mapped day name |
| `center_id` | `center_id` | Unique canteen / dining facility location ID |
| `meal_id` | `meal_id` & `food_item` | Dish designation (e.g., Masala Dosa, Veg Biryani) |
| `category` | `category` | Food course (Main Course, Snacks, Starters, Desserts, Beverages) |
| `cuisine` | `cuisine` | Regional style (Indian, Chinese, Italian, Continental) |
| `checkout_price` | `price` | Final discounted selling price |
| `base_price` | `base_price` | Standard list price |
| `emailer_for_promotion` / `homepage_featured` | `promotion` | Active marketing campaign flag (0/1) |
| **[Derived]** | `students_present` | Campus footfall / student attendance estimate |
| **[Derived]** | `holiday` | Weekend / Academic holiday indicator (0/1) |
| **[Derived]** | `weather` | Weather condition simulation (Sunny, Rainy, Cold, Hot) |
| **[Derived]** | `quantity_sold` | Customer order volume (from Kaggle `num_orders`) |
| **[Derived]** | `quantity_prepared` | Kitchen units prepared (`quantity_sold` + safety buffer) |
| **[Derived]** | `food_waste` | Surplus unconsumed food units (`quantity_prepared` - `quantity_sold`) |
| **[Derived]** | `revenue` | Total financial revenue (`quantity_sold` × `price`) |
| **[Derived]** | `waste_percentage` | (`food_waste` / `quantity_prepared`) × 100 |

---

## 📂 Project Directory Structure

```
smartcanteen/
├── backend/                  # FastAPI REST API implementation
│   └── main.py              # REST API endpoints & CORS middleware
├── frontend/                 # Modern React 18 + Vite + TypeScript web application
│   ├── src/
│   │   ├── App.tsx          # Main Glassmorphism Dashboard & Recharts components
│   │   ├── App.css          # Styling & Animations
│   │   └── main.tsx         # React DOM entry point
│   ├── package.json         # Node dependencies & Vite scripts
│   └── vite.config.ts       # Vite configuration
├── hdfs/                     # Hadoop HDFS configurations & ingestion scripts
│   └── scripts/
│       └── hdfs_setup.sh    # HDFS directory setup & data upload script
├── src/                      # Core Python source code
│   ├── analytics/           # PySpark & Pandas analytics engines
│   │   ├── spark_analytics.py
│   │   └── pandas_analytics.py
│   ├── data_processing/     # Ingestion, cleaning, and domain feature engineering
│   │   ├── data_processor.py
│   │   └── inspect_dataset.py
│   └── ml/                  # Machine Learning pipeline
│       └── demand_model.py  # Random Forest Regressor training & inference
├── sql/                      # Spark SQL analytics queries
│   └── analytics_queries.sql
├── docs/                     # Technical documentation & interview guide
│   └── interview_and_project_guide.md
├── run_smartcanteen.py       # End-to-end CLI pipeline runner
├── requirements.txt          # Python dependencies
└── README.md                 # Project README
```

---

## ⚙️ Installation & Running Instructions

### 1. Prerequisites
- Python 3.9+ installed
- Node.js 18+ (for React Frontend)
- Apache Spark / PySpark 3.4+
- Hadoop HDFS (Optional; required only for cluster deployment)

### 2. Install Python Dependencies
```bash
py -3 -m pip install -r requirements.txt
```

### 3. Start React UI + FastAPI REST Backend

**Step 1: Start FastAPI REST Backend (Port 8000)**
```bash
py -3 -m uvicorn backend.main:app --reload --port 8000
```

**Step 2: Start React Web App (Port 5173)**
```bash
cd frontend
npm install
npm run dev
```
Open **`http://localhost:5173`** in your browser.

---

### 4. Run Terminal Pipeline (CLI Engine)
Execute data processing, PySpark analytics, ML model training, and sample demand prediction queries directly in terminal:
```bash
py -3 run_smartcanteen.py
```

---

### 5. Setup Hadoop HDFS Storage (Optional Cluster Setup)
```bash
bash hdfs/scripts/hdfs_setup.sh
```

---

## 🌐 Free Cloud Deployment (Render + Vercel)

For step-by-step instructions to deploy the FastAPI backend on **Render** and the React frontend on **Vercel**, refer to the detailed [Cloud Deployment Guide](file:///c:/Users/HP/OneDrive/Desktop/suhas/smartcanteen/docs/cloud_deployment_guide.md).


---

## 📊 Dashboard Capabilities & Highlights

1. **Real-time KPI Header Banner**: Displays aggregated metrics for Total Orders, Revenue (₹), Waste Volume (Units & Kg), Average Waste %, and Daily Demand.
2. **Demand Analytics Tab**: Complete Day-of-Week demand breakdown (with guaranteed tick display for all days including Wednesday), Top 10 Popular Dishes, and Weekly trend lines.
3. **Revenue & Pricing Tab**: Revenue by food category, promotional discount impact, and canteen center revenue leaderboard.
4. **Food Wastage Analytics Tab**: Timeline comparing Food Preparation vs Demand vs Surplus Waste, and canteen center waste percentage rankings.
5. **AI Kitchen Preparation Predictor**: Interactive ML forecasting widget calculating **Predicted Food Demand**, **Recommended Kitchen Preparation Quantity** (with safety buffer), and **Estimated Waste Reduction**.
