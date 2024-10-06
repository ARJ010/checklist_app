from django.conf import settings
import os
import logging
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.http import HttpResponseBadRequest
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User, Group
from .forms import RegisterForm, UserProfileForm, UserEmployeeForm, ChangePasswordForm, ProcedureForm
from .models import Employee
from user.models import Procedure
from django.db.models import Sum
from django.core.paginator import Paginator
from django.db.models import Q
from checker.models import  ProcedureResponse

logger = logging.getLogger(__name__)

# Create your views here.


def employee_group_required(user):
    """Check if the user belongs to the 'Admin' group."""
    return user.groups.filter(name='Admin').exists()


@login_required
@user_passes_test(employee_group_required)
def my_protected_view(request):
    return render(request, 'manager/index.html')


@login_required
@user_passes_test(employee_group_required)
def register_user(request):
    form = RegisterForm()
    if request.method == 'POST':
        form = RegisterForm(request.POST, request.FILES)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user_type = request.GET.get('user_type')
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            user_photo = form.cleaned_data['user_photo']
            age = form.cleaned_data['age']
            gender = form.cleaned_data['gender']

            user = User.objects.create_user(
                username=username, email=email, password=password, first_name=first_name, last_name=last_name)

            group_name = 'Users' if user_type == 'user' else 'Checkers'
            try:
                group = Group.objects.get(name=group_name)
            except Group.DoesNotExist:
                group = Group.objects.create(name=group_name)
            user.groups.add(group)

            employee = Employee.objects.create(
                user=user, first_name=first_name, last_name=last_name, user_photo=user_photo, age=age, gender=gender)
            employee.save()

            if user_type == 'user':
                return redirect(reverse('all_users') + '?user_type=user')
            elif user_type == 'checker':
                return redirect(reverse('all_users') + '?user_type=checker')

    return render(request, 'manager/register.html', {'form': form})


@login_required
@user_passes_test(employee_group_required)
def all_users(request):
    user_type = request.GET.get('user_type')
    query = request.GET.get('qname')
    delete = request.GET.get('delete')

    group_name = 'Users' if user_type == 'user' else 'Checkers'
    try:
        users_group = Group.objects.get(name=group_name)
        all_users = Employee.objects.filter(user__groups=users_group)
        if query:
            all_users = all_users.filter(first_name__icontains=query) | all_users.filter(
                last_name__icontains=query)
        if delete:
            all_users = User.objects.filter(groups=users_group)
            return render(request, 'manager/all_users.html', {'all_users': all_users, 'query': query, 'delete': True})
    except Group.DoesNotExist:
        all_users = []

    return render(request, 'manager/all_users.html', {'all_users': all_users, 'query': query})


@login_required
@user_passes_test(employee_group_required)
def user_details(request):
    user_id = request.GET.get('user_id')
    user = get_object_or_404(User, id=user_id)

    total_created = 0
    total_proceeded = 0
    total_reviewed_user = 0
    total_reviewed = 0
    total_returns = 0
    successful_review_rate = 0
    successful_review_rate_user = 0

    # Check if the user is a creator (in 'Users' group)
    if user.groups.filter(name='Users').exists():
        created_procedures = Procedure.objects.filter(user=user)
        reviewed_procedures = Procedure.objects.filter(user=user,status='Reviewed')
        total_reviewed = reviewed_procedures.count()
        total_created = created_procedures.count()
        total_returns = created_procedures.aggregate(total=Sum('return_count'))['total'] or 0
        if total_reviewed > 0:
            successful_reviews = reviewed_procedures.filter(return_count=0).count()
            successful_review_rate_user = (successful_reviews / total_reviewed) * 100  # Successful review rate in percentage

    # Check if the user is a checker (in 'Checkers' group)
    if user.groups.filter(name='Checkers').exists():
        proceeded_procedure = Procedure.objects.filter(checker=user)
        reviewed_procedures = Procedure.objects.filter(checker=user,status='Reviewed')
        total_reviewed = reviewed_procedures.count()
        total_proceeded = proceeded_procedure.count()


        total_returns = reviewed_procedures.aggregate(total=Sum('return_count'))['total'] or 0
        if total_reviewed > 0:
            successful_reviews = reviewed_procedures.filter(return_count=0).count()
            successful_review_rate = (successful_reviews / total_reviewed) * 100  # Successful review rate in percentage

    context = {
        'user': user,
        'total_created': total_created,
        'total_proceeded': total_proceeded,
        'total_reviewed': total_reviewed,
        'total_returns': total_returns,
        'successful_review_rate': successful_review_rate,
        'successful_review_rate_user': successful_review_rate_user,
    }

    return render(request, 'manager/user-details.html', context)


