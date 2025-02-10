from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Job, SavedSearch
from .forms import JobForm

@login_required
def job_create(request):
    if request.method == 'POST':
        form = JobForm(request.POST, request.FILES)
        if form.is_valid():
            job = form.save(commit=False)
            job.employer = request.user.employer
            job.save()
            return redirect('job_detail', pk=job.pk)
    else:
        form = JobForm()
    return render(request, 'jobs/job_create.html', {'form': form})

@login_required
def job_edit(request, pk):
    job = get_object_or_404(Job, pk=pk)
    if request.method == 'POST':
        form = JobForm(request.POST, request.FILES, instance=job)
        if form.is_valid():
            job = form.save()
            return redirect('job_detail', pk=job.pk)
    else:
        form = JobForm(instance=job)
    return render(request, 'jobs/job_edit.html', {'form': form, 'job': job})

def job_list(request):
    query = request.GET.get('q')
    industry = request.GET.get('industry')
    jobs = Job.objects.all()

    if query:
        jobs = jobs.filter(title__icontains=query)

    if industry:
        jobs = jobs.filter(industry=industry)

    return render(request, 'jobs/job_list.html', {'jobs': jobs})

from django.contrib.auth.decorators import login_required
from .forms import SavedSearchForm

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
    return render(request, 'jobs/save_search.html', {'form': form})

@login_required
def saved_searches(request):
    saved_searches = SavedSearch.objects.filter(user=request.user)
    return render(request, 'jobs/saved_searches.html', {'saved_searches': saved_searches})

@login_required
def delete_saved_search(request, pk):
    saved_search = get_object_or_404(SavedSearch, pk=pk, user=request.user)
    saved_search.delete()
    return redirect('saved_searches')

def job_detail(request, pk):
    job = get_object_or_404(Job, pk=pk)
    return render(request, 'jobs/job_detail.html', {'job': job})
