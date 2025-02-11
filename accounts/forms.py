from django import forms
from django.contrib.auth.forms import (
    PasswordResetForm,
    SetPasswordForm,
    UserCreationForm,
)

from employers.models import Employer

from .models import JobSeeker, User


class RegistrationForm(UserCreationForm):
    password2 = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")

    class Meta:
        model = User
        fields = ("username", "email", "user_type")

    def clean_password2(self):
        password = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password != password2:
            raise forms.ValidationError("Passwords do not match")
        return password2


class EmployerProfileForm(forms.ModelForm):
    class Meta:
        model = Employer
        fields = ['company_name', 'company_description', 'website', 'logo']
        model = Employer
        fields = ["company_name", "company_description", "website", "logo"]


class JobSeekerProfileForm(forms.ModelForm):
    class Meta:
        model = JobSeeker
        fields = ['bio', 'resume', 'skills']


class PasswordResetForm(PasswordResetForm):
    pass


class SetPasswordForm(SetPasswordForm):
    pass
