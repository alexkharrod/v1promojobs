from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Application
from jobs.models import Job
from accounts.models import JobSeeker
from .forms import ApplicationForm

@login_required
def apply_for_job(request, job_id):
    job = get_object_or_404(Job, pk=job_id)
    if request.user.user_type == 'jobseeker':
        job_seeker = JobSeeker.objects.get(user=request.user)
        Application.objects.create(job=job, job_seeker=job_seeker)
        return render(request, 'applications/application_success.html')
    else:
        return render(request, 'applications/application_failure.html')

@login_required
@user_passes_test(lambda u: u.user_type == 'employer')
def employer_applications(request, job_id):
    job = get_object_or_404(Job, pk=job_id)
    applications = Application.objects.filter(job=job)
    return render(request, 'applications/employer_applications.html', {'job': job, 'applications': applications})

@login_required
@user_passes_test(lambda u: u.user_type == 'employer')
def application_detail(request, pk):
    application = get_object_or_404(Application, pk=pk)
    return render(request, 'applications/application_detail.html', {'application': application})

@login_required
@user_passes_test(lambda u: u.user_type == 'employer')
def update_application_status(request, pk):
    application = get_object_or_404(Application, pk=pk)
    if request.method == 'POST':
        form = ApplicationForm(request.POST, instance=application)
        if form.is_valid():
            form.save()
            return redirect('application_detail', pk=application.pk)
    else:
        form = ApplicationForm(instance=application)
    return render(request, 'applications/update_application_status.html', {'form': form, 'application': application})
