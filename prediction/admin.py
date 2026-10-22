
from django.contrib import admin

from .models import (
    DiabetesPrediction,
    HeartPrediction
)


# =========================================================
# DIABETES PREDICTION ADMIN
# =========================================================

@admin.register(DiabetesPrediction)
class DiabetesPredictionAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "age",
        "glucose",
        "bmi",
        "prediction",
        "probability",
        "model_used",
        "created_at",
    )

    list_filter = (
        "prediction",
        "created_at",
        "model_used",
    )

    search_fields = (
        "model_used",
    )

    ordering = (
        "-created_at",
    )


# =========================================================
# HEART DISEASE PREDICTION ADMIN
# =========================================================

@admin.register(HeartPrediction)
class HeartPredictionAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "age",
        "trestbps",
        "chol",
        "prediction",
        "probability",
        "model_used",
        "created_at",
    )

    list_filter = (
        "prediction",
        "created_at",
        "model_used",
    )

    search_fields = (
        "model_used",
    )

    ordering = (
        "-created_at",
    )

