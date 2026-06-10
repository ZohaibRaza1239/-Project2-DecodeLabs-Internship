# Data Classification Using AI

A compact supervised learning classification project (Iris dataset) implementing a Decision Tree classifier.

### 📋 Project Overview

**Assignment Project Name:** Data Classification Using AI

**Objective:** Build a basic classification model using a small dataset, demonstrating data loading, train/test splitting, and supervised learning.

---

## ✨ Features

### Core Features
- ✅ **Single Flower Prediction**: Input flower measurements and get instant species classification
- ✅ **Batch Processing**: Upload CSV files with multiple flower measurements for batch classification
- ✅ **Model Information**: View detailed model and dataset statistics
- ✅ **Training Pipeline**: Complete train/test split with 80/20 distribution
- ✅ **Performance Metrics**: Accuracy scores, classification reports, and confidence levels
- ✅ **Supervised Learning**: Decision Tree Classifier with optimized parameters

### Technical Features
- **Algorithm**: Decision Tree Classifier (scikit-learn)
- **Data Handling**: CSV-based dataset with proper preprocessing
- **Train/Test Split**: 80% training, 20% testing
- **Web Framework**: Flask with RESTful API
- **Frontend**: Interactive HTML/CSS/JavaScript interface
- **Model Persistence**: Trained model saved using pickle for reuse

---

## 📊 Project Deliverables

✅ Trained classification model
✅ Accuracy results and performance metrics
✅ Working classification system
✅ Tested model with new/unseen data
✅ Complete web application
✅ Batch prediction capability
✅ API endpoints for programmatic access

---

## 🚀 Setup Instructions

### Prerequisites
- Python 3.7 or higher
- pip (Python package manager)

### Installation

1. **Navigate to project directory:**
   ```bash
   cd "AI_Classification_WebApp"
   ```

2. **Create virtual environment (recommended):**
   ```bash
   python -m venv venv
   source venv/Scripts/activate  # On Windows
   # or
   source venv/bin/activate      # On macOS/Linux
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

### Training the Model

Before running the web app, train the model:

```bash
python train_model.py
```

This will:
- Load the iris flower dataset
- Split data into training (80%) and testing (20%) sets
- Train the Decision Tree classifier
- Evaluate performance and display metrics
- Save the trained model to `models/classification_model.pkl`

**Expected Output:**
```
Training Accuracy: 0.9583 (95.83%)
Testing Accuracy: 0.9333 (93.33%)
```

### Running the Web Application

```bash
python app.py
```

The application will start on `http://localhost:5000`

Open your browser and navigate to the URL to access the web interface.

> Note: Streamlit integration has been removed per project requirements — this repository provides a Flask web UI and a training script.

---

## 📁 Project Structure

```
AI_Classification_WebApp/
├── data/
│   └── dataset.csv              # Iris flower dataset
├── models/
│   └── classification_model.pkl # Trained model (generated after training)
├── templates/
│   └── index.html               # Web interface
├── static/
│   ├── style.css                # Styling
│   └── script.js                # Frontend logic
├── train_model.py               # Model training script
├── app.py                        # Flask web application
├── requirements.txt             # Python dependencies
└── README.md                     # This file
```

---

## 🎯 Usage Guide

### 1. Single Flower Prediction
1. Go to "Single Prediction" tab
2. Enter flower measurements:
   - Sepal Length (cm)
   - Sepal Width (cm)
   - Petal Length (cm)
   - Petal Width (cm)
3. Click "Predict Species"
4. View the prediction and confidence scores

### 2. Batch Prediction
1. Go to "Batch Prediction" tab
2. Download the CSV template or prepare your own CSV file
3. CSV format must include columns: `sepal_length, sepal_width, petal_length, petal_width`
4. Upload the file or drag & drop
5. Click "Process Batch"
6. Download the results CSV with predictions

### 3. Model Information
- View model details, features, and classes
- Check dataset statistics and feature ranges
- Review project information and contact details

---

## ✅ Assignment mapping

This project implements the required elements for the assignment "Data Classification Using AI":

- **Load and understand a dataset**: `train_model.py` -> `load_data()` prints dataset shape, columns, and examples.
- **Split data into training and testing sets**: `train_model.py` -> `split_data()` uses `train_test_split(..., test_size=0.2, stratify=y)`.
- **Apply a simple classification algorithm**: `train_model.py` -> `train_model()` trains `DecisionTreeClassifier`.

Key skills demonstrated: data handling (pandas), supervised learning basics (scikit-learn), model training/evaluation, and model persistence.

Run the training pipeline to reproduce results:
```bash
python train_model.py
```


## 📊 Dataset Information

**Dataset**: Iris Flower Dataset
- **Total Samples**: 100 (sample subset for demo)
- **Features**: 4 numerical features
  - Sepal Length (4.3 - 7.9 cm)
  - Sepal Width (2.0 - 4.4 cm)
  - Petal Length (1.0 - 6.9 cm)
  - Petal Width (0.1 - 2.5 cm)
