from django.urls import path

from . import views


urlpatterns = [
    path("", views.my_protected_view, name="checker_index"),
    path("all_process/", views.all_procedures, name="all_procedures"),
    path("proceed_procedure/<int:procedure_id>/", views.proceed_procedure, name="proceed_procedure"),  
    path("my_process/", views.my_procedures, name="my_procedures"),  
    path("cancel_procedure/<int:procedure_id>/", views.cancel_procedure, name="cancel_procedure"),
    path("view_response/<int:procedure_id>/", views.view_response, name="view_response"),
    path("edit_response/<int:procedure_id>/", views.edit_responses, name="edit_response"),
    path("edit_response_first/<int:procedure_id>/", views.edit_response_first, name="edit_response_first"),
    path("return_response/<int:procedure_id>/", views.return_procedure, name="return_procedure"),
    path("return/", views.checkers_returned, name="checkers_returned"),  
    path("final_submit/<int:procedure_id>/", views.final_submit, name="final_submit"),
    path("checkers_history/", views.checkers_history, name="checkers_history"),
    path("history_response/<int:procedure_id>/", views.history_response, name="history_response"),
]