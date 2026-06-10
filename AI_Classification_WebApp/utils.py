"""
Utility functions for AI Classification WebApp
"""

import os
import pickle
import pandas as pd
from config import Config

def ensure_directories():
    """Create necessary directories if they don't exist"""
    for directory in [Config.DATA_DIR, Config.MODELS_DIR]:
        os.makedirs(directory, exist_ok=True)

def save_model(model):
    """Save trained model to disk"""
    ensure_directories()
    with open(Config.MODEL_PATH, 'wb') as f:
        pickle.dump(model, f)

def load_model():
    """Load trained model from disk"""
    if os.path.exists(Config.MODEL_PATH):
        with open(Config.MODEL_PATH, 'rb') as f:
            return pickle.load(f)
    return None

def load_dataset(filepath=None):
    """Load dataset from CSV"""
    if filepath is None:
        filepath = Config.DATA_PATH
    if os.path.exists(filepath):
        return pd.read_csv(filepath)
    return None

def validate_features(data):
    """Validate that data contains required features"""
    required_features = ['sepal_length', 'sepal_width', 'petal_length', 'petal_width']
    return all(feature in data.columns for feature in required_features)
