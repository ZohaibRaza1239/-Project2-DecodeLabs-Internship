"""
Configuration file for AI Classification WebApp
"""

import os

# Base configuration
class Config:
    # Flask
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    DEBUG = True
    TESTING = False
    
    # Paths
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    DATA_DIR = os.path.join(BASE_DIR, 'data')
    MODELS_DIR = os.path.join(BASE_DIR, 'models')
    
    # Model
    MODEL_PATH = os.path.join(MODELS_DIR, 'classification_model.pkl')
    DATA_PATH = os.path.join(DATA_DIR, 'dataset.csv')
    
    # Training
    TEST_SIZE = 0.2
    RANDOM_STATE = 42
    MAX_DEPTH = 5
    MIN_SAMPLES_SPLIT = 5
    MIN_SAMPLES_LEAF = 2
    
    # Flask
    JSON_SORT_KEYS = False
    JSONIFY_PRETTYPRINT_REGULAR = True

# Production configuration
class ProductionConfig(Config):
    DEBUG = False
    TESTING = False

# Development configuration
class DevelopmentConfig(Config):
    DEBUG = True
    TESTING = False

# Testing configuration
class TestingConfig(Config):
    DEBUG = True
    TESTING = True

# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
