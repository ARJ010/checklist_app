from django.urls import path

from . import views


urlpatterns = [
    path("", views.my_protected_view, name="manager_index"),
    path('user_register/', views.register_user, name='user_register'),
    path('all_users/', views.all_users, name='all_users'),
    path('delete_users/', views.delete_users, name='delete_users'),
]