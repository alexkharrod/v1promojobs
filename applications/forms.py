from django import forms
from .models import Application  # Import the Application model

class ApplicationForm(forms.ModelForm):
    """
    Form for updating the status of an application.
    """
    class Meta:
        model = Application
        fields = ['status']  # Only allow the status to be updated
