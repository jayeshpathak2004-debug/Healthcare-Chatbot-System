from django.urls import path
from .views import chatbot, symptom_check, text_to_speech  # Import the function

urlpatterns = [
    path('', chatbot, name='chatbot'),
    path('symptom_check/', symptom_check, name='symptom_check'),
    path('text-to-speech/', text_to_speech, name='text_to_speech'),
]
