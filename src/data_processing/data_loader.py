import os
import pandas as pd
from config.config import TRAIN_CSV, MEAL_INFO_CSV, CENTER_INFO_CSV, PROCESSED_CSV
from src.data_processing.data_generator import generate_smartcanteen_dataset

class SmartCanteenDataLoader:
    """
    Data loading and preprocessing module for SmartCanteen.
    Handles Kaggle dataset ingestion, data cleaning, and domain metric calculations.
    """
    def __init__(self):
        self.raw_train_path = TRAIN_CSV
        self.meal_info_path = MEAL_INFO_CSV
        self.center_info_path = CENTER_INFO_CSV
        self.processed_path = PROCESSED_CSV

    def load_processed_data(self):
        """Loads processed SmartCanteen dataset or generates it if missing."""
        if not os.path.exists(self.processed_path):
            print("Processed dataset not found. Generating fresh dataset...")
            return generate_smartcanteen_dataset()
        return pd.read_csv(self.processed_path)

    def load_raw_kaggle_data(self):
        """Loads original raw Kaggle dataset components."""
        if not os.path.exists(self.raw_train_path):
            generate_smartcanteen_dataset()
        
        train_df = pd.read_csv(self.raw_train_path)
        meal_df = pd.read_csv(self.meal_info_path)
        center_df = pd.read_csv(self.center_info_path)
        return train_df, meal_df, center_df
