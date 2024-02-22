from django.contrib import admin
from .models import Checklist, ChecklistQuestion

# Register your models here.


admin.site.register(Checklist)
admin.site.register(ChecklistQuestion)