@login_required
@user_passes_test(employee_group_required)
def delete_users(request):
    if request.method == 'POST':
        user_ids = request.POST.getlist('user_ids')
        user_type = request.POST.get('user_type')

        if not user_ids:
            if user_type == 'user':
                return redirect(reverse('all_users') + '?user_type=user')
            elif user_type == 'checker':
                return redirect(reverse('all_users') + '?user_type=checker')

        try:
            users_to_delete = User.objects.filter(id__in=user_ids)
            logger.info("Users to delete: %s", users_to_delete)

            for user in users_to_delete:
                delete_user_and_photo(user)

            success_message = "Users successfully deleted."
            messages.success(request, success_message)

            if user_type == 'user':
                return redirect(reverse('all_users') + '?user_type=user')
            elif user_type == 'checker':
                return redirect(reverse('all_users') + '?user_type=checker')
        except Exception as e:
            logger.exception("Error deleting users")
            error_message = "Failed to delete users: {}".format(str(e))
            messages.error(request, error_message)
            return HttpResponseBadRequest(error_message)

    return HttpResponseBadRequest("Invalid request method. POST data expected.")


@login_required
@user_passes_test(employee_group_required)
def delete_user(request):
    user_type = request.GET.get('user_type')
    user_id = request.GET.get('user_id')

    user = User.objects.get(id=user_id)
    delete_user_and_photo(user)
    success_message = "Users successfully deleted."
    messages.success(request, success_message)
    if user_type == 'user':
        return redirect(reverse('all_users') + '?user_type=user')
    elif user_type == 'checker':
        return redirect(reverse('all_users') + '?user_type=checker')


def delete_user_and_photo(user):
    """
    Delete the user along with their associated photo if exists.
    """
    try:
        if user.employee.user_photo:
            photo_path = os.path.join(
                settings.MEDIA_ROOT, str(user.employee.user_photo))
            if os.path.exists(photo_path):
                os.remove(photo_path)
    except Exception as e:
        logger.exception("Error deleting user photo")

    try:
        user.delete()
    except Exception as e:
        logger.exception("Error deleting user")


@login_required
@user_passes_test(employee_group_required)
def edit_user_profile(request):
    user_id = request.GET.get('user_id')
    user = get_object_or_404(User, id=user_id)
    try:
        employee = user.employee
    except Employee.DoesNotExist:
        employee = Employee(user=user)

    if request.method == 'POST':
        user_form = UserEmployeeForm(request.POST, instance=user)
        profile_form = UserProfileForm(
            request.POST, request.FILES, instance=employee)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()

            employee.first_name = user.first_name
            employee.last_name = user.last_name
            employee.save()

            # Check if the image field has been cleared
            if 'user_photo' in profile_form.cleaned_data and not profile_form.cleaned_data['user_photo']:
                print("User photo cleared, deleting old image.")
                # Delete the old image file
                if employee.user_photo:
                    photo_path = os.path.join(
                        settings.MEDIA_ROOT, str(employee.user_photo))
                    if os.path.exists(photo_path):
                        os.remove(photo_path)
                    # Clear the image path from the user model
                    employee.user_photo = None
                    employee.save()

            # messages.success(request, 'Your profile has been updated!')
            # Adjust as needed
            return redirect(reverse('user_details') + '?user_id=' + str(user.id))
    else:
        user_form = UserEmployeeForm(instance=user)
        profile_form = UserProfileForm(instance=employee)
    return render(request, 'manager/edit_profile.html', {'user_form': user_form, 'profile_form': profile_form})


@login_required
@user_passes_test(employee_group_required)
def change_password(request):
    user_id = request.GET.get('user_id')
    user = get_object_or_404(User, id=user_id)

    if request.method == 'POST':
        form = ChangePasswordForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            # messages.success(request, 'Password has been updated!')
            return redirect(reverse('user_details') + '?user_id=' + str(user.id))
    else:
        form = ChangePasswordForm(instance=user)
    
    return render(request, 'manager/change_password.html', {'form': form})


