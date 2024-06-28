# checker/models.py

from django.db import models
from user.models import Procedure
from checklist.models import ChecklistQuestion

class ProcedureResponse(models.Model):
    procedure = models.ForeignKey(Procedure, on_delete=models.CASCADE)
    question = models.ForeignKey(ChecklistQuestion, on_delete=models.CASCADE)
    response = models.CharField(max_length=10, choices=[('yes', 'Yes'), ('no', 'No'), ('na', 'N/A')])
    remarks = models.TextField(blank=True, null=True)
    user_response = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Response for Procedure {self.procedure.id}, Question {self.question.question_id}: {self.response}, Remarks: {self.remarks}, User Response: {self.user_response}"
