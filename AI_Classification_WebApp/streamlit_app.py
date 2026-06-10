import streamlit as st
import pandas as pd
import numpy as np
import pickle
import os

MODEL_PATH = 'models/classification_model.pkl'
DATA_PATH = 'data/dataset.csv'

def load_model(path=MODEL_PATH):
    if not os.path.exists(path):
        return None
    with open(path, 'rb') as f:
        return pickle.load(f)

model = load_model()

st.set_page_config(page_title='Iris Classifier', layout='centered')

# Title adjusted to remove the word 'Streamlit' as requested
st.title('Iris Flower Classifier')

if model is None:
    st.warning('Trained model not found. Run `python train_model.py` to generate the model.')

st.markdown('Enter measurements below to predict the iris species.')

col1, col2 = st.columns(2)

with col1:
    sepal_length = st.number_input('Sepal length (cm)', min_value=0.0, value=5.1, format='%.2f')
    sepal_width = st.number_input('Sepal width (cm)', min_value=0.0, value=3.5, format='%.2f')
with col2:
    petal_length = st.number_input('Petal length (cm)', min_value=0.0, value=1.4, format='%.2f')
    petal_width = st.number_input('Petal width (cm)', min_value=0.0, value=0.2, format='%.2f')

if st.button('Predict'):
    if model is None:
        st.error('Model not loaded')
    else:
        features = np.array([sepal_length, sepal_width, petal_length, petal_width]).reshape(1, -1)
        pred = model.predict(features)[0]
        proba = model.predict_proba(features)[0]
        classes = model.classes_
        st.success(f'Prediction: {pred}')
        st.write('Confidence:', float(np.max(proba)))
        proba_df = pd.DataFrame({'class': classes, 'probability': proba})
        st.table(proba_df)

st.markdown('---')
st.header('Batch prediction (CSV)')
st.write('Upload a CSV with columns: `sepal_length`, `sepal_width`, `petal_length`, `petal_width`.')

uploaded = st.file_uploader('Choose CSV file', type=['csv'])
if uploaded is not None:
    try:
        df = pd.read_csv(uploaded)
        required = ['sepal_length', 'sepal_width', 'petal_length', 'petal_width']
        if not all(c in df.columns for c in required):
            st.error(f'CSV must contain columns: {required}')
        elif model is None:
            st.error('Model not loaded')
        else:
            X = df[required]
            preds = model.predict(X)
            probs = model.predict_proba(X)
            results = df.copy()
            results['predicted_species'] = preds
            for i, cname in enumerate(model.classes_):
                results[f'prob_{cname}'] = probs[:, i]
            results['confidence'] = np.max(probs, axis=1)
            st.success('Batch predictions complete')
            st.download_button('Download results CSV', results.to_csv(index=False), file_name='predictions.csv', mime='text/csv')
    except Exception as e:
        st.error(f'Error processing file: {e}')

st.markdown('---')
st.header('Model & Dataset')
if st.button('Show dataset stats'):
    if os.path.exists(DATA_PATH):
        df = pd.read_csv(DATA_PATH)
        st.write(df.describe())
    else:
        st.warning('Dataset not found')
