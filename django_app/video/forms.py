from django import forms


class SearchForm(forms.Form):
    query = forms.CharField()
    max_results = forms.IntegerField(required=False, min_value=1)
