# from django.urls import path
# from . import views

# # urlpatterns = [
# #     path('signin/', views.signin, name='signin'),
# #     path('signin', views.login, name='login'),  # Include 'signup/register/' pattern
# #     path('logout/', views.logout_view, name='logout'),
# # ]
# urlpatterns = [
#     path('signin/', views.login, name='login'),
#     path('logout/', views.logout_view, name='logout'),
# ]
from django.urls import path
from . import views

urlpatterns = [
    path('signin/', views.login, name='login'),
    path('logout/', views.logout_view, name='logout'),
]