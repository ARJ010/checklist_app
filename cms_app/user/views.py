from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import Group
from django.contrib.auth.models import User, Group


# Create your views here.    

def checkers_group_required(user):
    """Check if the user belongs to the 'Checkers' group."""
    return user.groups.filter(name='Users').exists()

@login_required
@user_passes_test(checkers_group_required)
def my_protected_view(request):
    user_id = request.GET.get('user_id')
    user = get_object_or_404(User, id=user_id)
    return render(request, 'user/index.html',{'user':user})


