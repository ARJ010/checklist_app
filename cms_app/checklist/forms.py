from django import forms
from django.forms import inlineformset_factory
from .models import Checklist, ChecklistQuestion, Section

# Checklist form remains the same
class ChecklistForm(forms.ModelForm):
    class Meta:
        model = Checklist
        fields = ['name']

    def clean_name(self):
        name = self.cleaned_data.get('name')
        instance = self.instance
        if instance and Checklist.objects.exclude(id=instance.id).filter(name=name).exists():
            raise forms.ValidationError("A checklist with this name already exists.")
        return name

# New form for Section
class SectionForm(forms.ModelForm):
    class Meta:
        model = Section
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }


SectionFormSet = inlineformset_factory(
    Checklist,  # Parent model
    Section,  # Child model
    form=SectionForm,  # Form to use for the inline formset
    fields=['name'],  # Fields to include in the formset
    extra=1,  # Number of extra forms to display
    can_delete=True,  # Allow deletion of existing sections
)

# ChecklistQuestion form remains the same
class ChecklistQuestionForm(forms.ModelForm):
    class Meta:
        model = ChecklistQuestion
        fields = ['question_text', 'section']
        widgets = {
            'question_text': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'section': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        checklist = kwargs.pop('checklist', None)  # Pass the checklist instance when initializing
        super(ChecklistQuestionForm, self).__init__(*args, **kwargs)
        if checklist:
            self.fields['section'].queryset = Section.objects.filter(checklist=checklist)  # Filter sections by checklist


# Define the inline formset for ChecklistQuestion
ChecklistQuestionFormSet = inlineformset_factory(
    Checklist,  # Parent model
    ChecklistQuestion,  # Child model
    form=ChecklistQuestionForm,  # Form to use for the inline formset
    fields=['question_text', 'section'],  # Include 'section' field
    extra=1,  # Number of extra forms to display
    can_delete=True,  # Allow deletion of existing questions
)

