"""
AI Classification Model - Training Script
Iris Flower Classification using Supervised Learning
This script loads data, splits it, trains a classification model, and evaluates its performance.
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import pickle
import os

# Configuration
DATA_PATH = 'data/dataset.csv'
MODEL_PATH = 'models/classification_model.pkl'
LABEL_ENCODER_PATH = 'models/label_encoder.pkl'
TEST_SIZE = 0.2
RANDOM_STATE = 42

def load_data(filepath):
    """Load dataset from CSV file"""
    print(f"Loading dataset from {filepath}...")
    df = pd.read_csv(filepath)
    print(f"Dataset shape: {df.shape}")
    print(f"Columns: {df.columns.tolist()}")
    print(f"\nFirst 5 rows:\n{df.head()}")
    return df

def preprocess_data(df):
    """Prepare data: separate features and labels"""
    print("\n" + "="*60)
    print("DATA PREPROCESSING")
    print("="*60)
    
    # Separate features and labels
    X = df.drop('species', axis=1)
    y = df['species']
    
    print(f"Features shape: {X.shape}")
    print(f"Labels shape: {y.shape}")
    print(f"Unique species: {y.unique()}")
    print(f"Species distribution:\n{y.value_counts()}")
    
    return X, y

def split_data(X, y, test_size=0.2):
    """Split data into training and testing sets"""
    print("\n" + "="*60)
    print("DATA SPLITTING")
    print("="*60)
    
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=RANDOM_STATE, stratify=y
    )
    
    print(f"Training set size: {X_train.shape[0]} samples ({(1-test_size)*100:.0f}%)")
    print(f"Testing set size: {X_test.shape[0]} samples ({test_size*100:.0f}%)")
    print(f"\nTraining set distribution:\n{y_train.value_counts()}")
    print(f"\nTesting set distribution:\n{y_test.value_counts()}")
    
    return X_train, X_test, y_train, y_test

def train_model(X_train, y_train):
    """Train classification model using Decision Tree"""
    print("\n" + "="*60)
    print("MODEL TRAINING")
    print("="*60)
    
    print("Training Decision Tree Classifier...")
    model = DecisionTreeClassifier(
        max_depth=5,
        random_state=RANDOM_STATE,
        min_samples_split=5,
        min_samples_leaf=2
    )
    
    model.fit(X_train, y_train)
    print("Model training completed successfully!")
    
    return model

def evaluate_model(model, X_train, y_train, X_test, y_test):
    """Evaluate model performance on training and testing sets"""
    print("\n" + "="*60)
    print("MODEL EVALUATION")
    print("="*60)
    
    # Training accuracy
    y_train_pred = model.predict(X_train)
    train_accuracy = accuracy_score(y_train, y_train_pred)
    print(f"\nTraining Accuracy: {train_accuracy:.4f} ({train_accuracy*100:.2f}%)")
    
    # Testing accuracy
    y_test_pred = model.predict(X_test)
    test_accuracy = accuracy_score(y_test, y_test_pred)
    print(f"Testing Accuracy: {test_accuracy:.4f} ({test_accuracy*100:.2f}%)")
    
    # Detailed classification report
    print(f"\n{'DETAILED CLASSIFICATION REPORT':^60}")
    print("="*60)
    print(classification_report(y_test, y_test_pred))
    
    # Confusion matrix
    print("Confusion Matrix:")
    cm = confusion_matrix(y_test, y_test_pred)
    print(cm)
    
    return y_train_pred, y_test_pred, train_accuracy, test_accuracy

def save_model(model, model_path):
    """Save trained model to disk"""
    os.makedirs(os.path.dirname(model_path), exist_ok=True)
    with open(model_path, 'wb') as f:
        pickle.dump(model, f)
    print(f"\nModel saved to {model_path}")

def test_with_new_data(model, X_test, y_test):
    """Test model with new/unseen data"""
    print("\n" + "="*60)
    print("TESTING WITH NEW DATA")
    print("="*60)
    
    print("\nMaking predictions on unseen test data...")
    predictions = model.predict(X_test)
    
    # Display first 10 predictions
    print("\nFirst 10 predictions on new data:")
    print(f"{'Index':<6} {'Actual':<15} {'Predicted':<15} {'Correct':<8}")
    print("-"*50)
    for i in range(min(10, len(predictions))):
        actual = y_test.iloc[i]
        predicted = predictions[i]
        correct = "✓" if actual == predicted else "✗"
        print(f"{i:<6} {actual:<15} {predicted:<15} {correct:<8}")
    
    return predictions

def main():
    """Main training pipeline"""
    print("\n" + "="*60)
    print("AI CLASSIFICATION MODEL - TRAINING PIPELINE")
    print("="*60)
    
    # Load data
    df = load_data(DATA_PATH)
    
    # Preprocess data
    X, y = preprocess_data(df)
    
    # Split data
    X_train, X_test, y_train, y_test = split_data(X, y, test_size=TEST_SIZE)
    
    # Train model
    model = train_model(X_train, y_train)
    
    # Evaluate model
    y_train_pred, y_test_pred, train_acc, test_acc = evaluate_model(
        model, X_train, y_train, X_test, y_test
    )
    
    # Test with new data
    test_with_new_data(model, X_test, y_test)
    
    # Save model
    save_model(model, MODEL_PATH)
    
    print("\n" + "="*60)
    print("TRAINING COMPLETE")
    print("="*60)
    print(f"✓ Model trained and saved")
    print(f"✓ Training Accuracy: {train_acc*100:.2f}%")
    print(f"✓ Testing Accuracy: {test_acc*100:.2f}%")
    print("="*60 + "\n")

if __name__ == "__main__":
    main()
