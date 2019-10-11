from django import forms
from homepage.models import MyChoice, Country, City
import datetime


class SearchRestaurantForm(forms.Form):
    name = forms.CharField(max_length=100, required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['country'] = forms.ChoiceField(
            choices=[(o.id, str(o)) for o in Country.objects.all()], required=False)
        self.fields['city'] = forms.ChoiceField(
            choices=[(o.id, str(o)) for o in City.objects.none()], required=False)

        if 'country' in self.data:
            try:
                country_id = int(self.data.get('country'))
                self.fields['city'] = forms.ChoiceField(
                    choices=[(o.id, str(o)) for o in City.objects.filter(country_id=country_id)], required=False)

            except (ValueError, TypeError):
                pass


class DateForm(forms.Form):
    year = forms.ChoiceField(choices=[(ch, ch) for ch in range(
        datetime.date.today().year, datetime.date.today().year+5
    )])

    month = forms.ChoiceField(choices=MyChoice.months)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['date'] = forms.ChoiceField(choices=[])

        if 'month' in self.data:
            month_id = self.data.get('month', None)
            if month_id == 1 or month_id == 3 or month_id == 5 or month_id == 7 or month_id == 8 or month_id == 10 or month_id == 12:
                self.fields['data'] = forms.ChoiceField(
                    choices=[o for o in range(1, 32)])
            elif month_id == 2:
                self.fields['data'] = forms.ChoiceField(
                    choices=[o for o in range(1, 29)])
            else:
                self.fields['data'] = forms.ChoiceField(
                    choices=[o for o in range(1, 31)])


          
