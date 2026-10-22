from django.urls import path
from . import views

# urlpatterns = [
#     path('signup/', views.signup, name='register'),
#     path('signup/register/', views.register),  # Include 'signup/register/' pattern
# ]
from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('signup/register/', views.register, name='register'),
]
