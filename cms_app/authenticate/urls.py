# accounts/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('login/',views.logout_view, name='logout'),
    path('test/', views.test_view, name='test_view'),
    # Add other authentication-related URLs here (e.g., registration, logout)
]
