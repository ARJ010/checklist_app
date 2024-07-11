from django.urls import path

from . import views


urlpatterns = [
    path('', views.user_index, name='user_index'),
    path('draft/', views.draft, name='draft'),
    path('add/', views.add_procedure, name='add_procedure'),
    path('submit/<int:procedure_id>/', views.submit_procedure, name='submit_procedure'),
    path('edit/<int:procedure_id>/', views.edit_procedure, name='edit_procedure'),
    path('delete/<int:procedure_id>/', views.delete_procedure, name='delete_procedure'),
    path('delete_temp/<int:procedure_id>/', views.temp_delete_procedure, name='delete_temp'),
    path('trash/', views.trash, name='trash'),
    path('restore/<int:procedure_id>/', views.restore_procedure, name='restore_procedure'),
    path('status/', views.status, name='status'),
    path('returned/', views.returned, name='returned'),
    path('history/', views.history, name='history'),
    path('view_responses/<int:procedure_id>/', views.user_view_responses, name='user_view_responses'),
    path('edit_responses/<int:procedure_id>/', views.user_edit_responses, name='user_edit_responses'),
    path("history_response/<int:procedure_id>/", views.user_history_response, name="user_history_response"),

] 