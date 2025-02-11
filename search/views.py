from django.shortcuts import render, redirect, get_object_or_404  # Import necessary modules
from django.contrib.auth.decorators import login_required  # Import the login_required decorator
from jobs.models import Job  # Import the Job model
from .forms import SearchForm, SavedSearchForm  # Import the SearchForm and SavedSearchForm
from .models import SavedSearch  # Import the SavedSearch model

@login_required  # Require the user to be logged in
def save_search(request):
    """
    Saves a search query for a user.
    """
    if request.method == 'POST':  # Check if the request method is POST
        form = SavedSearchForm(
            request.POST
        )  # Create a SavedSearchForm instance with the POST data
        if form.is_valid():  # Check if the form is valid
            saved_search = form.save(
                commit=False
            )  # Save the form data to create a new saved search
            saved_search.user = request.user  # Set the user for the saved search
            saved_search.save()  # Save the saved search
            return redirect(
                'saved_searches'
            )  # Redirect to the saved searches page
    else:
        form = SavedSearchForm()  # Create an empty SavedSearchForm instance
    return render(
        request, 'search/save_search.html', {'form': form}
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
        request, 'search/saved_searches.html', {'saved_searches': saved_searches}
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
    return redirect(
        'saved_searches'
    )  # Redirect to the saved searches page


def search(request):
    """
    View to display search results.
    """
    form = SearchForm(request.GET)  # Create a SearchForm instance with the GET data
    jobs = Job.objects.all()  # Get all job objects

    if form.is_valid():  # Check if the form is valid
        query = form.cleaned_data.get('query')  # Get the search query from the form
        industry = form.cleaned_data.get('industry')  # Get the industry from the form

        if query:  # Check if a query is provided
            jobs = jobs.filter(
                title__icontains=query
            )  # Filter jobs by title if a query is provided

        if industry:  # Check if an industry is provided
            jobs = jobs.filter(
                industry__icontains=industry
            )  # Filter jobs by industry if an industry is provided

    return render(
        request, 'search/search.html', {'form': form, 'jobs': jobs}
    )  # Render the search template with the form and job results
