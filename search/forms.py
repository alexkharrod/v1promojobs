from django import forms

from django import forms
from .models import SavedSearch

class SearchForm(forms.Form):
    query = forms.CharField(label='Search', required=False)
    industry = forms.CharField(label='Industry', required=False)

class SavedSearchForm(forms.ModelForm):
    class Meta:
        model = SavedSearch
        fields = ['query', 'industry']
