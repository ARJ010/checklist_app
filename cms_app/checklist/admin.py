from django.contrib import admin
from .models import Checklist, ChecklistQuestion, Section

# Register your models here.

@admin.register(Checklist)
class ChecklistAdmin(admin.ModelAdmin):
    list_display = ('name',)  # Display fields in the list view
    search_fields = ('name',)  # Search functionality
    list_filter = ('name',)  # Filter by name


@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    list_display = ('name', 'checklist')  # Show both name and checklist in the admin view
    search_fields = ('name', 'checklist__name')  # Search by section name and checklist name
    list_filter = ('checklist',)  # Filter by checklist


@admin.register(ChecklistQuestion)
class ChecklistQuestionAdmin(admin.ModelAdmin):
    list_display = ('question_text', 'checklist', 'section')  # Display text, checklist, and section
    search_fields = ('question_text', 'checklist__name', 'section__name')  # Search functionality
    list_filter = ('checklist', 'section')  # Filter by checklist and section
