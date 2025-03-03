from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Employer
from .forms import EmployerForm  # Import the EmployerForm
from core.models import UserActivity

@login_required  # Require the user to be logged in
def employer_profile_create(request):
    """
    View to create a new employer profile.
    """
    if request.method == 'POST':  # Check if the request method is POST
        form = EmployerForm(
            request.POST, request.FILES
        )  # Create an EmployerForm instance with the POST data and files
        if form.is_valid():  # Check if the form is valid
            employer = form.save(
                commit=False
            )  # Save the form data to create a new employer profile
            employer.user = request.user  # Set the user for the employer profile
            employer.save()  # Save the employer profile
            return redirect(
                'employer_profile_detail', pk=employer.pk
            )  # Redirect to the employer profile detail page
    else:
        form = EmployerForm()  # Create an empty EmployerForm instance
    return render(
        request, 'employers/employer_profile_create.html', {'form': form}
    )  # Render the employer profile create template


@login_required  # Require the user to be logged in
def employer_profile_edit(request, pk):
    """
    View to edit an existing employer profile.
    """
    employer = get_object_or_404(
        Employer, pk=pk, user=request.user
    )  # Get the employer object or return a 404 error if not found
    if request.method == 'POST':  # Check if the request method is POST
        form = EmployerForm(
            request.POST, request.FILES, instance=employer
        )  # Create an EmployerForm instance with the POST data, files, and the existing employer profile
        if form.is_valid():  # Check if the form is valid
            form.save()  # Save the form data to update the employer profile
            return redirect(
                'employer_profile_detail', pk=employer.pk
            )  # Redirect to the employer profile detail page
    else:
        form = EmployerForm(
            instance=employer
        )  # Create an EmployerForm instance with the existing employer profile
    return render(
        request,
        'employers/employer_profile_edit.html',
        {'form': form, 'employer': employer},
    )  # Render the employer profile edit template


def employer_profile_detail(request, pk):
    """
    Displays the details of a specific employer profile.
    """
    employer = get_object_or_404(
        Employer, pk=pk
    )  # Get the employer object or return a 404 error if not found
    if request.user.is_authenticated:
        UserActivity.objects.create(
            user=request.user, activity_type='employer_profile_view', details={'employer_id': employer.pk, 'employer_name': employer.company_name}
        )
    return render(
        request, 'employers/employer_profile_detail.html', {'employer': employer}
    )  # Render the employer profile detail template
