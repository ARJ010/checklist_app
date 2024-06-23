# checker/forms.py

from django import forms
from .models import ProcedureResponse

class ProcedureForm(forms.Form):
    def __init__(self, *args, **kwargs):
        checklist_questions = kwargs.pop('checklist_questions')
        super(ProcedureForm, self).__init__(*args, **kwargs)
        
        for question in checklist_questions:
            field_name = f"question_{question.pk}"
            self.fields[field_name] = forms.ChoiceField(
                label=question.question_text,
                choices=[('yes', 'Yes'), ('no', 'No'), ('na', 'N/A')],
                widget=forms.RadioSelect(attrs={'class': 'form-check-input'}),
            )
            self.fields[f"remarks_{question.pk}"] = forms.CharField(
                label="Remarks",
                required=False,
                widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            )

class CheckerProcedureResponseForm(forms.ModelForm):
    class Meta:
        model = ProcedureResponse
        fields = ['response', 'remarks', 'user_response']
    
    def __init__(self, *args, **kwargs):
        super(CheckerProcedureResponseForm, self).__init__(*args, **kwargs)
        self.fields['user_response'].disabled = True