from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from django.urls import reverse_lazy


# Create your views here.    

def checkers_group_required(user):
    """Check if the user belongs to the 'Checkers' group."""
    return user.groups.filter(name='Users').exists()

@login_required(login_url=reverse_lazy('login'))
@user_passes_test(checkers_group_required)
def my_protected_view(request):
    return render(request, 'user/index.html')


