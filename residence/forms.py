from .models import Residence, Space, SpaceAvailable
from homepage.base import *


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


class DateForm(forms.Form):
    number_of_space = forms.IntegerField(initial=1)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        year_choice = [("", "------------")]
        for i in range(datetime.today().year, datetime.today().year+5):
            year_choice += [(str(i), str(i))]
        self.fields['from_year'] = forms.ChoiceField(
            choices=year_choice, label="From Year")
        self.fields['from_month'] = forms.ChoiceField(
            choices=[("", "------------")], label="From Month")
        self.fields['from_day'] = forms.ChoiceField(
            choices=[("", "------------")], label="From Day")
        self.fields['to_year'] = forms.ChoiceField(
            choices=[("", "------------")], label='To Year')
        self.fields['to_month'] = forms.ChoiceField(
            choices=[("", "------------")], label='To Month')
        self.fields['to_day'] = forms.ChoiceField(
            choices=[("", "------------")], label='To Day')
