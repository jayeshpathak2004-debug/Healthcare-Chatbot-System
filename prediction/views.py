from django.shortcuts import render
from django.conf import settings

import os
import joblib
import pandas as pd

from app5.models import DiseasePrediction

from .models import (
    DiabetesPrediction,
    HeartPrediction
)


# =========================================================
# HOME PAGE
# =========================================================

def prediction_home(request):

    return render(
        request,
        "prediction/prediction.html"
    )


# =========================================================
# DIABETES PREDICTION
# =========================================================

def diabetes_prediction(request):

    result = None
    probability = None

    if request.method == "POST":

        # -------------------------------------------------
        # GET INPUTS
        # -------------------------------------------------

        gender = request.POST.get("gender", "")

        pregnancies = float(
            request.POST.get("Pregnancies", 0)
        )

        glucose = float(
            request.POST.get("Glucose", 0)
        )

        blood_pressure = float(
            request.POST.get("BloodPressure", 0)
        )

        skin_thickness = float(
            request.POST.get("SkinThickness", 0)
        )

        insulin = float(
            request.POST.get("Insulin", 0)
        )

        bmi = float(
            request.POST.get("BMI", 0)
        )

        diabetes_pedigree = float(
            request.POST.get(
                "DiabetesPedigreeFunction",
                0
            )
        )

        age = float(
            request.POST.get("Age", 0)
        )

        # -------------------------------------------------
        # MALE = NO PREGNANCIES
        # -------------------------------------------------

        if gender == "Male":
            pregnancies = 0

        # -------------------------------------------------
        # CREATE DATAFRAME
        # -------------------------------------------------

        data = pd.DataFrame(
            [[
                pregnancies,
                glucose,
                blood_pressure,
                skin_thickness,
                insulin,
                bmi,
                diabetes_pedigree,
                age
            ]],
            columns=[
                "Pregnancies",
                "Glucose",
                "BloodPressure",
                "SkinThickness",
                "Insulin",
                "BMI",
                "DiabetesPedigreeFunction",
                "Age"
            ]
        )

        # -------------------------------------------------
        # LOAD MODEL
        # -------------------------------------------------

        model_path = os.path.join(
            settings.BASE_DIR,
            "prediction",
            "ml_model",
            "diabetes_model.pkl"
        )

        model = joblib.load(model_path)

        # -------------------------------------------------
        # PREDICTION
        # -------------------------------------------------

        prediction = model.predict(data)[0]

        # -------------------------------------------------
        # PROBABILITY
        # -------------------------------------------------

        if hasattr(model, "predict_proba"):

            probability = model.predict_proba(data)[0][1]

            probability = round(
                float(probability) * 100,
                2
            )

        else:

            probability = (
                100.0
                if prediction == 1
                else 0.0
            )

        # -------------------------------------------------
        # RESULT
        # -------------------------------------------------

        if prediction == 1:

            result = "Diabetic"

        else:

            result = "Not Diabetic"

        # -------------------------------------------------
        # SAVE DIABETES PREDICTION
        # -------------------------------------------------

        DiabetesPrediction.objects.create(

            age=int(age),

            glucose=glucose,

            bmi=bmi,

            prediction=int(prediction),

            probability=probability,

            model_used="Diabetes Random Forest"
        )

    # -----------------------------------------------------
    # RETURN PAGE
    # -----------------------------------------------------

    return render(
        request,
        "prediction/diabetes.html",
        {
            "result": result,
            "probability": probability,
        }
    )


# =========================================================
# HEART DISEASE PREDICTION
# =========================================================

