from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.contrib.auth.models import Group
from .forms import LoginForm

def login_view(request):
    form = LoginForm()

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                next_url = request.GET.get('next', None)
                if next_url:
                    return redirect(next_url)
                else:
                    # Define group to URL mapping
                    group_redirects = {
                        'Admin': 'manager_index',
                        'Checkers': 'checker_index',
                        'Users': 'user_index'
                    }

                    user_groups = user.groups.all()
                    for group_name, redirect_url in group_redirects.items():
                        if user_groups.filter(name=group_name).exists():
                            return redirect(reverse(redirect_url) + '?user_id=' + str(user.id))

                    # If user does not belong to any expected group, show an error or handle accordingly
                    return render(request, 'authenticate/login.html', {'form': form, 'error': 'User does not belong to any valid group.'})

            else:
                return render(request, 'authenticate/login.html', {'form': form, 'error': 'Invalid username or password'})

    return render(request, 'authenticate/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')
