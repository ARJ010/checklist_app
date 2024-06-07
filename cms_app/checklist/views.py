from django.shortcuts import render, redirect, get_object_or_404
from .forms import ChecklistForm, ChecklistQuestionForm, ChecklistQuestionFormSet
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Checklist,ChecklistQuestion
from django.urls import reverse
from django.forms import formset_factory
from django.contrib import messages

def employee_group_required(user):
    """Check if the user belongs to the 'Admin' group."""
    return user.groups.filter(name='Admin').exists()

@login_required
@user_passes_test(employee_group_required)
def checklist_detail(request):
    checklist_id = request.GET.get('checklist_id')
    checklist = get_object_or_404(Checklist, id=checklist_id)
    return render(request, 'checklist/checklist_details.html', {'checklist': checklist})



@login_required
@user_passes_test(employee_group_required)
def add_checklist(request):
    if request.method == 'POST':
        form = ChecklistForm(request.POST)
        if form.is_valid():
            checklist = form.save()
            checklist_name = checklist.name
            # Redirect to add questions page after adding the checklist
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

    # Fetch the checklist instance
    checklist_instance = get_object_or_404(Checklist, name=checklist_name)

    if request.method == 'POST':
        formset = ChecklistQuestionFormSet(request.POST, instance=checklist_instance)
        if formset.is_valid():
            formset.save()
            action = request.POST.get('action')
            if action == 'submit':
                # Redirect to checklist detail page after saving and exiting
                return redirect(reverse('checklist_detail') + '?checklist_id=' + str(checklist_instance.id))
            return redirect(reverse('add_questions') + '?cname=' + checklist_name)
    else:
        formset = ChecklistQuestionFormSet(instance=checklist_instance)

    return render(request, 'checklist/add_checklist_questions.html', {'formset': formset, 'name': checklist_name})

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

        deleted_checklists = []
        failed_deletions = []
        for checklist in checklists_to_delete:
            try:
                checklist.delete()
                deleted_checklists.append(checklist)
            except Exception as e:
                failed_deletions.append(checklist)

        if deleted_checklists:
            messages.success(request, f'Successfully deleted {len(deleted_checklists)} checklist(s).')
        if failed_deletions:
            messages.error(request, f'Failed to delete {len(failed_deletions)} checklist(s).')

        return redirect('all_checklist')

    return redirect('all_checklist')

@login_required
@user_passes_test(employee_group_required)
def edit_checklist(request):
    checklist_id = request.GET.get('checklist_id')
    checklist = get_object_or_404(Checklist, id=checklist_id)

    if request.method == 'POST':
        form = ChecklistForm(request.POST, instance=checklist)
        formset = ChecklistQuestionFormSet(request.POST, instance=checklist)
        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()

            if request.POST.get('action') == 'save_and_edit':
                return redirect(reverse('edit_checklist') + '?checklist_id=' + str(checklist.id))
            else:
                return redirect(reverse('checklist_detail') + '?checklist_id=' + str(checklist.id))
    else:
        form = ChecklistForm(instance=checklist)
        formset = ChecklistQuestionFormSet(instance=checklist)

    return render(request, 'checklist/edit_checklist.html', {'form': form, 'formset': formset, 'checklist': checklist})
