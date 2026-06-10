/**
 * AI Classification WebApp - Frontend Script
 * Handles tab navigation, form submissions, and API calls
 */

// Tab Navigation
document.querySelectorAll('.tab-btn').forEach(btn => {
    btn.addEventListener('click', () => {
        const tabName = btn.dataset.tab;
        
        // Remove active class from all buttons and contents
        document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
        document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));
        
        // Add active class to clicked button and corresponding content
        btn.classList.add('active');
        document.getElementById(tabName).classList.add('active');
        
        // Load data for info tab
        if (tabName === 'info') {
            loadModelInfo();
            loadDatasetStats();
        }
    });
});

// ============================================
// TAB 1: Single Prediction
// ============================================

const form = document.getElementById('singlePredictionForm');
const resultsDiv = document.getElementById('singleResults');
const errorDiv = document.getElementById('singleError');

form.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const data = {
        sepal_length: document.getElementById('sepal_length').value,
        sepal_width: document.getElementById('sepal_width').value,
        petal_length: document.getElementById('petal_length').value,
        petal_width: document.getElementById('petal_width').value
    };
    
    try {
        errorDiv.classList.add('hidden');
        resultsDiv.classList.add('hidden');
        
        const response = await fetch('/api/predict', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });
        
        if (!response.ok) {
            throw new Error('Prediction failed');
        }
        
        const result = response.json();
        result.then(res => {
            if (res.success) {
                displayPredictionResult(res);
                resultsDiv.classList.remove('hidden');
            } else {
                showError(res.error, 'singleError');
            }
        });
    } catch (error) {
        showError(error.message, 'singleError');
    }
});

function displayPredictionResult(result) {
    document.getElementById('predictedSpecies').textContent = result.prediction;
    
    const probabilitiesContainer = document.getElementById('probabilitiesContainer');
    probabilitiesContainer.innerHTML = '';
    
    Object.entries(result.probabilities).forEach(([species, prob]) => {
        const percentage = (prob * 100).toFixed(2);
        const item = document.createElement('div');
        item.className = 'probability-item';
        item.innerHTML = `
            <span class="probability-label">${species}</span>
            <div class="probability-bar">
                <div class="probability-fill" style="width: ${percentage}%"></div>
            </div>
            <span class="probability-value">${percentage}%</span>
        `;
        probabilitiesContainer.appendChild(item);
    });
}

// ============================================
// TAB 2: Batch Prediction
// ============================================

const uploadArea = document.getElementById('uploadArea');
const csvFileInput = document.getElementById('csvFile');
const predictBatchBtn = document.getElementById('predictBatch');
const downloadTemplateBtn = document.getElementById('downloadTemplate');
const batchResultsDiv = document.getElementById('batchResults');
const batchErrorDiv = document.getElementById('batchError');
const downloadResultsBtn = document.getElementById('downloadResults');

let selectedFile = null;

// Click to select file
uploadArea.addEventListener('click', () => csvFileInput.click());

// Drag and drop
uploadArea.addEventListener('dragover', (e) => {
    e.preventDefault();
    uploadArea.classList.add('dragover');
});

uploadArea.addEventListener('dragleave', () => {
    uploadArea.classList.remove('dragover');
});

uploadArea.addEventListener('drop', (e) => {
    e.preventDefault();
    uploadArea.classList.remove('dragover');
    const files = e.dataTransfer.files;
    if (files.length > 0) {
        handleFileSelect(files[0]);
    }
});

// File input change
csvFileInput.addEventListener('change', (e) => {
    if (e.target.files.length > 0) {
        handleFileSelect(e.target.files[0]);
    }
});

function handleFileSelect(file) {
    if (!file.name.endsWith('.csv')) {
        showError('Please select a CSV file', 'batchError');
        return;
    }
    
    selectedFile = file;
    uploadArea.innerHTML = `
        <svg class="upload-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor">
            <polyline points="20 6 9 17 4 12"></polyline>
        </svg>
        <p>✓ File selected: ${file.name}</p>
        <span style="font-size: 0.9em; color: #7f8c8d;">${(file.size / 1024).toFixed(2)} KB</span>
    `;
    predictBatchBtn.disabled = false;
    batchErrorDiv.classList.add('hidden');
}

