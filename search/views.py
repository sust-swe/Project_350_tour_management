from django.shortcuts import render, HttpResponse
from django import views
from .forms import SearchRestaurantForm, SpaceSearchForm
from homepage.models import City
from restaurant.models import Restaurant
from .first_view import load_city_choice, load_flw_from_day, load_flw_to_day, load_flw_from_month, load_flw_to_month, load_flw_to_year

# Create your views here.


class SearchRestaurant(views.View):
    template_name = 'search_restaurant.html'
    form_class = SearchRestaurantForm

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST or None)

        if form.is_valid():
            country_id = form.cleaned_data.get('country', None)
            city_id = form.cleaned_data.get('city', None)
            restaurant_name = form.cleaned_data.get('name', None)
            # print(country_id, city_id, restaurant_name, type(country_id))
            # print(Restaurant.objects.all())

            restaurants = Restaurant.objects.all()

            if country_id:
                restaurants = Restaurant.objects.filter(
                    country_id=country_id)
            # print(restaurants)
            if city_id:
                restaurants = restaurants.filter(city_id=int(city_id))
            # print(restaurants)
            if restaurant_name:
                restaurants = restaurants.filter(
                    name__contains=restaurant_name)
            # print(restaurants)

            return render(request, self.template_name, {'restaurants': restaurants, 'form': form})
        else:
            # print(form.as_table())
            return render(request, self.template_name, {'form': form})


class SearchSpace(views.View):
    space_type_idlate_name = "search_space.html"
    form_class = SpaceSearchForm

    def get(self, request):
        form = self.form_class()
        print('space search view')
        # print(form.as_table())
        return render(request, self.space_type_idlate_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST or None)
        if form.is_valid():
            space_n = int(form.cleaned_data['space_n'])
            person_n = int(form.cleaned_data['person_n'])
            year = int(form.cleaned_data['from_year'])
            month = int(form.cleaned_data['from_month'])
            day = int(form.cleaned_data['from_day'])
            from_date = date(year, month, day)
            year = int(form.cleaned_data['to_year'])
            month = form.cleaned_data['to_month']
            day = form.cleaned_data['to_day']
            to_date = date(year, month, day)
            country = int(form.cleaned_data['country'])
            city = int(form.cleaned_data['city'])
            max_rent = min_rent = residence = 0
            if form.cleaned_data.get('max_rent', None):
                max_rent = form.cleaned_data['max_rent']
            if form.cleaned_data.get('min_rent', None):
                min_rent = form.cleaned_data['min_rent']
            if form.cleaned_data.get('residence', None):
                residence_name = int(form.cleaned_data['residence'])

            context = search_space(from_date, to_date, city, person_n, space_n, max_rent=max_rent,
                                   min_rent=min_rent, residence=residence)

            return render(request, self.template_name, {'context': context})
