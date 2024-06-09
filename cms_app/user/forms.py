from django import forms
from .models import Procedure

class ProcedureForm(forms.ModelForm):
    
    class Meta:
        model = Procedure
        fields = ['client_name','data_path', 'checklist']
