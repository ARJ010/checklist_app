from django.shortcuts import render, redirect
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

            # Create User
            user = User.objects.create_user(
                username=username, email=email, password=password, first_name=first_name, last_name=last_name)
            if user_type == 'user':
                user.groups.add(Group.objects.get(name='Users'))
            elif user_type == 'checker':
                user.groups.add(Group.objects.get(name='Checkers'))

            # Create Employee
            employee = Employee.objects.create(
                user=user, first_name=first_name, last_name=last_name, user_photo=user_photo, age=age, gender=gender)
            employee.save()

            # Redirect to login page after registration
            return redirect('login')

    return render(request, 'manager/register.html', {'form': form})


@login_required
@user_passes_test(employee_group_required)
def all_users(request):
    user_type = request.GET.get('user_type')
    if user_type == 'user':
        users_group = Group.objects.get(name='Users')
        all_users = Employee.objects.filter(user__groups=users_group)
        return render(request, 'manager/all_users.html', {'all_users': all_users})

    elif user_type == 'checker':
        users_group = Group.objects.get(name='Checkers')
        all_users = Employee.objects.filter(user__groups=users_group)
        return render(request, 'manager/all_users.html', {'all_users': all_users})


def search_users(request):
    user_type = request.GET.get('user_type')
    if user_type == 'user':
        query = request.GET.get('q')
        users_group = Group.objects.get(name='Users')
        all_users = Employee.objects.filter(first_name__icontains=query, user__groups=users_group) | Employee.objects.filter(
            last_name__icontains=query, user__groups=users_group)
        return render(request, 'manager/all_users.html', {'all_users': all_users, 'query': query})

    elif user_type == 'checker':
        query = request.GET.get('q')
        users_group = Group.objects.get(name='Checkers')
        all_users = Employee.objects.filter(first_name__icontains=query, user__groups=users_group) | Employee.objects.filter(
            last_name__icontains=query, user__groups=users_group)
        return render(request, 'manager/all_users.html', {'all_users': all_users, 'query': query})
