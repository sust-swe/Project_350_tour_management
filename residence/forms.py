from django import forms
from .models import Residence, Space, SpaceAvailable
from homepage.models import Country, City


class ResidenceForm(forms.ModelForm):

    class Meta:
        model = Residence
        exclude = ['user_detail']

    def __init__(self, *args, **kwargs):
        super(ResidenceForm, self).__init__(*args, **kwargs)

        self.fields['country'].queryset = Country.objects.all()
        self.fields['city'].queryset = City.objects.none()

        if 'country' in self.data:
            country_id = int(self.data.get('country'))
            self.fields['city'].queryset = City.objects.filter(
                country_id=country_id).order_by('city')
        elif self.instance.pk:
            self.fields['city'].queryset = self.instance.country.city_set.order_by(
                'city')


class SpaceForm(forms.ModelForm):
    class Meta:
        model = Space
        exclude = ['residence']


class SpaceAvailabilityForm(forms.ModelForm):
    class Meta:
        model = SpaceAvailable
        exclude = ['space']
