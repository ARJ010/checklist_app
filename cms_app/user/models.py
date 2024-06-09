from django.db import models
from django.contrib.auth.models import User
from checklist.models import Checklist

# Create your models here.

class Procedure(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Submitted', 'Submitted'),
        ('Returned', 'Returned'),
        ('Reviewed', 'Reviewed'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    client_name = models.CharField(max_length=255)
    data_path = models.CharField(max_length=255)
    checklist = models.ForeignKey(Checklist, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Pending')
    checker = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='checked_procedures')
    return_count = models.PositiveIntegerField(default=0)
    final_submission_date = models.DateTimeField(null=True, blank=True)
    returned_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Procedure {self.id} - {self.client_data}"
