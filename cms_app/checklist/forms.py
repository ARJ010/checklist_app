from django import forms
from .models import Checklist, ChecklistQuestion


class ChecklistQuestionForm(forms.ModelForm):
    class Meta:
        model = ChecklistQuestion
        fields = ['checklist', 'question_text']
        widgets = {
            'checklist': forms.Select(attrs={'class': 'form-control'}),
            'question_text': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['checklist'].queryset = Checklist.objects.all()
