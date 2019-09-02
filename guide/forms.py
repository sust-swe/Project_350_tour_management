from django import forms
from .models import Guide, GuideAvailable


class GuideForm(forms.ModelForm):
    class Meta:
        model = Guide
        fields = ['name', 'mobile', 'description', 'img']


class GuideAvailableForm(forms.ModelForm):
    class Meta:
        model = GuideAvailable
        fields = '__all__'
