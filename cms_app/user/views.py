# user/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import Group
from django.contrib.auth.models import User, Group
from django.core.paginator import Paginator
from django.urls import reverse
from django.db.models import Q
from checker.models import  ProcedureResponse

from django.forms import modelformset_factory



from .models import Procedure
from .forms import ProcedureForm, UserProcedureResponseForm


# Create your views here.    

def users_group_required(user):
    """Check if the user belongs to the 'Checkers' group."""
    return user.groups.filter(name='Users').exists()

@login_required
@user_passes_test(users_group_required)
def user_index(request):
    user = request.user
    return render(request, 'user/index.html',{'user':user})


@login_required
@user_passes_test(users_group_required)
def draft(request):
    user = request.user
    procedures = Procedure.objects.filter(user=user, status='Pending').order_by('-date_created')

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
@user_passes_test(users_group_required)
def add_procedure(request):
    user = request.user
    if request.method == 'POST':
        form = ProcedureForm(request.POST)
        if form.is_valid():
            procedure = form.save(commit=False)
            procedure.user = user
            procedure.save()
            return redirect('draft')
    else:
        form = ProcedureForm()
    return render(request, 'user/add_procedure.html', {'form': form, 'user': user})

@login_required
@user_passes_test(users_group_required)
def submit_procedure(request, procedure_id):
    status = request.GET.get('status')
    procedure = get_object_or_404(Procedure, id=procedure_id)
    # Update procedure status to 'Submitted'
    procedure.status = 'Submitted'
    procedure.save()
    if status == 'draft':
        return redirect('draft')  # Redirect to list of procedures
    return redirect('returned')


@login_required
@user_passes_test(users_group_required)
def edit_procedure(request, procedure_id):
    status = request.GET.get('status')
    procedure = get_object_or_404(Procedure, id=procedure_id)
    if request.method == 'POST':
        form = ProcedureForm(request.POST, instance=procedure)
        if form.is_valid():
            form.save()
            if status == 'draft':
                return redirect('draft')
            return redirect('returned')
    else:
        form = ProcedureForm(instance=procedure)
    return render(request, 'user/edit_procedure.html', {'form': form, "status":status})


@login_required
@user_passes_test(users_group_required)
def delete_procedure(request, procedure_id):
    procedure = get_object_or_404(Procedure, id=procedure_id)
    # Delete procedure from the database
    procedure.delete()
    return redirect('trash')

@login_required
@user_passes_test(users_group_required)
def temp_delete_procedure(request, procedure_id):
    procedure = get_object_or_404(Procedure, id=procedure_id)
    # Delete procedure from the database
    procedure.status = 'Deleted'
    procedure.save()
    return redirect('draft')

@login_required
@user_passes_test(users_group_required)
def restore_procedure(request, procedure_id):
    procedure = get_object_or_404(Procedure, id=procedure_id)
    # Delete procedure from the database
    procedure.status = 'Pending'
    procedure.save()
    return redirect('trash')

@login_required
@user_passes_test(users_group_required)
def status(request):
    user = request.user
    procedures = Procedure.objects.filter(
    Q(user=request.user) &
    Q(return_count=0) &
    (Q(status='Submitted') | Q(status='Processing'))).order_by('-date_created')

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
@user_passes_test(users_group_required)
def trash(request):
    user = request.user
    procedures = Procedure.objects.filter(user=request.user, status='Deleted').order_by('-date_created')

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

    return render(request, 'user/trash.html', {'page_obj': page_obj, 'user': user})

@login_required
@user_passes_test(users_group_required)
def returned(request):
    user = request.user
    procedures = Procedure.objects.filter(Q(user=request.user) & (Q(status='Returned') | Q(return_count__gt=0)) & ~Q(status='Reviewed')).order_by('-returned_date')

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

    return render(request, 'user/returned.html', {'page_obj': page_obj, 'user': user})

@login_required
@user_passes_test(users_group_required)
def history(request):
    user = request.user
    procedures = Procedure.objects.filter(user=request.user, status='Reviewed').order_by('-final_submission_date')

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

    return render(request, 'user/history.html', {'page_obj': page_obj, 'user': user})


@login_required
@user_passes_test(users_group_required)
def user_view_responses(request, procedure_id):
    procedure = get_object_or_404(Procedure, id=procedure_id)
    responses = ProcedureResponse.objects.filter(procedure=procedure)
    
    return render(request, 'user/view_response.html', {
        'procedure': procedure,
        'responses': responses
    })

@login_required
@user_passes_test(users_group_required)
def user_edit_responses(request, procedure_id):
    procedure = get_object_or_404(Procedure, id=procedure_id)
    responses = ProcedureResponse.objects.filter(procedure=procedure)
    
    ProcedureResponseFormSet = modelformset_factory(
        ProcedureResponse, 
        form=UserProcedureResponseForm,  # Use the custom form here
        extra=0
    )
    formset = ProcedureResponseFormSet(queryset=responses)
    
    if request.method == 'POST':
        formset = ProcedureResponseFormSet(request.POST, queryset=responses)
        if formset.is_valid():
            formset.save()
            return redirect(reverse('user_view_responses', args=[procedure_id]))
    
    return render(request, 'user/edit_responses.html', {
        'procedure': procedure,
        'formset': formset
    })


@login_required
@user_passes_test(users_group_required)
def user_history_response(request, procedure_id):
    procedure = get_object_or_404(Procedure, id=procedure_id)
    responses = ProcedureResponse.objects.filter(procedure=procedure)
    
    return render(request, 'user/history_response.html', {
        'procedure': procedure,
        'responses': responses
    })