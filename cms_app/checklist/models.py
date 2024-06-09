#checklist/models.py

from django.db import models

# Create your models here.


class Checklist(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class ChecklistQuestion(models.Model):
    checklist = models.ForeignKey(Checklist, on_delete=models.CASCADE)
    question_id = models.AutoField(primary_key=True)
    question_text = models.TextField()

    def __str__(self):
        return f"Question {self.question_id} - {self.question_text}"
