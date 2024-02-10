from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from .models import Employee

# Register your models here.



class CustomUserAdmin(UserAdmin):
    list_display = ('id', 'username', 'email', 'first_name', 'last_name', 'is_staff', 'is_active')
    search_fields = ('id', 'username', 'email', 'first_name', 'last_name')
    ordering = ('id',)

class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'first_name', 'last_name', 'user_photo', 'age', 'gender')

# Unregister the default User admin
admin.site.unregister(User)

# Register the custom User admin
admin.site.register(User, CustomUserAdmin)

admin.site.register(Employee, EmployeeAdmin)
