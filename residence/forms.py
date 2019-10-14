from .models import Residence, Space, SpaceAvailable
from homepage.base import *
from .views_1 import load_flw_to_day, load_flw_from_day, load_flw_from_month, load_flw_to_month, load_flw_to_year


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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        year_choice = [("", "------------")]
        for i in range(datetime.today().year, datetime.today().year+5):
            year_choice += [(i, str(i))]
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

        if 'from_year' in self.data:
            from_month = int(self.data['from_month'])
            from_year = int(self.data['from_year'])
            from_day = int(self.data['from_day'])
            to_day = int(self.data['to_day'])
            to_month = int(self.data['to_month'])
            to_year = int(self.data['to_year'])

            self.fields['from_month'] = forms.ChoiceField(
                choices=load_flw_from_month(from_year))
            self.fields['from_day'] = forms.ChoiceField(
                choices=load_flw_from_day(from_year, from_month))
            self.fields['to_year'] = forms.ChoiceField(
                choices=load_flw_to_year(from_year))
            self.fields['to_month'] = forms.ChoiceField(
                choices=load_flw_to_month(from_year, to_year, from_month))
            self.fields['to_day'] = forms.ChoiceField(choices=load_flw_to_day(
                from_year, to_year, from_month, to_month, from_day))


class SpaceBookForm(forms.Form):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        year_choice = [("", "------------")]
        for i in range(datetime.today().year, datetime.today().year+5):
            year_choice += [(i, str(i))]
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

        if 'from_year' in self.data:
            from_month = int(self.data['from_month'])
            from_year = int(self.data['from_year'])
            from_day = int(self.data['from_day'])
            to_day = int(self.data['to_day'])
            to_month = int(self.data['to_month'])
            to_year = int(self.data['to_year'])

            self.fields['from_month'] = forms.ChoiceField(
                choices=load_flw_from_month(from_year))
            self.fields['from_day'] = forms.ChoiceField(
                choices=load_flw_from_day(from_year, from_month))
            self.fields['to_year'] = forms.ChoiceField(
                choices=load_flw_to_year(from_year))
            self.fields['to_month'] = forms.ChoiceField(
                choices=load_flw_to_month(from_year, to_year, from_month))
            self.fields['to_day'] = forms.ChoiceField(choices=load_flw_to_day(
                from_year, to_year, from_month, to_month, from_day))
