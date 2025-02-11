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
    """
    View to obtain an authentication token for API access.
    """
    if request.method == 'POST':  # Check if the request method is POST
        try:
            data = json.loads(request.body.decode('utf-8'))  # Parse the JSON request body
            username = data.get('username')  # Get the username from the request body
            password = data.get('password')  # Get the password from the request body
        except (json.JSONDecodeError, AttributeError):  # Handle JSON decoding errors
            return JsonResponse({'error': 'Invalid request body'}, status=400)  # Return an error response

        if not username or not password:  # Check if both username and password are provided
            return JsonResponse({'error': 'Please provide both username and password'}, status=400)  # Return an error response

        user = authenticate(username=username, password=password)  # Authenticate the user

        if user is not None:  # Check if the user is authenticated
            token, _ = Token.objects.get_or_create(user=user)  # Get or create a token for the user
            return JsonResponse({'token': token.key})  # Return the token
        else:
            return JsonResponse({'error': 'Invalid credentials'}, status=401)  # Return an error response

    else:
        return JsonResponse({'error': 'Only POST requests are allowed'}, status=405)  # Return an error response


def register(request):
    """
    View to register a new user.
    """
    if request.method == 'POST':  # Check if the request method is POST
        form = RegistrationForm(request.POST)  # Create a RegistrationForm instance with the POST data
        if form.is_valid():  # Check if the form is valid
            user = form.save()  # Save the form data to create a new user
            return redirect('login')  # Redirect to the login page
    else:
        form = RegistrationForm()  # Create an empty RegistrationForm instance
    return render(request, 'accounts/register.html', {'form': form})  # Render the registration form


def login_view(request):
    """
    View to log in an existing user.
    """
    if request.method == 'POST':  # Check if the request method is POST
        form = AuthenticationForm(request, data=request.POST)  # Create an AuthenticationForm instance with the POST data
        if form.is_valid():  # Check if the form is valid
            user = form.get_user()  # Get the user object from the form
            login(request, user)  # Log in the user
            UserActivity.objects.create(user=user, activity_type='login')  # Create a UserActivity record for the login
            return redirect('home')  # Redirect to the home page
    else:
        form = AuthenticationForm()  # Create an empty AuthenticationForm instance
    return render(request, 'accounts/login.html', {'form': form})  # Render the login form


@login_required  # Require the user to be logged in
def edit_employer_profile(request):
    """
    View to edit an employer profile.
    """
    try:
        employer_profile = request.user.employer  # Get the employer profile for the current user
    except Employer.DoesNotExist:  # Handle the case where the employer profile does not exist
        employer_profile = None  # Set employer_profile to None

    UserActivity.objects.create(user=request.user, activity_type='view_employer_profile')  # Create a UserActivity record for viewing the employer profile

    if request.method == 'POST':  # Check if the request method is POST
        form = EmployerProfileForm(request.POST, instance=employer_profile)  # Create an EmployerProfileForm instance with the POST data and the existing employer profile
        if form.is_valid():  # Check if the form is valid
            employer = form.save(commit=False)  # Save the form data to create a new employer profile
            employer.user = request.user  # Set the user for the employer profile
            employer.save()  # Save the employer profile
            return redirect('profile_success')  # Redirect to a success page
    else:
        form = EmployerProfileForm(instance=employer_profile)  # Create an EmployerProfileForm instance with the existing employer profile

    return render(request, 'accounts/edit_employer_profile.html', {'form': form, 'employer_profile': employer_profile})  # Render the edit employer profile form


@login_required  # Require the user to be logged in
def profile_success(request):
    """
    View to display a success message after profile update.
    """
    return render(request, 'accounts/profile_success.html')  # Render the profile success template


@login_required  # Require the user to be logged in
def edit_jobseeker_profile(request):
    """
    View to edit a job seeker profile.
    """
    try:
        jobseeker_profile = request.user.jobseeker  # Get the job seeker profile for the current user
    except JobSeeker.DoesNotExist:  # Handle the case where the job seeker profile does not exist
        jobseeker_profile = None  # Set jobseeker_profile to None

    UserActivity.objects.create(user=request.user, activity_type='view_jobseeker_profile')  # Create a UserActivity record for viewing the job seeker profile

    if request.method == 'POST':  # Check if the request method is POST
        form = JobSeekerProfileForm(request.POST, instance=jobseeker_profile)  # Create a JobSeekerProfileForm instance with the POST data and the existing job seeker profile
        if form.is_valid():  # Check if the form is valid
            jobseeker = form.save(commit=False)  # Save the form data to create a new job seeker profile
            jobseeker.user = request.user  # Set the user for the job seeker profile
            jobseeker.save()  # Save the job seeker profile
            return redirect('profile_success')  # Redirect to a success page
    else:
        form = JobSeekerProfileForm(instance=jobseeker_profile)  # Create a JobSeekerProfileForm instance with the existing job seeker profile

    return render(request, 'accounts/edit_jobseeker_profile.html', {'form': form, 'jobseeker_profile': jobseeker_profile})  # Render the edit job seeker profile form


def logout_view(request):
    """
    View to log out the current user.
    """
    logout(request)  # Log out the user
    return redirect('home')  # Redirect to the home page