@login_required
@user_passes_test(employee_group_required)
def admin_history(request):
    procedures = Procedure.objects.filter(status='Reviewed').order_by('-final_submission_date')

    # Existing search fields
    search_client_name = request.GET.get('searchClientName')
    search_checklist = request.GET.get('searchChecklist')
    search_date = request.GET.get('searchDate')
    search_user = request.GET.get('searchUser')
    search_checker = request.GET.get('searchChecker')
    search_status = request.GET.get('searchStatus')

    # Filter by client name
    if search_client_name:
        procedures = procedures.filter(client_name__icontains=search_client_name)

    # Filter by checklist name
    if search_checklist:
        procedures = procedures.filter(checklist__name__icontains=search_checklist)

    # Filter by creation date
    if search_date:
        procedures = procedures.filter(date_created__date=search_date)

    # Filter by user
    if search_user:
        procedures = procedures.filter(user__username__icontains=search_user)

    # Filter by checker
    if search_checker:
        procedures = procedures.filter(checker__username__icontains=search_checker)

    # Filter by status
    if search_status:
        procedures = procedures.filter(status__icontains=search_status)

    paginator = Paginator(procedures, 10)  # Show 10 procedures per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'manager/admin_history.html', {'page_obj': page_obj })

@login_required
@user_passes_test(employee_group_required)
def admin_history_response(request, procedure_id):
    procedure = get_object_or_404(Procedure, id=procedure_id)
    responses = ProcedureResponse.objects.filter(procedure=procedure)
    
    return render(request, 'manager/history_response.html', {
        'procedure': procedure,
        'responses': responses
    })


@login_required
@user_passes_test(employee_group_required)
def admin_processing(request):
    procedures = Procedure.objects.filter(
    Q(status='Processing') | Q(status='Submitted') | Q(status='Returned')
).order_by('-final_submission_date')

    # Existing search fields
    search_client_name = request.GET.get('searchClientName')
    search_checklist = request.GET.get('searchChecklist')
    search_date = request.GET.get('searchDate')
    search_user = request.GET.get('searchUser')
    search_checker = request.GET.get('searchChecker')
    search_status = request.GET.get('searchStatus')

    # Filter by client name
    if search_client_name:
        procedures = procedures.filter(client_name__icontains=search_client_name)

    # Filter by checklist name
    if search_checklist:
        procedures = procedures.filter(checklist__name__icontains=search_checklist)

    # Filter by creation date
    if search_date:
        procedures = procedures.filter(date_created__date=search_date)

    # Filter by user
    if search_user:
        procedures = procedures.filter(user__username__icontains=search_user)

    # Filter by checker
    if search_checker:
        procedures = procedures.filter(checker__username__icontains=search_checker)

    # Filter by status
    if search_status:
        procedures = procedures.filter(status__icontains=search_status)


    paginator = Paginator(procedures, 10)  # Show 10 procedures per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'manager/admin_processing.html', {'page_obj': page_obj })

@login_required
@user_passes_test(employee_group_required)
def admin_procedure_edit(request, procedure_id):
    procedure = get_object_or_404(Procedure, id=procedure_id)

    if request.method == 'POST':
        form = ProcedureForm(request.POST, instance=procedure)
        if form.is_valid():
            form.save()
            return redirect(reverse('admin_processing'))
    else:
        form = ProcedureForm(instance=procedure)

    return render(request, 'manager/admin_edit_procedure.html', {'form': form})

@login_required
@user_passes_test(employee_group_required)
def procedure_details(request):
    total_created = Procedure.objects.count()  # Count all procedures
    total_reviewed = Procedure.objects.filter(status='Reviewed').count()  # Count all reviewed procedures
    total_pending = Procedure.objects.filter(status='Pending').count()  # Count all procedures pending review
    total_proceeded = Procedure.objects.filter(status='Processing').count()  # Count all proceeded procedures
    total_returns = Procedure.objects.filter(status='Returned').count() # return counts

    context = {
        'total_created': total_created,
        'total_reviewed': total_reviewed,
        'total_pending': total_pending,
        'total_returns': total_returns,
        'total_proceeded': total_proceeded
    }

    return render(request, 'manager/procedure.html', context)
