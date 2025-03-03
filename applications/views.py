from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Application
from jobs.models import Job
from accounts.models import JobSeeker
from django.shortcuts import render, redirect, get_object_or_404  # Import necessary modules
from django.contrib.auth.decorators import (
    login_required,
    user_passes_test,
)  # Import decorators for authentication and authorization
from .models import Application  # Import the Application model
from jobs.models import Job  # Import the Job model
from accounts.models import JobSeeker  # Import the JobSeeker model
from .forms import ApplicationForm  # Import the ApplicationForm
from core.models import UserActivity  # Import the UserActivity model


@login_required  # Require the user to be logged in
def apply_for_job(request, job_id):
    """
    Allows a job seeker to apply for a job.
    """
    job = get_object_or_404(
        Job, pk=job_id
    )  # Get the job object or return a 404 error if not found
    if request.user.user_type == 'jobseeker':  # Check if the user is a job seeker
        job_seeker = JobSeeker.objects.get(
            user=request.user
        )  # Get the job seeker profile for the current user
        Application.objects.create(
            job=job, job_seeker=job_seeker
        )  # Create a new application
        job.applications += 1  # Increment the application count for the job
        job.save()  # Save the job object
        UserActivity.objects.create(
            user=request.user, activity_type='application_submitted', details={'job_id': job.pk, 'job_title': job.title}
        )
        return redirect(
            'application_success'
        )  # Redirect to the application success page
    else:
        return redirect(
            'application_failure'
        )  # Redirect to the application failure page


@login_required  # Require the user to be logged in
@user_passes_test(
    lambda u: u.user_type == 'employer'
)  # Require the user to be an employer
def employer_applications(request, job_id):
    """
    Lists all applications for a specific job.
    """
    job = get_object_or_404(
        Job, pk=job_id
    )  # Get the job object or return a 404 error if not found
    applications = Application.objects.filter(
        job=job
    )  # Get all applications for the job
    return render(
        request,
        'applications/employer_applications.html',
        {'job': job, 'applications': applications},
    )  # Render the employer applications template


@login_required  # Require the user to be logged in
@user_passes_test(
    lambda u: u.user_type == 'employer'
)  # Require the user to be an employer
def application_detail(request, pk):
    """
    Displays a single application.
    """
    application = get_object_or_404(
        Application, pk=pk
    )  # Get the application object or return a 404 error if not found
    return render(
        request, 'applications/application_detail.html', {'application': application}
    )  # Render the application detail template


@login_required  # Require the user to be logged in
@user_passes_test(
    lambda u: u.user_type == 'employer'
)  # Require the user to be an employer
def update_application_status(request, pk):
    """
    Updates the status of an application.
    """
    application = get_object_or_404(
        Application, pk=pk
    )  # Get the application object or return a 404 error if not found
    if request.method == 'POST':  # Check if the request method is POST
        form = ApplicationForm(
            request.POST, instance=application
        )  # Create an ApplicationForm instance with the POST data and the existing application
        if form.is_valid():  # Check if the form is valid
            application = form.save()  # Save the form data to update the application
            return redirect(
                'application_detail', pk=application.pk
            )  # Redirect to the application detail page
    else:
        form = ApplicationForm(
            instance=application
        )  # Create an ApplicationForm instance with the existing application
    return render(
        request,
        'applications/update_application_status.html',
        {'form': form, 'application': application},
    )  # Render the update application status template