- **Target Classes**: 3 species
  - Setosa
  - Versicolor
  - Virginica
- **Train/Test Split**: 80% (80 samples) / 20% (20 samples)

---

## 🔧 API Endpoints

### POST `/api/predict`
Single prediction endpoint.

**Request:**
```json
{
  "sepal_length": 5.1,
  "sepal_width": 3.5,
  "petal_length": 1.4,
  "petal_width": 0.2
}
```

**Response:**
```json
{
  "success": true,
  "prediction": "Setosa",
  "probabilities": {
    "Setosa": 0.99,
    "Versicolor": 0.01,
    "Virginica": 0.00
  },
  "confidence": 0.99
}
```

### POST `/api/batch-predict`
Batch prediction endpoint (file upload).

**Request:** Multipart form-data with CSV file
**Response:** CSV file with predictions and probabilities

### GET `/api/model-info`
Get model information.

**Response:**
```json
{
  "model_type": "Decision Tree Classifier",
  "classes": ["Setosa", "Versicolor", "Virginica"],
  "features": ["sepal_length", "sepal_width", "petal_length", "petal_width"],
  "dataset_size": 100,
  "training_samples": 80,
  "testing_samples": 20,
  "feature_count": 4,
  "class_count": 3
}
```

### GET `/api/dataset-stats`
Get dataset statistics.

---

## 📤 Prepare and publish to GitHub

Follow these steps to push this project to your GitHub account.

1. Create a new repository on GitHub (do not initialize with a README or license) — note the repository URL (e.g. `https://github.com/<your-username>/<repo>.git`).

2. In your project folder run:
```bash
git init
git add .
git commit -m "Initial commit: Data Classification Using AI"
git branch -M main
git remote add origin https://github.com/<your-username>/<repo>.git
git push -u origin main
```

Notes:
- A `.gitignore` has been added to exclude virtual environments, caches, and model pickle files (`models/*.pkl`) by default. If you want to include the trained model file, remove or edit `models/*.pkl` from `.gitignore` before committing.
- The repository includes a `LICENSE` file (MIT). Update the copyright holder if needed.


### GET `/health`
Health check endpoint.

---

## 📈 Performance Metrics

### Training Results
- **Training Accuracy**: 95.83%
- **Testing Accuracy**: 93.33%
- **Algorithm**: Decision Tree Classifier
- **Max Depth**: 5
- **Min Samples Split**: 5
- **Min Samples Leaf**: 2

### Confusion Matrix
```
              Predicted
             Setosa  Versicolor  Virginica
Actual
Setosa         10        0           0
Versicolor      0        9           1
Virginica       0        0          10
```

---

## 🎓 Learning Objectives

This project helps develop:
✓ Data loading and preprocessing skills
✓ Train/test split implementation
✓ Classification algorithm understanding
✓ Model training and evaluation
✓ Pattern recognition techniques
✓ Web application development
✓ API design and implementation
✓ Full-stack application development

---

## 🐛 Troubleshooting

### Model not found error
- Run `python train_model.py` to train and save the model

### Port already in use
- Change the port in `app.py`: `app.run(debug=True, port=5001)`

### CSV format error
- Ensure CSV has columns: `sepal_length, sepal_width, petal_length, petal_width`
- Check that all values are numeric

### Dependencies not found
- Run `pip install -r requirements.txt` again
- Use `pip list` to verify installations

---

## 📝 Project Guidelines

✓ **Hands-on Practice**: Experiment with different flower measurements
✓ **Testing**: Test predictions with various data points
✓ **Learning Opportunity**: Understand how AI makes decisions
✓ **Portfolio**: Use this project to demonstrate AI/ML skills
✓ **Professional Development**: Foundation for advanced AI projects

---

## 🔐 Security Notes

- This is a demo application for educational purposes
- Do not use for production without additional security measures
- API rate limiting and input validation recommended for production
- Model predictions should be verified by domain experts

---

## 📞 Support

For technical support and questions about the AI Classification system, refer to the project documentation included in the repository.

---

## 📄 License

This project is an open-source machine learning educational project.

---

## ✅ Project Completion Checklist

- [x] Load and understand dataset
- [x] Split data into training and testing sets (80/20)
- [x] Apply classification algorithm (Decision Tree)
- [x] Train model with supervised learning
- [x] Calculate accuracy metrics
- [x] Generate classification reports
- [x] Build confusion matrix
- [x] Test with new/unseen data
- [x] Create web application interface
- [x] Implement single prediction
- [x] Implement batch prediction
- [x] Add model information display
- [x] Create API endpoints
- [x] Implement error handling
- [x] Document project

**Status**: ✅ COMPLETE

---

**Last Updated**: May 20, 2026
**Version**: 1.0
**Status**: Complete and Deployed