// Batch prediction
predictBatchBtn.addEventListener('click', async () => {
    if (!selectedFile) {
        showError('Please select a CSV file first', 'batchError');
        return;
    }
    
    try {
        batchErrorDiv.classList.add('hidden');
        batchResultsDiv.classList.add('hidden');
        predictBatchBtn.disabled = true;
        predictBatchBtn.innerHTML = '<span class="loading"></span> Processing...';
        
        const formData = new FormData();
        formData.append('file', selectedFile);
        
        const response = await fetch('/api/batch-predict', {
            method: 'POST',
            body: formData
        });
        
        if (response.ok) {
            const blob = await response.blob();
            downloadResultsBtn.onclick = () => {
                const url = window.URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = url;
                a.download = 'predictions.csv';
                a.click();
                window.URL.revokeObjectURL(url);
            };
            
            document.getElementById('batchMessage').textContent = 
                `✓ Batch prediction completed! ${selectedFile.name} has been processed and classified.`;
            batchResultsDiv.classList.remove('hidden');
        } else {
            const error = await response.json();
            showError(error.error || 'Batch prediction failed', 'batchError');
        }
    } catch (error) {
        showError(error.message, 'batchError');
    } finally {
        predictBatchBtn.disabled = false;
        predictBatchBtn.innerHTML = 'Process Batch';
    }
});

// Download template
downloadTemplateBtn.addEventListener('click', () => {
    const template = `sepal_length,sepal_width,petal_length,petal_width
5.1,3.5,1.4,0.2
7.0,3.2,4.7,1.4
6.3,3.3,6.0,2.5
4.7,3.2,1.3,0.2
6.4,3.2,4.5,1.5`;
    
    const blob = new Blob([template], { type: 'text/csv' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'template.csv';
    a.click();
    window.URL.revokeObjectURL(url);
});

// ============================================
// TAB 3: Model Information
// ============================================

async function loadModelInfo() {
    try {
        const response = await fetch('/api/model-info');
        const data = await response.json();
        
        const html = `
            <p><strong>Model Type:</strong> ${data.model_type}</p>
            <p><strong>Classes:</strong> ${data.classes.join(', ')}</p>
            <p><strong>Features:</strong> ${data.features.join(', ')}</p>
            <p><strong>Total Dataset Size:</strong> ${data.dataset_size} samples</p>
            <p><strong>Training Samples:</strong> ${data.training_samples} (80%)</p>
            <p><strong>Testing Samples:</strong> ${data.testing_samples} (20%)</p>
        `;
        document.getElementById('modelDetails').innerHTML = html;
    } catch (error) {
        console.error('Failed to load model info:', error);
    }
}

async function loadDatasetStats() {
    try {
        const response = await fetch('/api/dataset-stats');
        const data = await response.json();
        
        let html = `<p><strong>Total Samples:</strong> ${data.total_samples}</p>`;
        
        // Species distribution
        html += '<p><strong>Species Distribution:</strong></p><ul>';
        Object.entries(data.species_distribution).forEach(([species, count]) => {
            const percentage = ((count / data.total_samples) * 100).toFixed(1);
            html += `<li>${species}: ${count} samples (${percentage}%)</li>`;
        });
        html += '</ul>';
        
        document.getElementById('datasetStats').innerHTML = html;
        
        // Feature ranges
        const rangesHtml = Object.entries(data.features).map(([feature, stats]) => `
            <div class="feature-item">
                <h4>${feature.replace(/_/g, ' ').toUpperCase()}</h4>
                <p><strong>Min:</strong> ${stats.min.toFixed(2)} cm</p>
                <p><strong>Max:</strong> ${stats.max.toFixed(2)} cm</p>
                <p><strong>Mean:</strong> ${stats.mean.toFixed(2)} cm</p>
            </div>
        `).join('');
        
        document.getElementById('featureRanges').innerHTML = rangesHtml;
    } catch (error) {
        console.error('Failed to load dataset stats:', error);
    }
}

// ============================================
// Utility Functions
// ============================================

function showError(message, elementId) {
    const errorElement = document.getElementById(elementId);
    errorElement.textContent = `❌ Error: ${message}`;
    errorElement.classList.remove('hidden');
}

// Load initial data
window.addEventListener('load', () => {
    // Check model status
    fetch('/health')
        .then(res => res.json())
        .then(data => {
            const statusElement = document.getElementById('modelStatus');
            if (data.model_loaded) {
                statusElement.innerHTML = '✓ Model Loaded';
                statusElement.className = 'status-badge loaded';
            }
        })
        .catch(err => console.error('Health check failed:', err));
});
