from django.shortcuts import render
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
        country_id = int(form.fields['country'].value())
        city_id = int(form.fields['country'].value())

        restaurants = Restaurant.objects.filter(
            country_id=country_id, city_id=country_id)
        context = {
            'restaurants': restaurants,
            'form': form,
        }
        return render(request, self.template_name, context)


def load_city(request):
    country_id = int(request.GET.get('country'))
    cities = City.objects.filter(country_id=country_id)
    print(cities)
    return render(request, 'ajax_city.html', {'cities': cities})
