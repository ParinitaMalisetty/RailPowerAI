import os
import joblib
import numpy as np
from django.shortcuts import render
from django.conf import settings

# Paths to models
MODEL_DIR = os.path.join(settings.BASE_DIR, 'predictor', 'ml_models')
clf_basic = joblib.load(os.path.join(MODEL_DIR, 'fault_classifier.pkl'))
clf_scaled = joblib.load(os.path.join(MODEL_DIR, 'fault_classifier_scaled.pkl'))
reg_basic = joblib.load(os.path.join(MODEL_DIR, 'load_regressor.pkl'))
reg_scaled = joblib.load(os.path.join(MODEL_DIR, 'load_regressor_scaled.pkl'))
scaler = joblib.load(os.path.join(MODEL_DIR, 'scaler.pkl'))

fault_map = {
    'Derailment Risk': '🚨 Derailment Risk',
    'Overload': '⚠️ Overload',
    'Fluctuation': '🔄 Fluctuation',
    'No Fault': '✅ No Fault'
}

def home(request):
    return render(request, 'predictor/home.html')


# --- Fault Classification ---

def classify_basic(request):
    result = None
    if request.method == 'POST':
        features = [float(request.POST[key]) for key in ['Voltage', 'Current', 'Temperature', 'Vibration', 'Speed']]
        prediction = clf_basic.predict([features])[0]
        result = fault_map.get(prediction, prediction)
    return render(request, 'predictor/classify_basic.html', {'result': result})


def classify_scaled(request):
    result = None
    if request.method == 'POST':
        features = [float(request.POST[key]) for key in ['Voltage', 'Current', 'Temperature', 'Vibration', 'Speed']]
        scaled_features = scaler.transform([features])
        prediction = clf_scaled.predict(scaled_features)[0]
        result = fault_map.get(prediction, prediction)
    return render(request, 'predictor/classify_scaled.html', {'result': result})


# --- Load Forecasting ---

from django.shortcuts import render
import numpy as np

def forecast_basic(request):
    if request.method == 'POST':
        try:
            voltage = float(request.POST['voltage'])
            current = float(request.POST['current'])
            temperature = float(request.POST['temperature'])
            vibration = float(request.POST['vibration'])
            speed = float(request.POST['speed'])

            features = np.array([[voltage, current, temperature, vibration, speed]])
            load_prediction = reg_basic.predict(features)[0]
            result = f"⚡ Predicted Load: {load_prediction:.2f} kW"
        except Exception as e:
            result = f"❌ Error: {str(e)}"
        
        return render(request, 'predictor/forecast_basic.html', {'result': result})
    
    return render(request, 'predictor/forecast_basic.html')



# --- SCALED LOAD FORECAST ---
def forecast_scaled(request):
    result = ""
    if request.method == 'POST':
        try:
            voltage = float(request.POST['voltage'])
            current = float(request.POST['current'])
            temperature = float(request.POST['temperature'])
            vibration = float(request.POST['vibration'])
            speed = float(request.POST['speed'])

            features = np.array([[voltage, current, temperature, vibration, speed]])
            scaled_features = scaler.transform(features)
            prediction = reg_scaled.predict(scaled_features)[0]
            result = f"⚡ Predicted Load: {prediction:.2f} kW"
        except Exception as e:
            result = f"❌ Error: {str(e)}"
    return render(request, 'predictor/forecast_scaled.html', {'result': result})