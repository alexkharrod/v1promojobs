from django import forms
from .models import Job, SavedSearch

class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ['title', 'description', 'location', 'salary', 'industry', 'image']

class SavedSearchForm(forms.ModelForm):
    class Meta:
        model = SavedSearch
        fields = ['query', 'industry']
