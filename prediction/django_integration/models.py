from django.db import models
from django.contrib.auth.models import User


class PredictionRecord(models.Model):
    """Stores every prediction made through the system, per patient/session."""

    DISEASE_CHOICES = [
        ("diabetes", "Diabetes"),
        ("heart", "Heart Disease"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    disease_type = models.CharField(max_length=20, choices=DISEASE_CHOICES)
    input_data = models.JSONField()          # raw form inputs, kept for audit/report
    prediction = models.IntegerField()       # 0 = negative, 1 = positive
    probability = models.FloatField()        # model confidence for the positive class
    risk_segment = models.CharField(max_length=30, blank=True)  # from unsupervised module
    model_used = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.get_disease_type_display()} | {'Positive' if self.prediction else 'Negative'} | {self.created_at:%Y-%m-%d %H:%M}"
