# accounts/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.models import Group

from .forms import LoginForm

# Create your views here.

def login_view(request):
    form = LoginForm()  # Instantiate the LoginForm

    if request.method == 'POST':
        form = LoginForm(request.POST)  # Bind the form with POST data
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                login(request, user)
                # Redirect users based on their group membership
                if Group.objects.get(name='Admin') in user.groups.all():
                    return redirect('manager_index')
                elif Group.objects.get(name='Checkers') in user.groups.all():
                    return redirect(reverse('checker_index') + '?user_id=' + str(user.id))
                elif Group.objects.get(name='Users') in user.groups.all():
                    return redirect(reverse('user_index') + '?user_id=' + str(user.id))
            else:
                # Invalid username or password
                return render(request, 'authenticate/login.html', {'form': form, 'error': 'Invalid username or password'})
    
    # If the request method is not POST or form is invalid, render the login form
    return render(request, 'authenticate/login.html', {'form': form})
    
def logout_view(request):
    logout(request)
    return redirect('login')

