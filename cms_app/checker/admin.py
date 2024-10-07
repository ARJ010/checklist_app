from django.contrib import admin
from .models import ProcedureResponse

@admin.register(ProcedureResponse)
class ProcedureResponseAdmin(admin.ModelAdmin):
    list_display = ('procedure', 'question', 'response', 'remarks', 'user_response')  # Display these fields in list view
    search_fields = ('procedure__id', 'question__question_id', 'response', 'remarks', 'user_response')  # Enable search on relevant fields
    list_filter = ('response', 'procedure', 'question')  # Filter by response type, procedure, and question
