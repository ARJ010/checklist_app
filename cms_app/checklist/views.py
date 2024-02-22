from django.shortcuts import render, redirect
from .forms import ChecklistQuestionForm
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Checklist, ChecklistQuestion

# Create your views here.

def employee_group_required(user):
    """Check if the user belongs to the 'Admin' group."""
    return user.groups.filter(name='Admin').exists()


@login_required
@user_passes_test(employee_group_required)
def add_checklist_question(request):
    if request.method == 'POST':
        form = ChecklistQuestionForm(request.POST)
        if form.is_valid():
            action = request.POST.get('action')  # Get the value of the clicked button
            if action == 'add_question':
                form.save()
            elif action == 'submit':
                # Save the form data even if the user hasn't clicked "Add Question"
                form.save()
                # Perform final submission logic
                # You can redirect the user to a different page or display a success message
                return redirect('manager_index')  # Redirect to a success page
            return redirect('view_checklist')  # Redirect to the same page after successful submission
    else:
        form = ChecklistQuestionForm()
    return render(request, 'checklist/addchecklist.html', {'form': form})


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