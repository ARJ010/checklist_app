from django.conf import settings
import os,logging
from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponseBadRequest
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User, Group
from .forms import RegisterForm
from .models import Employee

logger = logging.getLogger(__name__)

# Create your views here.

def employee_group_required(user):
    """Check if the user belongs to the 'Admin' group."""
    return user.groups.filter(name='Admin').exists()

@login_required
@user_passes_test(employee_group_required)
def my_protected_view(request):
    return render(request, 'manager/index.html')

@login_required
@user_passes_test(employee_group_required)
def register_user(request):
    form = RegisterForm()
    if request.method == 'POST':
        form = RegisterForm(request.POST, request.FILES)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user_type = request.GET.get('user_type')
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            user_photo = form.cleaned_data['user_photo']
            age = form.cleaned_data['age']
            gender = form.cleaned_data['gender']

            user = User.objects.create_user(username=username, email=email, password=password, first_name=first_name, last_name=last_name)

            group_name = 'Users' if user_type == 'user' else 'Checkers'
            try:
                group = Group.objects.get(name=group_name)
            except Group.DoesNotExist:
                group = Group.objects.create(name=group_name)
            user.groups.add(group)

            employee = Employee.objects.create(user=user, first_name=first_name, last_name=last_name, user_photo=user_photo, age=age, gender=gender)
            employee.save()

            if user_type == 'user':
                return redirect(reverse('all_users') + '?user_type=user')
            elif user_type == 'checker':
                return redirect(reverse('all_users') + '?user_type=checker')

    return render(request, 'manager/register.html', {'form': form})

@login_required
@user_passes_test(employee_group_required)
def all_users(request):
    user_type = request.GET.get('user_type')
    query = request.GET.get('qname')
    delete = request.GET.get('delete')

    group_name = 'Users' if user_type == 'user' else 'Checkers'
    try:
        users_group = Group.objects.get(name=group_name)
        all_users = Employee.objects.filter(user__groups=users_group)
        if query:
            all_users = all_users.filter(first_name__icontains=query) | all_users.filter(last_name__icontains=query)
        if delete:
            all_users = User.objects.filter(groups=users_group)
            return render(request, 'manager/all_users.html', {'all_users': all_users, 'query': query , 'delete': True})
    except Group.DoesNotExist:
        all_users = []

    return render(request, 'manager/all_users.html', {'all_users': all_users, 'query': query})


@login_required
@user_passes_test(employee_group_required)
def user_details(request):
    user_id = request.GET.get('user_id')
    user = User.objects.get(id=user_id)
    return render(request, 'manager/user-details.html', {'user': user})


@login_required
@user_passes_test(employee_group_required)
def delete_users(request):
    if request.method == 'POST':
        user_ids = request.POST.getlist('user_ids')
        user_type = request.POST.get('user_type')

        if not user_ids:
            if user_type == 'user':
                return redirect(reverse('all_users') + '?user_type=user')
            elif user_type == 'checker':
                return redirect(reverse('all_users') + '?user_type=checker')

        try:
            users_to_delete = User.objects.filter(id__in=user_ids)
            logger.info("Users to delete: %s", users_to_delete)

            for user in users_to_delete:
                delete_user_and_photo(user)

            success_message = "Users successfully deleted."
            messages.success(request, success_message)

            if user_type == 'user':
                return redirect(reverse('all_users') + '?user_type=user')
            elif user_type == 'checker':
                return redirect(reverse('all_users') + '?user_type=checker')
        except Exception as e:
            logger.exception("Error deleting users")
            error_message = "Failed to delete users: {}".format(str(e))
            messages.error(request, error_message)
            return HttpResponseBadRequest(error_message)

    return HttpResponseBadRequest("Invalid request method. POST data expected.")
def delete_user_and_photo(user):
    """
    Delete the user along with their associated photo if exists.
    """
    try:
        if user.employee.user_photo:
            photo_path = os.path.join(settings.MEDIA_ROOT, str(user.employee.user_photo))
            if os.path.exists(photo_path):
                os.remove(photo_path)
    except Exception as e:
        logger.exception("Error deleting user photo")

    try:
        user.delete()
    except Exception as e:
        logger.exception("Error deleting user")