def heart_prediction(request):

    result = None
    probability = None

    if request.method == "POST":

        # -------------------------------------------------
        # LOAD HEART MODEL
        # -------------------------------------------------

        model_path = os.path.join(
            settings.BASE_DIR,
            "prediction",
            "ml_model",
            "heart_model.pkl"
        )

        model = joblib.load(model_path)

        # -------------------------------------------------
        # GET INPUT VALUES
        # -------------------------------------------------

        age = float(request.POST["age"])
        sex = float(request.POST["sex"])
        cp = float(request.POST["cp"])
        trestbps = float(request.POST["trestbps"])
        chol = float(request.POST["chol"])
        fbs = float(request.POST["fbs"])
        restecg = float(request.POST["restecg"])
        thalach = float(request.POST["thalach"])
        exang = float(request.POST["exang"])
        oldpeak = float(request.POST["oldpeak"])
        ca = float(request.POST["ca"])
        thal = float(request.POST["thal"])

        # -------------------------------------------------
        # CREATE INPUT
        # -------------------------------------------------

        values = [
            age,
            sex,
            cp,
            trestbps,
            chol,
            fbs,
            restecg,
            thalach,
            exang,
            oldpeak,
            ca,
            thal
        ]

        # -------------------------------------------------
        # PREDICTION
        # -------------------------------------------------

        prediction = model.predict(
            [values]
        )[0]

        # -------------------------------------------------
        # PROBABILITY
        # -------------------------------------------------

        if hasattr(model, "predict_proba"):

            probabilities = model.predict_proba(
                [values]
            )[0]

            probability = round(
                float(probabilities[1]) * 100,
                2
            )

        else:

            probability = (
                100.0
                if prediction == 1
                else 0.0
            )

        # -------------------------------------------------
        # RESULT
        # -------------------------------------------------

        if prediction == 1:

            result = "Heart Disease Detected"

        else:

            result = "No Heart Disease"

        # -------------------------------------------------
        # SAVE HEART PREDICTION
        # -------------------------------------------------

        HeartPrediction.objects.create(

            age=int(age),

            trestbps=trestbps,

            chol=chol,

            prediction=int(prediction),

            probability=probability,

            model_used="Heart Random Forest"
        )

    # -----------------------------------------------------
    # RETURN PAGE
    # -----------------------------------------------------

    return render(
        request,
        "prediction/heart.html",
        {
            "result": result,
            "probability": probability,
        }
    )


# =========================================================
# HISTORY
# =========================================================


def history(request):

    query = request.GET.get("q", "").strip()

    # ==========================================
    # DIABETES
    # ==========================================

    diabetes_records = DiabetesPrediction.objects.all()

    # ==========================================
    # HEART
    # ==========================================

    heart_records = HeartPrediction.objects.all()

    # ==========================================
    # ML DISEASE
    # ==========================================

    ml_records = DiseasePrediction.objects.all()

    # ==========================================
    # SEARCH
    # ==========================================

    if query:

        diabetes_records = diabetes_records.filter(
            model_used__icontains=query
        )

        heart_records = heart_records.filter(
            model_used__icontains=query
        )

        ml_records = ml_records.filter(
            predicted_disease__icontains=query
        )

    # ==========================================
    # ORDER
    # ==========================================

    diabetes_records = diabetes_records.order_by(
        "-created_at"
    )

    heart_records = heart_records.order_by(
        "-created_at"
    )

    ml_records = ml_records.order_by(
        "-created_at"
    )

    # ==========================================
    # RETURN
    # ==========================================

    return render(
        request,
        "prediction/history.html",
        {
            "diabetes_records": diabetes_records,
            "heart_records": heart_records,
            "ml_records": ml_records,
            "query": query,
        }
    )

# def history(request):
#
#     query = request.GET.get("q", "").strip()
#
#     diabetes_records = DiabetesPrediction.objects.all()
#
#     heart_records = HeartPrediction.objects.all()
#
#     # -----------------------------------------------------
#     # SEARCH
#     # -----------------------------------------------------
#
#     if query:
#
#         diabetes_records = diabetes_records.filter(
#             model_used__icontains=query
#         )
#
#         heart_records = heart_records.filter(
#             model_used__icontains=query
#         )
#
#     # -----------------------------------------------------
#     # ORDER
#     # -----------------------------------------------------
#
#     diabetes_records = diabetes_records.order_by(
#         "-created_at"
#     )
#
#     heart_records = heart_records.order_by(
#         "-created_at"
#     )
#
#     return render(
#         request,
#         "prediction/history.html",
#         {
#             "diabetes_records": diabetes_records,
#             "heart_records": heart_records,
#             "query": query,
#         }
#     )


