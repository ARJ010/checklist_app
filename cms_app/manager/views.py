from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponseBadRequest
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User, Group
from .forms import RegisterForm
from .models import Employee

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

# You can use the same view for searching users

@login_required
@user_passes_test(employee_group_required)
def delete_users(request):
    if request.method == 'POST':
        # Get the list of user IDs from the POST request
        user_ids = request.POST.getlist('user_ids')
        user_type = request.POST.get('user_type')

        # Ensure user_ids is not empty
        if not user_ids:
            if user_type == 'user':
                return redirect(reverse('all_users') + '?user_type=user')
            elif user_type == 'checker':
                return redirect(reverse('all_users') + '?user_type=checker')

        try:
            # Convert user IDs from strings to integers
            user_ids_to_delete = list(map(int, user_ids))
            users_to_delete = User.objects.filter(id__in=user_ids_to_delete)
            print("Users to delete:", users_to_delete)
            users_to_delete.delete()
            # Redirect to the appropriate URL based on user_type
            if user_type == 'user':
                return redirect(reverse('all_users') + '?user_type=user')
            elif user_type == 'checker':
                return redirect(reverse('all_users') + '?user_type=checker')
        except Exception as e:
            # Print exception details for debugging
            print("Error deleting users:", e)
            return HttpResponseBadRequest("Failed to delete users: {}".format(str(e)))

    return HttpResponseBadRequest("Invalid request method. POST data expected.")