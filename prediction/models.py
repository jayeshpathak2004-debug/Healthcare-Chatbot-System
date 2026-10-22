from django.db import models


class DiabetesPrediction(models.Model):

    age = models.IntegerField()

    glucose = models.FloatField()

    bmi = models.FloatField()

    prediction = models.IntegerField()

    probability = models.FloatField()

    model_used = models.CharField(
        max_length=100
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):

        return (
            f"Diabetes | "
            f"{self.prediction} | "
            f"{self.created_at}"
        )


class HeartPrediction(models.Model):

    age = models.IntegerField()

    trestbps = models.FloatField()

    chol = models.FloatField()

    prediction = models.IntegerField()

    probability = models.FloatField()

    model_used = models.CharField(
        max_length=100
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):

        return (
            f"Heart Disease | "
            f"{self.prediction} | "
            f"{self.created_at}"
        )