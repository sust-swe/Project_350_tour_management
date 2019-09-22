from django import forms
from homepage.models import MyChoice, Country, City


class SearchRestaurantForm(forms.Form):
    name = forms.CharField(max_length=100, required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['country'] = forms.ChoiceField(
            choices=[(o.id, str(o)) for o in Country.objects.all()])
        self.fields['city'] = forms.ChoiceField(
            choices=[(o.id, str(o)) for o in City.objects.none()])

        if 'country' in self.data:
            country_id = int(self.data.get('country'))
