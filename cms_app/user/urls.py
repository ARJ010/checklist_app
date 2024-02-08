from django.urls import path

from . import views


urlpatterns = [
    path("", views.my_protected_view, name="user_index"),
]