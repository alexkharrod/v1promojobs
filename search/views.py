from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from jobs.models import Job
from .forms import SearchForm, SavedSearchForm
from .models import SavedSearch

@login_required
def save_search(request):
    if request.method == 'POST':
        form = SavedSearchForm(request.POST)
        if form.is_valid():
            saved_search = form.save(commit=False)
            saved_search.user = request.user
            saved_search.save()
            return redirect('saved_searches')
    else:
        form = SavedSearchForm()
    return render(request, 'search/save_search.html', {'form': form})

@login_required
def saved_searches(request):
    saved_searches = SavedSearch.objects.filter(user=request.user)
    return render(request, 'search/saved_searches.html', {'saved_searches': saved_searches})

@login_required
def delete_saved_search(request, pk):
    saved_search = get_object_or_404(SavedSearch, pk=pk, user=request.user)
    saved_search.delete()
    return redirect('saved_searches')

def search(request):
    form = SearchForm(request.GET)
    jobs = Job.objects.all()

    if form.is_valid():
        query = form.cleaned_data.get('query')
        industry = form.cleaned_data.get('industry')

        if query:
            jobs = jobs.filter(title__icontains=query)

        if industry:
            jobs = jobs.filter(industry__icontains=industry)

    return render(request, 'search/search.html', {'form': form, 'jobs': jobs})
