from django import forms  # Import the forms module
from django.contrib.auth.forms import (
    PasswordResetForm,
    SetPasswordForm,
    UserCreationForm,
)  # Import authentication forms

from employers.models import Employer  # Import the Employer model

from .models import JobSeeker, User  # Import the JobSeeker and User models
from django.contrib.auth.hashers import (
    make_password,
)  # Import the function to hash passwords


class RegistrationForm(forms.Form):
    """
    Form for user registration.
    """
    username = forms.CharField(
        max_length=150, required=True
    )  # Field for username (required)
    email = forms.EmailField(required=True)  # Field for email (required)
    password = forms.CharField(
        widget=forms.PasswordInput, required=True
    )  # Field for password (required)
    password2 = forms.CharField(
        widget=forms.PasswordInput, label="Confirm Password", required=True
    )  # Field to confirm password (required)
    user_type = forms.ChoiceField(
        choices=User.USER_TYPE_CHOICES, required=True
    )  # Field for user type (required)

    def clean_password2(self):
        """
        Validates that the password and confirm password fields match.
        """
        password = self.cleaned_data.get("password")  # Get the password
        password2 = self.cleaned_data.get("password2")  # Get the confirm password
        if password != password2:  # Check if passwords match
            raise forms.ValidationError(
                "Passwords do not match"
            )  # Raise validation error if they don't match
        return password2  # Return the confirm password

    def save(self):
        """
        Saves the new user to the database.
        """
        username = self.cleaned_data.get("username")  # Get the username
        email = self.cleaned_data.get("email")  # Get the email
        password = self.cleaned_data.get("password")  # Get the password
        user_type = self.cleaned_data.get("user_type")  # Get the user type

        user = User.objects.create(
            username=username, email=email, user_type=user_type
        )  # Create a new user
        user.password = make_password(
            password
        )  # Hash the password
        user.save()  # Save the user
        return user  # Return the user


class EmployerProfileForm(forms.ModelForm):
    """
    Form for creating and editing employer profiles.
    """
    class Meta:
        model = Employer  # Associate with the Employer model
        fields = [
            "company_name",
            "company_description",
            "website",
            "logo",
        ]  # Specify the fields to include
        model = Employer
        fields = ["company_name", "company_description", "website", "logo"]


class JobSeekerProfileForm(forms.ModelForm):
    """
    Form for creating and editing job seeker profiles.
    """
    class Meta:
        model = JobSeeker  # Associate with the JobSeeker model
        fields = ["bio", "resume", "skills"]  # Specify the fields to include


class PasswordResetForm(PasswordResetForm):
    """
    Custom password reset form.
    """
    pass


class SetPasswordForm(SetPasswordForm):
    """
    Custom set password form.
    """
    pass
