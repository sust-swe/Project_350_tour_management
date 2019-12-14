from django import forms
from .models import Guide, GuideAvailable
from homepage.models import City
from homepage.base import *
from .first_views import load_flw_from_month, load_flw_to_month, load_flw_from_day, load_flw_to_day, load_flw_to_year


class CreateGuideForm(forms.ModelForm):
    class Meta:
        model = Guide
        exclude = ['user_detail']
        labels = {"img": "Photo"}
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["city"].queryset = City.objects.none()
        if "country" in self.data:
            country = int(self.data.get("country"))
            self.fields["city"].queryset = City.objects.filter(country_id=country)
        elif self.instance.pk:
            country = self.instance.country
            self.fields["city"].queryset = City.objects.filter(country=country)


class GuideAvailableForm(forms.ModelForm):
    class Meta:
        model = GuideAvailable
        fields = '__all__'
        

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
