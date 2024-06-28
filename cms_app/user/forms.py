from django import forms
from .models import Procedure
from checker.models import ProcedureResponse

class ProcedureForm(forms.ModelForm):
    
    class Meta:
        model = Procedure
        fields = ['client_name','data_path', 'checklist']


class UserProcedureResponseForm(forms.ModelForm):
    class Meta:
        model = ProcedureResponse
        fields = ['response', 'remarks', 'user_response']

    def __init__(self, *args, **kwargs):
        super(UserProcedureResponseForm, self).__init__(*args, **kwargs)
        self.fields['response'].disabled = True
        self.fields['remarks'].disabled = True
        
        # Update widget attributes
        for field_name in self.fields:
            if isinstance(self.fields[field_name].widget, forms.Textarea):
                self.fields[field_name].widget.attrs.update({'rows': 1})