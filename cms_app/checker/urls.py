from django.urls import path

from . import views


urlpatterns = [
    path("", views.my_protected_view, name="checker_index"),
    path("all_process/", views.all_procedures, name="all_procedures"),
    path("proceed_procedure/", views.proceed_procedure, name="proceed_procedure"),  
    path("my_process/", views.my_procedures, name="my_procedures"),  
    path("cancel_procedure/", views.cancel_procedure, name="cancel_procedure"),
    path("view_response/", views.view_response, name="view_response"),
    path("edit_response/", views.edit_responses, name="edit_response"),
    path("return_response/", views.return_procedure, name="return_procedure"),
    path("return/", views.checkers_returned, name="checkers_returned"),  
    path("final_submit/", views.final_submit, name="final_submit"),
    path("checkers_history/", views.checkers_history, name="checkers_history"),

]