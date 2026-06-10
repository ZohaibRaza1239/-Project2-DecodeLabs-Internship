"""
Flask Web Application for Iris Flower Classification
Interactive web interface to test the trained classification model
"""

from flask import Flask, render_template, request, jsonify, send_file
import pandas as pd
import numpy as np
import pickle
import os
from io import BytesIO
import json

app = Flask(__name__, template_folder='templates', static_folder='static')

# Configuration
MODEL_PATH = 'models/classification_model.pkl'
DATA_PATH = 'data/dataset.csv'

# Load trained model
def load_model():
    """Load the trained classification model"""
    if not os.path.exists(MODEL_PATH):
        return None
    with open(MODEL_PATH, 'rb') as f:
        return pickle.load(f)

model = load_model()

@app.route('/')
def index():
    """Home page"""
    return render_template('index.html', model_loaded=(model is not None))

@app.route('/api/predict', methods=['POST'])
def predict():
    """API endpoint for making predictions"""
    try:
        data = request.json
        
        # Extract features
        features = [
            float(data['sepal_length']),
            float(data['sepal_width']),
            float(data['petal_length']),
            float(data['petal_width'])
        ]
        
        # Reshape for prediction
        features_array = np.array(features).reshape(1, -1)
        
        # Make prediction
        if model is None:
            return jsonify({'error': 'Model not loaded'}), 400
        
        prediction = model.predict(features_array)[0]
        prediction_proba = model.predict_proba(features_array)[0]
        
        # Get classes
        classes = model.classes_
        probabilities = {classes[i]: float(prediction_proba[i]) for i in range(len(classes))}
        
        return jsonify({
            'success': True,
            'prediction': prediction,
            'probabilities': probabilities,
            'confidence': float(max(prediction_proba))
        })
    except Exception as e:
        return jsonify({'error': str(e), 'success': False}), 400

@app.route('/api/batch-predict', methods=['POST'])
def batch_predict():
    """API endpoint for batch predictions from CSV"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        # Read CSV
        df = pd.read_csv(file)
        
        # Validate columns
        required_cols = ['sepal_length', 'sepal_width', 'petal_length', 'petal_width']
        if not all(col in df.columns for col in required_cols):
            return jsonify({'error': f'CSV must contain columns: {required_cols}'}), 400
        
        # Make predictions
        if model is None:
            return jsonify({'error': 'Model not loaded'}), 400
        
        X = df[required_cols]
        predictions = model.predict(X)
        probabilities = model.predict_proba(X)
        
        # Create results dataframe
        results_df = df.copy()
        results_df['predicted_species'] = predictions
        
        # Add probability columns
        for i, class_name in enumerate(model.classes_):
            results_df[f'prob_{class_name}'] = probabilities[:, i]
        
        results_df['confidence'] = np.max(probabilities, axis=1)
        
        # Save to CSV
        output = BytesIO()
        results_df.to_csv(output, index=False)
        output.seek(0)
        
        return send_file(
            output,
            mimetype='text/csv',
            as_attachment=True,
            download_name='predictions.csv'
        )
    except Exception as e:
        return jsonify({'error': str(e), 'success': False}), 400

@app.route('/api/model-info', methods=['GET'])
def model_info():
    """Get information about the trained model"""
    if model is None:
        return jsonify({'error': 'Model not loaded'}), 400
    
    try:
        # Load dataset to get statistics
        df = pd.read_csv(DATA_PATH)
        
        return jsonify({
            'model_type': 'Decision Tree Classifier',
            'classes': list(model.classes_),
            'features': ['sepal_length', 'sepal_width', 'petal_length', 'petal_width'],
            'dataset_size': len(df),
            'training_samples': int(len(df) * 0.8),
            'testing_samples': int(len(df) * 0.2),
            'feature_count': 4,
            'class_count': len(model.classes_)
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/dataset-stats', methods=['GET'])
def dataset_stats():
    """Get dataset statistics"""
    try:
        df = pd.read_csv(DATA_PATH)
        
        stats = {
            'total_samples': len(df),
            'features': {
                'sepal_length': {'min': float(df['sepal_length'].min()), 'max': float(df['sepal_length'].max()), 'mean': float(df['sepal_length'].mean())},
                'sepal_width': {'min': float(df['sepal_width'].min()), 'max': float(df['sepal_width'].max()), 'mean': float(df['sepal_width'].mean())},
                'petal_length': {'min': float(df['petal_length'].min()), 'max': float(df['petal_length'].max()), 'mean': float(df['petal_length'].mean())},
                'petal_width': {'min': float(df['petal_width'].min()), 'max': float(df['petal_width'].max()), 'mean': float(df['petal_width'].mean())}
            },
            'species_distribution': df['species'].value_counts().to_dict()
        }
        
        return jsonify(stats)
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({'status': 'ok', 'model_loaded': model is not None})

if __name__ == '__main__':
    # Allow overriding host/port/debug via environment variables for local deployment
    host = os.environ.get('FLASK_RUN_HOST', '127.0.0.1')
    port = int(os.environ.get('FLASK_RUN_PORT', os.environ.get('PORT', 5000)))
    debug_env = os.environ.get('FLASK_DEBUG')
    if debug_env is None:
        debug = app.config.get('DEBUG', True)
    else:
        debug = debug_env.lower() in ('1', 'true', 'yes')

    app.run(host=host, port=port, debug=debug)
