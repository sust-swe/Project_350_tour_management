from django import forms
from .models import Guide, GuideAvailable


class GuideForm(forms.ModelForm):
    class Meta:
        model = Guide
        exclude = ['user_detail']


class GuideAvailableForm(forms.ModelForm):
    class Meta:
        model = GuideAvailable
        fields = '__all__'
