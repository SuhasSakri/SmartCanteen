# 🚀 SmartCanteen: Cloud Deployment Guide

This guide provides step-by-step instructions to deploy the **SmartCanteen** project for free to cloud production:
- **FastAPI REST Backend API**: Deployed on **Render**
- **React 18 + Vite Web Frontend**: Deployed on **Vercel**

---

## 📋 Prerequisites
1. A **GitHub** account (with your project repository pushed to GitHub).
2. A free **Render** account ([render.com](https://render.com)).
3. A free **Vercel** account ([vercel.com](https://vercel.com)).

---

## 1️⃣ Step 1: Deploy FastAPI Backend to Render

1. Log into your **Render Dashboard** and click **New +** $\rightarrow$ **Web Service**.
2. Connect your GitHub repository (`smartcanteen`).
3. Configure the Web Service settings:
   - **Name**: `smartcanteen-backend`
   - **Region**: Select closest region to your users
   - **Branch**: `main` (or `master`)
   - **Root Directory**: `.` (leave empty or set to root)
   - **Runtime**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn backend.main:app --host 0.0.0.0 --port $PORT`
4. Click **Create Web Service**.
5. Once Render finishes building, copy your live API URL (e.g. `https://smartcanteen-backend.onrender.com`).

---

## 2️⃣ Step 2: Deploy React Frontend to Vercel

1. Log into your **Vercel Dashboard** and click **Add New...** $\rightarrow$ **Project**.
2. Import your GitHub repository (`smartcanteen`).
3. Configure Project Settings:
   - **Framework Preset**: `Vite`
   - **Root Directory**: Select `frontend`
   - **Build Command**: `npm run build`
   - **Output Directory**: `dist`
4. **Environment Variables**:
   - Add a new environment variable:
     - **Key**: `VITE_API_BASE`
     - **Value**: `https://smartcanteen-backend.onrender.com/api` *(replace with your actual Render API URL from Step 1)*
5. Click **Deploy**.

---

## 3️⃣ Step 3: Verify Live Deployment

1. Visit your live Vercel URL (e.g., `https://smartcanteen.vercel.app`).
2. Test the dashboard tabs:
   - **KPI Banners**: Verify live data fetched from FastAPI backend.
   - **Demand Patterns**: Verify line & bar charts render cleanly.
   - **AI Demand Predictor**: Test live ML predictions via the backend API.

---

## 🛠️ Configuration Files Reference

- **[Procfile](file:///c:/Users/HP/OneDrive/Desktop/suhas/smartcanteen/Procfile)**: Start command wrapper for Render / Heroku.
- **[render.yaml](file:///c:/Users/HP/OneDrive/Desktop/suhas/smartcanteen/render.yaml)**: Automatic Render Blueprint deployment file.
- **[vercel.json](file:///c:/Users/HP/OneDrive/Desktop/suhas/smartcanteen/frontend/vercel.json)**: Vite SPA route rewriting rule.
