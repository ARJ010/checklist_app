from django.urls import path

from . import views


urlpatterns = [
    path("", views.my_protected_view, name="user_index"),
    path('draft/', views.draft, name='draft'),
    path('add/', views.add_procedure, name='add_procedure'),
    path('submit/', views.submit_procedure, name='submit_procedure'),
    path('edit/', views.edit_procedure, name='edit_procedure'),
    path('delete/', views.delete_procedure, name='delete_procedure'),
    path('status/', views.status, name='status'),
    path('returned/', views.returned, name='returned'),
    path('history/', views.history, name='history'),

] 