from django import forms

from django import forms
from .models import SavedSearch

class SearchForm(forms.Form):
    query = forms.CharField(label='Search', required=False)
    industry = forms.CharField(label='Industry', required=False)

class SearchForm(forms.Form):
    """
    Form for searching jobs.
    """
    query = forms.CharField(
        label='Search', required=False
    )  # Field for the search query (optional)
    industry = forms.CharField(
        label='Industry', required=False
    )  # Field for the industry (optional)


class SavedSearchForm(forms.ModelForm):
    """
    Form for saving search queries.
    """
    class Meta:
        model = SavedSearch  # Associate with the SavedSearch model
        fields = ['query', 'industry']  # Specify the fields to include
