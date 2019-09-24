from django.shortcuts import render, HttpResponse
from django import views
from .forms import SearchRestaurantForm
from homepage.models import City
from restaurant.models import Restaurant

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


def load_city(request):
    country_id = int(request.GET.get('country'))
    cities = City.objects.filter(country_id=country_id)
    # print(cities)
    return render(request, 'ajax_city.html', {'cities': cities})


def load_date(request):
    month_id = int(request.GET.get('month', None))
    var = 0
    if month_id == 1 or month_id == 3 or month_id == 5 or month_id == 7 or month_id == 8 or month_id == 10 or month_id == 12:
        var = [o for o in range(1, 32)]
    elif month_id == 2:
        var = [o for o in range(1, 29)]
    else:
        var = [o for o in range(1, 31)]

    return render(request, 'load_date.html', {'var': var})
