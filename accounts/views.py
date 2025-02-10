from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Employer, JobSeeker, User
from .forms import EmployerProfileForm, JobSeekerProfileForm, RegistrationForm  # Import RegistrationForm
from django.contrib.auth import login, authenticate, logout  # Import authenticate and logout
from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('profile_success')
    else:
        form = RegistrationForm()
    return render(request, 'accounts/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')  # Redirect to home page
            else:
                return render(request, 'accounts/login.html', {'form': form, 'error': 'Invalid username or password'})
        else:
            return render(request, 'accounts/login.html', {'form': form, 'error': 'Invalid username or password'})
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})

@login_required
def logout_view(request):
    logout(request)
    return redirect('home')  # Redirect to home page

@login_required
@user_passes_test(lambda u: u.user_type == 'employer')
def edit_employer_profile(request):
    try:
        employer = request.user.employer
    except Employer.DoesNotExist:
        employer = Employer(user=request.user)

    if request.method == 'POST':
        form = EmployerProfileForm(request.POST, request.FILES, instance=employer)
        if form.is_valid():
            form.save()
            return redirect('profile_success')  # Replace with your success URL
    else:
        form = EmployerProfileForm(instance=employer)

    return render(request, 'accounts/edit_employer_profile.html', {'form': form})

@login_required
@user_passes_test(lambda u: u.user_type == 'jobseeker')
def edit_jobseeker_profile(request):
    try:
        jobseeker = request.user.jobseeker
    except JobSeeker.DoesNotExist:
        jobseeker = JobSeeker(user=request.user)

    if request.method == 'POST':
        form = JobSeekerProfileForm(request.POST, request.FILES, instance=jobseeker)
        if form.is_valid():
            form.save()
            return redirect('profile_success')  # Replace with your success URL
    else:
        form = JobSeekerProfileForm(instance=jobseeker)

    return render(request, 'accounts/edit_jobseeker_profile.html', {'form': form})

from django.urls import reverse

def profile_success(request):
    return render(request, 'accounts/profile_success.html', {'otp_url': reverse('two_factor:profile')})

class PasswordResetView(PasswordResetView):
    template_name = 'accounts/password_reset.html'
    email_template_name = 'accounts/password_reset_email.html'
    success_url = '/accounts/password_reset/done/'

class PasswordResetDoneView(PasswordResetDoneView):
    template_name = 'accounts/password_reset_done.html'

class PasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'accounts/password_reset_confirm.html'
    success_url = '/accounts/password_reset/complete/'

class PasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'accounts/password_reset_complete.html'
