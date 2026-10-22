from django.db import models


class DiseasePrediction(models.Model):

    patient_name = models.CharField(
        max_length=150
    )

    age = models.PositiveIntegerField(
        null=True,
        blank=True
    )

    gender = models.CharField(
        max_length=20,
        blank=True
    )

    symptoms = models.TextField()

    predicted_disease = models.CharField(
        max_length=255
    )

    confidence = models.FloatField(
        default=0
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):

        return (
            f"{self.patient_name} - "
            f"{self.predicted_disease}"
        )