from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import DiseasePrediction


@admin.register(DiseasePrediction)
class DiseasePredictionAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "patient_name",
        "age",
        "gender",
        "predicted_disease",
        "confidence",
        "created_at",
    )

    list_filter = (
        "gender",
        "predicted_disease",
        "created_at",
    )

    search_fields = (
        "patient_name",
        "symptoms",
        "predicted_disease",
    )

    readonly_fields = (
        "created_at",
    )

    ordering = (
        "-created_at",
    )