from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import Group
from django.contrib.auth.models import User, Group
from django.core.paginator import Paginator
from django.urls import reverse

from .models import Procedure
from .forms import ProcedureForm


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


@login_required
@user_passes_test(checkers_group_required)
def draft(request):
    user_id = request.GET.get('user_id')
    if user_id != str(request.user.id):
        return redirect('unauthorized')
    
    user = get_object_or_404(User, id=user_id)
    procedures = Procedure.objects.filter(user=user, status='Pending')

    search_client_name = request.GET.get('searchClientName')
    search_checklist = request.GET.get('searchChecklist')
    search_date = request.GET.get('searchDate')

    if search_client_name:
        procedures = procedures.filter(client_name__icontains=search_client_name)
    if search_checklist:
        procedures = procedures.filter(checklist__name__icontains=search_checklist)
    if search_date:
        procedures = procedures.filter(date_created__date=search_date)

    paginator = Paginator(procedures, 10)  # Show 10 procedures per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'user/draft.html', {'page_obj': page_obj, 'user': user})



@login_required
@user_passes_test(checkers_group_required)
def add_procedure(request):
    user_id = request.GET.get('user_id')
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        form = ProcedureForm(request.POST)
        if form.is_valid():
            procedure = form.save(commit=False)
            procedure.user = user
            procedure.save()
            return redirect(reverse('draft') + '?user_id=' + str(user.id))
    else:
        form = ProcedureForm()
    return render(request, 'user/add_procedure.html', {'form': form, 'user': user})

@login_required
@user_passes_test(checkers_group_required)
def submit_procedure(request):
    user_id = request.GET.get('user_id')
    user = get_object_or_404(User, id=user_id)
    procedure_id= request.GET.get('procedure_id')
    procedure = get_object_or_404(Procedure, id=procedure_id)
    # Update procedure status to 'Submitted'
    procedure.status = 'Submitted'
    procedure.save()
    return redirect(reverse('draft') + '?user_id=' + str(user.id))  # Redirect to list of procedures


@login_required
@user_passes_test(checkers_group_required)
def edit_procedure(request):
    user_id = request.GET.get('user_id')
    user = get_object_or_404(User, id=user_id)
    procedure_id = request.GET.get('procedure_id')
    procedure = get_object_or_404(Procedure, id=procedure_id)
    if request.method == 'POST':
        form = ProcedureForm(request.POST, instance=procedure)
        if form.is_valid():
            form.save()
            return redirect(reverse('draft') + '?user_id=' + str(user.id))
    else:
        form = ProcedureForm(instance=procedure)
    return render(request, 'user/edit_procedure.html', {'form': form})


@login_required
@user_passes_test(checkers_group_required)
def delete_procedure(request):
    user_id = request.GET.get('user_id')
    user = get_object_or_404(User, id=user_id)
    procedure_id = request.GET.get('procedure_id')
    procedure = get_object_or_404(Procedure, id=procedure_id)
    # Delete procedure from the database
    procedure.delete()
    return redirect(reverse('draft') + '?user_id=' + str(user.id))


@login_required
@user_passes_test(checkers_group_required)
def status(request):
    user_id = request.GET.get('user_id')
    user = get_object_or_404(User, id=user_id)
    procedures = Procedure.objects.filter(user=request.user, status='Submitted')

    search_client_name = request.GET.get('searchClientName')
    search_checklist = request.GET.get('searchChecklist')
    search_date = request.GET.get('searchDate')

    if search_client_name:
        procedures = procedures.filter(client_name__icontains=search_client_name)
    if search_checklist:
        procedures = procedures.filter(checklist__name__icontains=search_checklist)
    if search_date:
        procedures = procedures.filter(date_created__date=search_date)

    paginator = Paginator(procedures, 10)  # Show 10 procedures per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'user/status.html', {'page_obj': page_obj, 'user': user})

@login_required
@user_passes_test(checkers_group_required)
def returned(request):
    user_id = request.GET.get('user_id')
    user = get_object_or_404(User, id=user_id)
    procedures = Procedure.objects.filter(user=request.user, status='Returned')


    paginator = Paginator(procedures, 10)  # Show 10 procedures per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'user/returned.html', {'page_obj': page_obj, 'user': user})

@login_required
@user_passes_test(checkers_group_required)
def history(request):
    user_id = request.GET.get('user_id')
    user = get_object_or_404(User, id=user_id)
    procedures = Procedure.objects.filter(user=request.user, status='Reviewed')

    paginator = Paginator(procedures, 10)  # Show 10 procedures per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'user/history.html', {'page_obj': page_obj, 'user': user})
