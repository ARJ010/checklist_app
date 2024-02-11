from django.urls import path

from . import views


urlpatterns = [
    path("", views.my_protected_view, name="manager_index"),
    path('user_register/', views.register_user, name='user_register'),
    path('all_users/', views.all_users, name='all_users'),
    path('delete_users/', views.delete_users, name='delete_users'),
    path('delete_user/', views.delete_user, name='delete_user'),
    path('user_details/', views.user_details, name='user_details'),
    path('edit_profile/', views.edit_user_profile, name='edit_user_profile'),
]