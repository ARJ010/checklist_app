from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.


class Employee(AbstractUser):
    employee_id = models.IntegerField(unique=True)

    EMPLOYEE_TYPES = [
        ('admin', 'Admin'),
        ('user', 'User'),
        ('checker', 'Checker'),
    ]
    employee_type = models.CharField(max_length=10, choices=EMPLOYEE_TYPES)

    # Specify custom related_name for groups and user_permissions fields
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        related_name='employees_groups',
        related_query_name='employee_group',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        related_name='employees_permissions',
        related_query_name='employee_permission',
    )

    def __str__(self):
        return self.username
