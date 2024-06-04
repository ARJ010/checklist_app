#manager/models.py

from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    user_photo = models.ImageField(upload_to='static/images/user', blank=True)
    age = models.PositiveIntegerField(blank=True, null=True)
    gender = models.CharField(max_length=10, blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

