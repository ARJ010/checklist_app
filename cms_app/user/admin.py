from django.contrib import admin
from .models import Procedure

@admin.register(Procedure)
class ProcedureAdmin(admin.ModelAdmin):
    list_display = ('id', 'client_name', 'user', 'status', 'checklist', 'return_count', 'date_created', 'final_submission_date', 'returned_date')  # Display key fields in the admin view
    search_fields = ('client_name', 'user__username', 'checker__username', 'checklist__name', 'status')  # Search across fields
    list_filter = ('status', 'checklist', 'user', 'checker', 'return_count', 'date_created')  # Filter by status, checklist, and other fields
    readonly_fields = ('date_created', 'final_submission_date', 'returned_date')  # Prevent editing of certain fields

    def get_readonly_fields(self, request, obj=None):
        """
        Override to make the status field readonly after the procedure is submitted.
        """
        if obj and obj.status != 'Pending':
            return self.readonly_fields + ('status',)
        return self.readonly_fields
