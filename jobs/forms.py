from django import forms  # Import the forms module
from .models import Job, SavedSearch  # Import the Job and SavedSearch models


class JobForm(forms.ModelForm):
    """
    Form for creating and editing job listings.
    """

    class Meta:
        model = Job  # Associate with the Job model
        fields = [
            'title',
            'description',
            'location',
            'salary',
            'industry',
            'image',
        ]  # Specify the fields to include


class SavedSearchForm(forms.ModelForm):
    """
    Form for saving search queries.
    """

    class Meta:
        model = SavedSearch  # Associate with the SavedSearch model
        fields = ['query', 'industry']  # Specify the fields to include
