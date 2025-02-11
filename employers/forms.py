from django import forms
from .models import Employer

class EmployerForm(forms.ModelForm):
    class Meta:
        model = Employer  # Associate with the Employer model
        fields = [
            'company_name',
            'company_description',
            'website',
            'logo'
        ]  # Specify the fields to include
