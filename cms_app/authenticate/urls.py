# accounts/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('login/',views.logout_view, name='logout')
    # Add other authentication-related URLs here (e.g., registration, logout)
]
