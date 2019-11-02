from django import forms
from homepage.models import MyChoice, Country, City
from homepage.base import *
from .first_view import load_city_choice, load_flw_from_day, load_flw_from_month, load_flw_to_day, load_flw_to_month, load_flw_to_year, load_residence_choice
from residence.models import Residence


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


class SpaceSearchForm(forms.Form):
    space_n = forms.ChoiceField(
        choices=[(i, str(i)) for i in range(1, 100)], label="Number of Space")
    person_n = forms.ChoiceField(
        choices=[(i, str(i)) for i in range(1, 100)], label="Person per Room")
    max_rent = forms.CharField(label="Maximal Rent", required=False)
    min_rent = forms.CharField(label="Minimal Rent", required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        today = date.today()
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

        country_choice = [("", "------------")]
        for ob in Country.objects.all():
            country_choice += [(ob.id, str(ob.name))]
        self.fields['country'] = forms.ChoiceField(choices=country_choice)

        self.fields['city'] = forms.ChoiceField(choices=[("", "------------")])
        if 'country' in self.data:
            country = int(self.data.get('country', None))
            self.fields['city'] = forms.ChoiceField(
                choices=load_city_choice(City, country))

        self.fields['residence'] = forms.ChoiceField(label="Residence", choices=[
            ("", "------------")], required=False)
        if 'city' in self.data:
            city = int(self.data['city'])
            self.fields['residence'] = forms.ChoiceField(
                label="Residence", choices=load_residence_choice(Residence, city), required=False)

        # print('init spacesearch     form')


class SearchGuideForm(forms.Form):
    max_rent = forms.CharField(label="Maximal Rent", required=False)
    min_rent = forms.CharField(label="Minimal Rent", required=False)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["gender"] = forms.ChoiceField(choices=[(1, "Male"), (2, "female")])
        
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
            
        country_choice = [("", "------------")]
        for ob in Country.objects.all():
            country_choice += [(ob.id, str(ob.name))]
        self.fields['country'] = forms.ChoiceField(choices=country_choice)
    
        self.fields['city'] = forms.ChoiceField(choices=[("", "------------")])
        if 'country' in self.data:
            country = int(self.data.get('country', None))
            self.fields['city'] = forms.ChoiceField(
                choices=load_city_choice(City, country))