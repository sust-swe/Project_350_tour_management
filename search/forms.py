from django import forms
from homepage.models import MyChoice


class SearchRestaurantForm(forms.Form):
    name = forms.CharField(max_length=100, blank=True)
    city = forms.ChoiceField()