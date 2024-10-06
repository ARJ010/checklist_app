from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import ChecklistForm, ChecklistQuestionFormSet, SectionForm, SectionFormSet
from .models import Checklist, Section, ChecklistQuestion
from django.urls import reverse
from django.forms import formset_factory,inlineformset_factory
from django.contrib import messages
from django.core.paginator import Paginator

def employee_group_required(user):
    """Check if the user belongs to the 'Admin' group."""
    return user.groups.filter(name='Admin').exists()


@login_required
@user_passes_test(employee_group_required)
def checklist_detail(request):
    checklist_id = request.GET.get('checklist_id')
    checklist = get_object_or_404(Checklist, id=checklist_id)

    # Retrieve sections and their related questions
    sections = checklist.section_set.prefetch_related('checklistquestion_set').all()

    # Pagination logic - paginate by sections
    paginator = Paginator(sections, 1)  # Show 1 sections per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'checklist/checklist_details.html', {
        'checklist': checklist,
        'page_obj': page_obj,  # Paginated sections
    })



@login_required
@user_passes_test(employee_group_required)
def add_checklist(request):
    if request.method == 'POST':
        form = ChecklistForm(request.POST)
        if form.is_valid():
            checklist = form.save()
            checklist_name = checklist.name
            return redirect(reverse('add_section') + '?cname=' + checklist_name)
    else:
        form = ChecklistForm()
    return render(request, 'checklist/add_checklist.html', {'form': form})

@login_required
@user_passes_test(employee_group_required)
def add_section(request):
    checklist_name = request.GET.get('cname', None)
    if checklist_name is None:
        return redirect('error_page')

    checklist_instance = get_object_or_404(Checklist, name=checklist_name)

    # Handle POST request
    if request.method == 'POST':
        formset = SectionFormSet(request.POST, instance=checklist_instance)
        if formset.is_valid():
            formset.save()
            action = request.POST.get('action')
            if action == 'submit':
                return redirect(reverse('add_questions') + '?cname=' + checklist_name)
            elif action == 'save_and_add':
                return redirect(reverse('add_section') + '?cname=' + checklist_name + '#end')
    else:
        formset = SectionFormSet(instance=checklist_instance)

    return render(request, 'checklist/add_section.html', {'formset': formset, 'name': checklist_name})


@login_required
@user_passes_test(employee_group_required)
def add_checklist_question(request):
    checklist_name = request.GET.get('cname', None)
    if checklist_name is None:
        return redirect('error_page')

    checklist_instance = get_object_or_404(Checklist, name=checklist_name)

    if request.method == 'POST':
        formset = ChecklistQuestionFormSet(request.POST, instance=checklist_instance)
        for form in formset:
            form.fields['section'].queryset = Section.objects.filter(checklist=checklist_instance)  # Filter section choices
        if formset.is_valid():
            formset.save()
            action = request.POST.get('action')
            if action == 'submit':
                return redirect('all_checklist')
            elif action == 'save_and_add':
                return redirect(reverse('add_questions') + '?cname=' + checklist_name + '#end')
    else:
        formset = ChecklistQuestionFormSet(instance=checklist_instance)
        for form in formset:
            form.fields['section'].queryset = Section.objects.filter(checklist=checklist_instance)  # Filter section choices

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

    # Get the questions linked to the checklist
    questions = ChecklistQuestion.objects.filter(checklist=checklist)

    if request.method == 'POST':
        form = ChecklistForm(request.POST, instance=checklist)
        formset = ChecklistQuestionFormSet(request.POST, instance=checklist)

        # Pass checklist instance to each form in the formset
        for form in formset:
            form.fields['section'].queryset = Section.objects.filter(checklist=checklist)

        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()

            # Delete any empty questions after saving
            for question in formset:
                if question.cleaned_data.get('question_text', '').strip() == '':
                    question.instance.delete()

            # Redirect to either the same page to continue editing or exit to the checklist view
            action = request.POST.get('action')
            if action == 'save_and_edit':
                return redirect(reverse('edit_checklist') + '?checklist_id=' + str(checklist.id))
            else:
                return redirect(reverse('checklist_detail') + '?checklist_id=' + str(checklist.id))
    else:
        form = ChecklistForm(instance=checklist)
        formset = ChecklistQuestionFormSet(instance=checklist)

        # Pass checklist instance to each form in the formset
        for form in formset:
            form.fields['section'].queryset = Section.objects.filter(checklist=checklist)

    return render(request, 'checklist/edit_checklist.html', {
        'form': form,
        'formset': formset,
        'checklist': checklist,
    })




@login_required
@user_passes_test(employee_group_required)
def edit_section(request):
    checklist_id = request.GET.get('checklist_id')
    checklist = get_object_or_404(Checklist, id=checklist_id)

    # Get the sections linked to the checklist
    sections = Section.objects.filter(checklist=checklist)

    if request.method == 'POST':
        formset = SectionFormSet(request.POST, instance=checklist)

        if formset.is_valid():
            formset.save()

            # Redirect to either the same page to continue editing or exit to the checklist view
            action = request.POST.get('action')
            if action == 'save_and_edit':
                return redirect(reverse('edit_section') + '?checklist_id=' + str(checklist.id))
            else:
                return redirect(reverse('checklist_detail') + '?checklist_id=' + str(checklist.id))
    else:
        formset = SectionFormSet(instance=checklist)

    return render(request, 'checklist/edit_section.html', {
        'formset': formset,
        'checklist': checklist,
    })