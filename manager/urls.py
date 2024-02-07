from django.urls import path

from . import views


urlpatterns = [
    path("", views.index, name="manager_index"),
]