#checklist/models.py

from django.core.exceptions import ValidationError
from django.db import models

class Checklist(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Section(models.Model):
    checklist = models.ForeignKey(Checklist, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name} - {self.checklist.name}"


class ChecklistQuestion(models.Model):
    checklist = models.ForeignKey(Checklist, on_delete=models.CASCADE)  # Still referencing Checklist
    section = models.ForeignKey(Section, on_delete=models.SET_NULL, null=True, blank=True)  # New relationship
    question_id = models.AutoField(primary_key=True)
    question_text = models.TextField()

    def __str__(self):
        return f"{self.checklist.name} - {self.question_id} - {self.question_text}"

    def clean(self):
        """Ensure the question's checklist and section's checklist are the same."""
        if self.section and self.section.checklist != self.checklist:
            raise ValidationError('The section and checklist must belong to the same checklist.')
    
    def save(self, *args, **kwargs):
        """Override save to perform validation before saving the model."""
        self.clean()  # Ensure validation is called during save
        super(ChecklistQuestion, self).save(*args, **kwargs)
