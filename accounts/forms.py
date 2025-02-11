from django import forms
from django.contrib.auth.forms import (
    PasswordResetForm,
    SetPasswordForm,
    UserCreationForm,
)

from employers.models import Employer

from .models import JobSeeker, User
from django.contrib.auth.hashers import make_password

class RegistrationForm(forms.Form):
    username = forms.CharField(max_length=150, required=True)
    email = forms.EmailField(required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)
    password2 = forms.CharField(widget=forms.PasswordInput, label="Confirm Password", required=True)
    user_type = forms.ChoiceField(choices=User.USER_TYPE_CHOICES, required=True)

    def clean_password2(self):
        password = self.cleaned_data.get("password")
        password2 = self.cleaned_data.get("password2")
        if password != password2:
            raise forms.ValidationError("Passwords do not match")
        return password2

    def save(self):
        username = self.cleaned_data.get("username")
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")
        user_type = self.cleaned_data.get("user_type")

        user = User.objects.create(
            username=username,
            email=email,
            user_type=user_type,
        )
        user.password = make_password(password)
        user.save()
        return user


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
