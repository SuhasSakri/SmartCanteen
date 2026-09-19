#!/bin/bash
# SmartCanteen HDFS Data Ingestion Script

echo "=========================================="
echo "  SmartCanteen HDFS Storage Setup Script  "
echo "=========================================="

# 1. Create HDFS directory structure
echo "[1/3] Creating HDFS directories..."
hdfs dfs -mkdir -p /smartcanteen/data/raw
hdfs dfs -mkdir -p /smartcanteen/data/processed
hdfs dfs -mkdir -p /smartcanteen/models

# 2. Upload Kaggle raw datasets to HDFS
echo "[2/3] Uploading Kaggle raw dataset to HDFS..."
hdfs dfs -put -f ./data/raw/train.csv /smartcanteen/data/raw/
hdfs dfs -put -f ./data/raw/meal_info.csv /smartcanteen/data/raw/
hdfs dfs -put -f ./data/raw/fulfilment_center_info.csv /smartcanteen/data/raw/

# 3. Upload processed SmartCanteen dataset to HDFS
echo "[3/3] Uploading processed dataset to HDFS..."
hdfs dfs -put -f ./data/processed/smartcanteen_processed.csv /smartcanteen/data/processed/

echo "=========================================="
echo " HDFS Data Setup Complete! "
echo " Verify with: hdfs dfs -ls /smartcanteen/data/processed/"
echo "=========================================="
