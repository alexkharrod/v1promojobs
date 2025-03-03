from django.contrib.auth.decorators import (
    login_required,  # Import the login_required decorator
)
from django.shortcuts import (  # Import necessary modules
    get_object_or_404,
    redirect,
    render,
)
from django_ratelimit.decorators import ratelimit
from rest_framework import generics
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)
from rest_framework.permissions import IsAuthenticated

from core.models import UserActivity  # Import the UserActivity model

from .forms import JobForm, SavedSearchForm  # Import the JobForm and SavedSearchForm
from .models import Job, SavedSearch  # Import the Job and SavedSearch models
from .serializers import JobSerializer


class JobListAPIView(generics.ListAPIView):
    queryset = Job.objects.all()
    serializer_class = JobSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]


class JobDetailAPIView(generics.RetrieveAPIView):
    queryset = Job.objects.all()
    serializer_class = JobSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]


@login_required  # Require the user to be logged in
def job_create(request):
    """
    View to create a new job listing.
    """
    if request.method == "POST":  # Check if the request method is POST
        form = JobForm(
            request.POST, request.FILES
        )  # Create a JobForm instance with the POST data and files
        if form.is_valid():  # Check if the form is valid
            job = form.save(
                commit=False
            )  # Save the form data to create a new job listing
            job.employer = request.user.employer  # Set the employer for the job listing
            job.save()  # Save the job listing
            return redirect("job_detail", pk=job.pk)  # Redirect to the job detail page
    else:
        form = JobForm()  # Create an empty JobForm instance
    return render(
        request, "jobs/job_create.html", {"form": form}
    )  # Render the job create template


@login_required  # Require the user to be logged in
def job_edit(request, pk):
    """
    View to edit an existing job listing.
    """
    job = get_object_or_404(
        Job, pk=pk
    )  # Get the job object or return a 404 error if not found
    if request.method == "POST":  # Check if the request method is POST
        form = JobForm(
            request.POST, request.FILES, instance=job
        )  # Create a JobForm instance with the POST data, files, and the existing job listing
        if form.is_valid():  # Check if the form is valid
            job = form.save()  # Save the form data to update the job listing
            return redirect("job_detail", pk=job.pk)  # Redirect to the job detail page
    else:
        form = JobForm(
            instance=job
        )  # Create a JobForm instance with the existing job listing
    return render(
        request, "jobs/job_edit.html", {"form": form, "job": job}
    )  # Render the job edit template


def job_list(request):
    """
    Lists all job listings based on search criteria.
    """
    query = request.GET.get("q")  # Get the search query from the request
    industry = request.GET.get("industry")  # Get the industry from the request
    jobs = Job.objects.all()  # Get all job objects

    if query:  # Check if a query is provided
        jobs = jobs.filter(
            title__icontains=query
        )  # Filter jobs by title if a query is provided

    if industry:  # Check if an industry is provided
        jobs = jobs.filter(
            industry=industry
        )  # Filter jobs by industry if an industry is provided

    if request.user.is_authenticated:  # Check if the user is authenticated
        search_details = {
            "query": query,
            "industry": industry,
        }  # Create a dictionary with the search details
        UserActivity.objects.create(
            user=request.user, activity_type="job_search", details=search_details
        )  # Create a UserActivity record for the job search

    return render(
        request, "jobs/job_list.html", {"jobs": jobs}
    )  # Render the job list template


@login_required  # Require the user to be logged in
def save_search(request):
    """
    Saves a search query for a user.
    """
    if request.method == "POST":  # Check if the request method is POST
        form = SavedSearchForm(
            request.POST
        )  # Create a SavedSearchForm instance with the POST data
        if form.is_valid():  # Check if the form is valid
            saved_search = form.save(
                commit=False
            )  # Save the form data to create a new saved search
            saved_search.user = request.user  # Set the user for the saved search
            saved_search.save()  # Save the saved search
            return redirect("saved_searches")  # Render the saved searches page
    else:
        form = SavedSearchForm()  # Create an empty SavedSearchForm instance
    return render(
        request, "jobs/save_search.html", {"form": form}
    )  # Render the save search template


@login_required  # Require the user to be logged in
def saved_searches(request):
    """
    Lists all saved searches for a user.
    """
    saved_searches = SavedSearch.objects.filter(
        user=request.user
    )  # Get all saved searches for the current user
    return render(
        request, "jobs/saved_searches.html", {"saved_searches": saved_searches}
    )  # Render the saved searches template


@login_required  # Require the user to be logged in
def delete_saved_search(request, pk):
    """
    Deletes a saved search.
    """
    saved_search = get_object_or_404(
        SavedSearch, pk=pk, user=request.user
    )  # Get the saved search object or return a 404 error if not found
    saved_search.delete()  # Delete the saved search
    return redirect("saved_searches")  # Render the saved searches page


def job_detail(request, pk):
    """
    Displays the details of a specific job.
    """
    job = get_object_or_404(
        Job, pk=pk
    )  # Get the job object or return a 404 error if not found
    job.views += 1  # Increment the view count for the job
    job.save()  # Save the job object
    if request.user.is_authenticated:
        UserActivity.objects.create(
            user=request.user,
            activity_type="job_view",
            details={"job_id": job.pk, "job_title": job.title},
        )
    return render(
        request, "jobs/job_detail.html", {"job": job}
    )  # Render the job detail template
