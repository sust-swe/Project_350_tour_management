from django import forms
from homepage.models import MyChoice, Country, City


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
