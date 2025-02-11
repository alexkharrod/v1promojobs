from django import forms
from .models import Application

class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application  # Associate with the Application model
        fields = ['status']  # Specify the fields to include
