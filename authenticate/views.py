# accounts/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import Group

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        
        if user is not None:
            login(request, user)
            # Redirect users based on their group membership
            if Group.objects.get(name='Admin') in user.groups.all():
                return redirect('manager_index')
            elif Group.objects.get(name='Checkers') in user.groups.all():
                return redirect('checker_index')
            elif Group.objects.get(name='Users') in user.groups.all():
                return redirect('user_index')
            else:
                # Handle users not belonging to any group
                return render(request, 'authenticate/login.html', {'error_message': 'Invalid username or password'})
    else:
        return render(request, 'authenticate/login.html')
