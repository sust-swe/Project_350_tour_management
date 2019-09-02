from django import forms
from .models import Residence, Space, SpaceAvailable


class ResidenceForm(forms.ModelForm):
    class Meta:
        model = Residence
        fields = ['name', 'mobile', 'description', 'img']


class SpaceForm(forms.ModelForm):
    class Meta:
        model = Space
        fields = '__all__'


class SpaceAvailableForm(forms.ModelForm):
    class Meta:
        model = SpaceAvailable
        fields = '__all__'
