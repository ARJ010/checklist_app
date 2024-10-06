# checker/forms.py

from django import forms
from .models import ProcedureResponse

class ProcedureForm(forms.Form):
    def __init__(self, *args, **kwargs):
        checklist_sections = kwargs.pop('checklist_sections')
        super(ProcedureForm, self).__init__(*args, **kwargs)

        for section, questions in checklist_sections.items():
            for question in questions:
                field_name = f"question_{question.pk}"
                self.fields[field_name] = forms.ChoiceField(
                    label=f"{section.name} - {question.question_text}",  # Display section name in label
                    choices=[('yes', 'Yes'), ('no', 'No'), ('na', 'N/A'), ('-----', '-----')],
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

        # Update widget attributes
        for field_name in self.fields:
            if isinstance(self.fields[field_name].widget, forms.Textarea):
                self.fields[field_name].widget.attrs.update({'rows': 1})
