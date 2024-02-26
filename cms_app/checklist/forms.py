from django import forms
from .models import Checklist, ChecklistQuestion


class ChecklistForm(forms.ModelForm):
    class Meta:
        model = Checklist
        fields = ['name']

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if Checklist.objects.filter(name=name).exists():
            raise forms.ValidationError("A checklist with this name already exists.")
        return name


class ChecklistQuestionForm(forms.ModelForm):
    class Meta:
        model = ChecklistQuestion
        fields = ['question_text']
        widgets = {
            'question_text': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }