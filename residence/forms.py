from django import forms
from .models import Residence, Space, SpaceAvailable


class ResidenceForm(forms.ModelForm):

    class Meta:
        model = Residence
        exclude = ['user_detail']


class SpaceForm(forms.ModelForm):
    class Meta:
        model = Space
        exclude = ['residence']


class SpaceAvailableForm(forms.ModelForm):
    class Meta:
        model = SpaceAvailable
        fields = '__all__'
