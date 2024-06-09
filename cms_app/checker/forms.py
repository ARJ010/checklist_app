from django import forms
from user.models import Procedure
from checklist.models import ChecklistQuestion
from .models import ProcedureResponse

class ProcedureForm(forms.Form):
    def __init__(self, *args, **kwargs):
        checklist_questions = kwargs.pop('checklist_questions')
        super(ProcedureForm, self).__init__(*args, **kwargs)
        
        # Add a form field for each checklist question
        for question in checklist_questions:
            field_name = f"question_{question.pk}"
            self.fields[field_name] = forms.ChoiceField(
                label=question.question_text,
                choices=[('yes', 'Yes'), ('no', 'No'), ('na', 'N/A')],
                widget=forms.RadioSelect(attrs={'class': 'form-check-input'}),
            )


class ProcedureResponseForm(forms.ModelForm):
    class Meta:
        model = ProcedureResponse
        fields = ['response']