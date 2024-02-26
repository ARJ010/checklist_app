from django.shortcuts import render, redirect, get_object_or_404
from .forms import ChecklistQuestionForm, ChecklistForm
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Checklist,ChecklistQuestion
from django.urls import reverse

def employee_group_required(user):
    """Check if the user belongs to the 'Admin' group."""
    return user.groups.filter(name='Admin').exists()

@login_required
@user_passes_test(employee_group_required)
def add_checklist(request):
    if request.method == 'POST':
        form = ChecklistForm(request.POST)
        if form.is_valid():
            checklist = form.save()
            checklist_name = checklist.name
            return redirect(reverse('add_questions') + '?cname=' + checklist_name)
    else:
        form = ChecklistForm()
    return render(request, 'checklist/add_checklist.html', {'form': form})

@login_required
@user_passes_test(employee_group_required)
def add_checklist_question(request):
    checklist_name = request.GET.get('cname', None)
    if checklist_name is None:
        # Handle the case where the checklist name is not provided
        return redirect('error_page')  # Redirect to an error page or handle it as per your requirement

    # Fetch the questions associated with the checklist
    questions = ChecklistQuestion.objects.filter(checklist__name=checklist_name)

    if request.method == 'POST':
        form = ChecklistQuestionForm(request.POST)
        if form.is_valid():
            # Fetch the Checklist instance corresponding to the checklist name
            checklist_instance = Checklist.objects.get(name=checklist_name)
            question = form.save(commit=False)
            question.checklist = checklist_instance  # Set the Checklist instance
            question.save()
            action = request.POST.get('action')
            if action == 'submit':
                return redirect('all_checklist')  # Redirect to a success page
            return redirect(reverse('add_questions') + '?cname=' + checklist_name)
    else:
        form = ChecklistQuestionForm()

    return render(request, 'checklist/add_checklist_questions.html', {'form': form, 'name': checklist_name, 'questions': questions})

@login_required
@user_passes_test(employee_group_required)
def all_checklist(request):
    query = request.GET.get('qname')
    delete = request.GET.get('delete')

    try:
        all_checklist = Checklist.objects.all()
        if query:
            all_checklist = all_checklist.filter(name__icontains=query)
        if delete:
            all_checklist = Checklist.objects.all()
            return render(request, 'checklist/all_checklist.html', {'all_checklist': all_checklist, 'query': query, 'delete': True})
    except all_checklist.DoesNotExist:
        all_checklist = []

    return render(request, 'checklist/all_checklist.html', {'all_checklist': all_checklist, 'query': query})


@login_required
@user_passes_test(employee_group_required)
def delete_checklist(request):
    if request.method == 'POST':
        checklist_ids = request.POST.getlist('checklist_ids')
        checklists_to_delete = Checklist.objects.filter(id__in=checklist_ids)

        # Handle checklist deletion
        deleted_checklists = []
        failed_deletions = []
        for checklist in checklists_to_delete:
            try:
                checklist.delete()
                deleted_checklists.append(checklist)
            except Exception as e:
                # Log or handle the error appropriately
                failed_deletions.append(checklist)

        if failed_deletions:
            # Handle failed deletions (e.g., show error message)
            pass

        # Redirect to the page displaying all checklists
        return redirect('all_checklist')

    # If the request method is not POST, return a GET request
    # This is to prevent accidental deletions via direct URL access
    return redirect('all_checklist')
