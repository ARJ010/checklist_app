from django.urls import path

from . import views
from checklist import views as checklist_views


urlpatterns = [
    path("", views.my_protected_view, name="manager_index"),
    path('user_register/', views.register_user, name='user_register'),
    path('all_users/', views.all_users, name='all_users'),
    path('delete_users/', views.delete_users, name='delete_users'),
    path('delete_user/', views.delete_user, name='delete_user'),
    path('user_details/', views.user_details, name='user_details'),
    path('edit_profile/', views.edit_user_profile, name='edit_user_profile'),
    path('change_password/', views.change_password, name='change_password'),
    path('all_checklist/', checklist_views.all_checklist, name='all_checklist'),
    path('add_checklist/', checklist_views.add_checklist, name='add_checklist'),
    path('add_checklist_questions/', checklist_views.add_checklist_question, name='add_questions'),
    path('delete_checklist/', checklist_views.delete_checklist, name='delete_checklist'),
    path('checklist_details/', checklist_views.checklist_detail, name='checklist_detail'),
    path('checklist_edit/', checklist_views.edit_checklist, name='edit_checklist'),
    path('add-section/', checklist_views.add_section, name='add_section'),
    path('edit_section/', checklist_views.edit_section, name='edit_section'),
    path('History/', views.admin_history, name='admin_history'),
    path("history_response/<int:procedure_id>/", views.admin_history_response, name="admin_history_response"),
    path("admin_processing/", views.admin_processing, name="admin_processing"),
    path("admin_procedure_edit/<int:procedure_id>/", views.admin_procedure_edit, name="admin_procedure_edit"),
    path("procedure_details/", views.procedure_details, name="procedure_details"),
]