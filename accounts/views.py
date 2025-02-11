from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from rest_framework.authtoken.models import Token
from django.views.decorators.csrf import csrf_exempt
import json
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from .forms import RegistrationForm, EmployerProfileForm, JobSeekerProfileForm
from employers.models import Employer
from accounts.models import JobSeeker
from core.models import UserActivity


@csrf_exempt
def obtain_auth_token(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))
            username = data.get('username')
            password = data.get('password')
        except (json.JSONDecodeError, AttributeError):
            return JsonResponse({'error': 'Invalid request body'}, status=400)

        if not username or not password:
            return JsonResponse({'error': 'Please provide both username and password'}, status=400)

        user = authenticate(username=username, password=password)

        if user is not None:
            token, _ = Token.objects.get_or_create(user=user)
            return JsonResponse({'token': token.key})
        else:
            return JsonResponse({'error': 'Invalid credentials'}, status=401)

    else:
        return JsonResponse({'error': 'Only POST requests are allowed'}, status=405)


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            return redirect('login')
    else:
        form = RegistrationForm()
    return render(request, 'accounts/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            UserActivity.objects.create(user=user, activity_type='login')
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})


@login_required
def edit_employer_profile(request):
    try:
        employer_profile = request.user.employer
    except Employer.DoesNotExist:
        employer_profile = None

    UserActivity.objects.create(user=request.user, activity_type='view_employer_profile')

    if request.method == 'POST':
        form = EmployerProfileForm(request.POST, instance=employer_profile)
        if form.is_valid():
            employer = form.save(commit=False)
            employer.user = request.user
            employer.save()
            return redirect('profile_success')  # Redirect to a success page
    else:
        form = EmployerProfileForm(instance=employer_profile)

    return render(request, 'accounts/edit_employer_profile.html', {'form': form, 'employer_profile': employer_profile})


@login_required
def profile_success(request):
    return render(request, 'accounts/profile_success.html')


@login_required
def edit_jobseeker_profile(request):
    try:
        jobseeker_profile = request.user.jobseeker
    except JobSeeker.DoesNotExist:
        jobseeker_profile = None

    UserActivity.objects.create(user=request.user, activity_type='view_jobseeker_profile')

    if request.method == 'POST':
        form = JobSeekerProfileForm(request.POST, instance=jobseeker_profile)
        if form.is_valid():
            jobseeker = form.save(commit=False)
            jobseeker.user = request.user
            jobseeker.save()
            return redirect('profile_success')  # Redirect to a success page
    else:
        form = JobSeekerProfileForm(instance=jobseeker_profile)

    return render(request, 'accounts/edit_jobseeker_profile.html', {'form': form, 'jobseeker_profile': jobseeker_profile})


def logout_view(request):
    logout(request)
    return redirect('home')
