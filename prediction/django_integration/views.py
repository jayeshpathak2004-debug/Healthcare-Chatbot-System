"""
views.py
---------
Wires the trained ML models (supervised) and the risk-segmentation
K-Means model (unsupervised) into Django views, following the same
pattern used in the Laptop Price Prediction System (form -> validate ->
load pickled model -> predict -> render result).
"""

import os
import joblib
import numpy as np
from django.shortcuts import render
from django.conf import settings

from .forms import DiabetesForm, HeartDiseaseForm
from .models import PredictionRecord

# Point this to wherever you copy the /models folder in your Django project,
# e.g. BASE_DIR / "ml_models"
MODEL_DIR = os.path.join(settings.BASE_DIR, "ml_models")

_model_cache = {}


def _load_bundle(disease_type):
    """Loads (model, scaler, feature_names) once and caches it in memory."""
    if disease_type not in _model_cache:
        path = os.path.join(MODEL_DIR, f"{disease_type}_model.pkl")
        _model_cache[disease_type] = joblib.load(path)
    return _model_cache[disease_type]


def _risk_segment_from_probability(prob):
    """Lightweight stand-in for the unsupervised K-Means segment lookup —
    in the full system you'd instead run the saved KMeans + scaler on the
    same input vector (see unsupervised_module.py) and map cluster -> label."""
    if prob < 0.33:
        return "Low Risk"
    elif prob < 0.66:
        return "Moderate Risk"
    return "High Risk"


def _predict(disease_type, form_data):
    bundle = _load_bundle(disease_type)
    model, scaler, feature_names = bundle["model"], bundle["scaler"], bundle["feature_names"]

    ordered_values = [float(form_data[name]) for name in feature_names]
    X = np.array(ordered_values).reshape(1, -1)
    X_scaled = scaler.transform(X)

    prediction = int(model.predict(X_scaled)[0])
    probability = float(model.predict_proba(X_scaled)[0][1]) if hasattr(model, "predict_proba") else float(prediction)
    risk_segment = _risk_segment_from_probability(probability)

    return prediction, probability, risk_segment, bundle["model_name"]


def diabetes_predict_view(request):
    result = None
    if request.method == "POST":
        form = DiabetesForm(request.POST)
        if form.is_valid():
            prediction, probability, risk_segment, model_name = _predict("diabetes", form.cleaned_data)

            PredictionRecord.objects.create(
                user=request.user if request.user.is_authenticated else None,
                disease_type="diabetes",
                input_data=form.cleaned_data,
                prediction=prediction,
                probability=probability,
                risk_segment=risk_segment,
                model_used=model_name,
            )

            result = {
                "prediction": "Diabetic" if prediction == 1 else "Not Diabetic",
                "probability": round(probability * 100, 2),
                "risk_segment": risk_segment,
                "model_used": model_name,
            }
    else:
        form = DiabetesForm()

    return render(request, "predictions/diabetes_form.html", {"form": form, "result": result})


def heart_predict_view(request):
    result = None
    if request.method == "POST":
        form = HeartDiseaseForm(request.POST)
        if form.is_valid():
            prediction, probability, risk_segment, model_name = _predict("heart", form.cleaned_data)

            PredictionRecord.objects.create(
                user=request.user if request.user.is_authenticated else None,
                disease_type="heart",
                input_data=form.cleaned_data,
                prediction=prediction,
                probability=probability,
                risk_segment=risk_segment,
                model_used=model_name,
            )

            result = {
                "prediction": "Heart Disease Detected" if prediction == 1 else "No Heart Disease",
                "probability": round(probability * 100, 2),
                "risk_segment": risk_segment,
                "model_used": model_name,
            }
    else:
        form = HeartDiseaseForm()

    return render(request, "predictions/heart_form.html", {"form": form, "result": result})


def history_view(request):
    """Shows past predictions — handy for a demo/report screenshot."""
    records = PredictionRecord.objects.all()[:50]
    return render(request, "predictions/history.html", {"records": records})
