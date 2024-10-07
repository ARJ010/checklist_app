from django.db import models
from django.contrib.auth.models import User
from checklist.models import Checklist
from django.db.models.signals import post_delete
from django.dispatch import receiver

# Create your models here.

class Procedure(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Submitted', 'Submitted'),
        ('Processing', 'Processing'),
        ('Returned', 'Returned'),
        ('Reviewed', 'Reviewed'),
        ('Deleted', 'Deleted'),
    ]

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    client_name = models.CharField(max_length=255)
    data_path = models.CharField(max_length=255)
    checklist = models.ForeignKey(Checklist, on_delete=models.PROTECT)
    date_created = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Pending')
    checker = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='checked_procedures')
    return_count = models.PositiveIntegerField(default=0)
    final_submission_date = models.DateTimeField(null=True, blank=True)
    returned_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Procedure {self.id} - {self.client_name} - {self.status} - {self.return_count}"


@receiver(post_delete, sender=User)
def delete_pending_procedures(sender, instance, **kwargs):
    """
    When a User is deleted, only delete their pending procedures.
    """
    # Delete procedures associated with the deleted user that are in 'Pending' status
    Procedure.objects.filter(user=instance, status='Pending').delete()