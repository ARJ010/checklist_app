# checker/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import Group
from django.contrib.auth.models import User, Group
from django.core.paginator import Paginator
from django.urls import reverse
from django.forms import modelformset_factory
from django.db import transaction

from django.db.models import Q

from user.models import Procedure
from checklist.models import ChecklistQuestion

from .forms import ProcedureForm, CheckerProcedureResponseForm
from .models import ProcedureResponse


# Create your views here.    

def checkers_group_required(user):
    """Check if the user belongs to the 'Checkers' group."""
    return user.groups.filter(name='Checkers').exists()

@login_required
@user_passes_test(checkers_group_required)
def my_protected_view(request):
    user = request.user
    return render(request, 'checker/index.html',{'user':user})


@login_required
@user_passes_test(checkers_group_required)
def all_procedures(request):
    user = request.user
    procedures = Procedure.objects.filter(status='Submitted', return_count=0)

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
    
    return render(request, 'checker/all_process.html', {'page_obj': page_obj, 'user': user})


@login_required
@user_passes_test(checkers_group_required)
def proceed_procedure(request, procedure_id):
    checker_user = request.user

    with transaction.atomic():
        # Lock the procedure row for update
        procedure = Procedure.objects.select_for_update().get(id=procedure_id)

        # Check if the procedure is already being processed
        if procedure.status != 'Submitted' or procedure.checker is not None:
            # Redirect or show an error message if already processed
            return redirect('all_procedures')

        # Update the procedure's status and checker
        procedure.checker = checker_user
        procedure.status = 'Processing'
        procedure.save()

    checklist = procedure.checklist
    checklist_questions = ChecklistQuestion.objects.filter(checklist=checklist)

    if request.method == 'POST':
        form = ProcedureForm(request.POST, checklist_questions=checklist_questions)
        if form.is_valid():
            for question in checklist_questions:
                response, created = ProcedureResponse.objects.get_or_create(
                    procedure=procedure,
                    question=question
                )
                response.response = form.cleaned_data.get(f"question_{question.pk}")
                response.remarks = form.cleaned_data.get(f"remarks_{question.pk}")
                response.save()

            return redirect('my_procedures')
    else:
        initial_data = {}
        for question in checklist_questions:
            response = ProcedureResponse.objects.filter(procedure=procedure, question=question).first()
            initial_data[f"question_{question.pk}"] = response.response if response else ""
            initial_data[f"remarks_{question.pk}"] = response.remarks if response else ""
        form = ProcedureForm(initial=initial_data, checklist_questions=checklist_questions)

    return render(request, 'checker/procedureform.html', {
        'form': form,
        'user': checker_user,
        'procedure_id': procedure_id,
        'checklist_name': checklist.name
    })





@login_required
@user_passes_test(checkers_group_required)
def view_response(request, procedure_id):
    procedure = get_object_or_404(Procedure, id=procedure_id)
    responses = ProcedureResponse.objects.filter(procedure=procedure)
    
    return render(request, 'checker/view_response.html', {
        'procedure': procedure,
        'responses': responses
    })

@login_required
@user_passes_test(checkers_group_required)
def edit_responses(request, procedure_id):
    procedure = get_object_or_404(Procedure, id=procedure_id)
    responses = ProcedureResponse.objects.filter(procedure=procedure)
    
    ProcedureResponseFormSet = modelformset_factory(
        ProcedureResponse, 
        form=CheckerProcedureResponseForm,  # Use the custom form here
        extra=0
    )
    formset = ProcedureResponseFormSet(queryset=responses)
    
    if request.method == 'POST':
        formset = ProcedureResponseFormSet(request.POST, queryset=responses)
        if formset.is_valid():
            formset.save()
            return redirect(reverse('view_response', args=[procedure_id]))
    
    return render(request, 'checker/edit_responses.html', {
        'procedure': procedure,
        'formset': formset
    })



@login_required
@user_passes_test(checkers_group_required)
def cancel_procedure(request, procedure_id):
    user = request.user
    procedure = get_object_or_404(Procedure, id=procedure_id)
    # Update procedure status to 'Submitted'
    procedure.status = 'Submitted'
    procedure.checker = None
    procedure.save()
    return redirect('all_procedures')  # Redirect to list of procedures


@login_required
@user_passes_test(checkers_group_required)
def my_procedures(request):
    user = request.user
    procedures = Procedure.objects.filter(status='Processing', checker=user)

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
    
    return render(request, 'checker/my_process.html', {'page_obj': page_obj, 'user': user})




from django.utils import timezone

@login_required
@user_passes_test(checkers_group_required)
def return_procedure(request, procedure_id):
    status = request.GET.get('status')
    procedure = get_object_or_404(Procedure, id=procedure_id)
    procedure.return_count += 1
    procedure.returned_date = timezone.now()
    procedure.status = 'Returned'
    procedure.save()
    if status == 'my_process':
        return redirect('my_procedures')
    return redirect('checkers_returned')


@login_required
@user_passes_test(checkers_group_required)
def checkers_returned(request):
    user = request.user
    procedures = Procedure.objects.filter(
    Q(checker=user) &
    (Q(status='Returned') | Q(return_count__gt=0)) &
    ~Q(status='Reviewed')
)


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
    
    return render(request, 'checker/returned.html', {'page_obj': page_obj, 'user': user})


@login_required
@user_passes_test(checkers_group_required)
def final_submit(request, procedure_id):
    procedure = get_object_or_404(Procedure, id=procedure_id)
    procedure.final_submission_date = timezone.now()
    procedure.status = 'Reviewed'
    procedure.save()
    if procedure.return_count == 0:
        return redirect('my_procedures')
    return redirect('checkers_returned')


@login_required
@user_passes_test(checkers_group_required)
def checkers_history(request):
    user = request.user
    procedures = Procedure.objects.filter(
    Q(checker=user) & Q(status='Reviewed')
)


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
    
    return render(request, 'checker/checkers_history.html', {'page_obj': page_obj, 'user': user})