# # # =========================================================
# # # DELETE DIABETES
# # # =========================================================
# #
# # def delete_diabetes_prediction(request, id):
# #
# #     record = get_object_or_404(
# #         DiabetesPrediction,
# #         id=id
# #     )
# #
# #     record.delete()
# #
# #     return redirect("history")
#
#
# # =========================================================
# # DELETE HEART
# # =========================================================
#
# def delete_heart_prediction(request, id):
#
#     record = get_object_or_404(
#         HeartPrediction,
#         id=id
#     )
#
#     record.delete()
#
#     return redirect("history")


# =========================================================
# DASHBOARD
# =========================================================

def dashboard(request):

    # =====================================================
    # DIABETES
    # =====================================================

    diabetes_predictions = DiabetesPrediction.objects.all()

    diabetes_count = diabetes_predictions.count()

    diabetes_positive = diabetes_predictions.filter(
        prediction=1
    ).count()

    diabetes_negative = diabetes_predictions.filter(
        prediction=0
    ).count()

    # =====================================================
    # HEART
    # =====================================================

    heart_predictions = HeartPrediction.objects.all()

    heart_count = heart_predictions.count()

    heart_positive = heart_predictions.filter(
        prediction=1
    ).count()

    heart_negative = heart_predictions.filter(
        prediction=0
    ).count()

    # =====================================================
    # ML DISEASE - APP5
    # =====================================================

    ml_predictions = DiseasePrediction.objects.all()

    ml_count = ml_predictions.count()

    # =====================================================
    # TOTAL HEART + DIABETES
    # =====================================================

    total_predictions = (
        diabetes_count +
        heart_count
    )

    # =====================================================
    # TOTAL INCLUDING ML
    # =====================================================

    total_all_predictions = (
        total_predictions +
        ml_count
    )

    # =====================================================
    # POSITIVE / NEGATIVE
    # HEART + DIABETES
    # =====================================================

    positive_count = (
        diabetes_positive +
        heart_positive
    )

    negative_count = (
        diabetes_negative +
        heart_negative
    )

    # =====================================================
    # RECENT DIABETES
    # =====================================================

    recent_diabetes = diabetes_predictions.order_by(
        "-created_at"
    )[:10]

    # =====================================================
    # RECENT HEART
    # =====================================================

    recent_heart = heart_predictions.order_by(
        "-created_at"
    )[:10]

    # =====================================================
    # RECENT ML
    # =====================================================

    recent_ml_predictions = ml_predictions.order_by(
        "-created_at"
    )[:10]

    # =====================================================
    # ML DISEASE COUNTS
    # =====================================================

    ml_disease_counts = {}

    for record in ml_predictions:

        disease = record.predicted_disease

        if disease in ml_disease_counts:

            ml_disease_counts[disease] += 1

        else:

            ml_disease_counts[disease] = 1

    ml_disease_counts = dict(
        sorted(
            ml_disease_counts.items(),
            key=lambda item: item[1],
            reverse=True
        )
    )

    # =====================================================
    # DASHBOARD
    # =====================================================

    return render(
        request,
        "prediction/dashboard.html",
        {

            # -------------------------------------------------
            # TOTAL
            # -------------------------------------------------

            "total_predictions":
                total_predictions,

            "total_all_predictions":
                total_all_predictions,

            "positive_count":
                positive_count,

            "negative_count":
                negative_count,

            # -------------------------------------------------
            # DIABETES
            # -------------------------------------------------

            "diabetes_count":
                diabetes_count,

            "diabetes_positive":
                diabetes_positive,

            "diabetes_negative":
                diabetes_negative,

            "recent_diabetes":
                recent_diabetes,

            # -------------------------------------------------
            # HEART
            # -------------------------------------------------

            "heart_count":
                heart_count,

            "heart_positive":
                heart_positive,

            "heart_negative":
                heart_negative,

            "recent_heart":
                recent_heart,

            # -------------------------------------------------
            # ML DISEASE
            # -------------------------------------------------

            "ml_count":
                ml_count,

            "recent_ml_predictions":
                recent_ml_predictions,

            "ml_disease_counts":
                ml_disease_counts,
        }
    )


def delete_prediction(request, prediction_type, id):

    if prediction_type == "diabetes":

        record = get_object_or_404(
            DiabetesPrediction,
            id=id
        )

        record.delete()

    elif prediction_type == "heart":

        record = get_object_or_404(
            HeartPrediction,
            id=id
        )

        record.delete()

    return redirect("history")