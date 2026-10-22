from django.urls import path
from . import views

app_name = "predictions"

urlpatterns = [
    path("diabetes/", views.diabetes_predict_view, name="diabetes"),
    path("heart/", views.heart_predict_view, name="heart"),
    path("history/", views.history_view, name="history"),
]
