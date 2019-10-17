from homepage.base import *
from .views_1 import load_flw_from_month, load_flw_from_day, load_flw_to_year, load_flw_to_month, load_flw_to_day
from homepage.models import City


month_array = ['', 'January', 'February', 'March', 'April', 'May', 'June',
               'July', 'August', 'September', 'Octobor', 'November', 'December']


def load_from_month(request):
    #    print(type(request.GET)) <class 'django.http.request.QueryDict'>
    year = request.GET.get('year', None)
    month = []
    if year:
        year = int(year)
        month = load_flw_from_month(year)
    return render(request, 'load_from_month.html', {'month': month})


def load_from_day(request):
    # print('load_day')
    year = request.GET.get('year', None)
    month = request.GET.get('month', None)
    day_arr = []
    if year and month:
        year = int(year)
        month = int(month)
        day_arr = load_flw_from_day(year, month)
    return render(request, 'load_from_day.html', {'day_arr': day_arr})


def load_to_year(request):
    from_year = request.GET.get('year', None)
    year_choice = []
    if from_year:
        from_year = int(from_year)
        year_choice = load_flw_to_year(from_year)
    return render(request, 'load_to_year.html', {'years': year_choice})


def load_to_month(request):
    from_year = request.GET.get('from_year', None)
    to_year = request.GET.get('to_year', None)
    from_month = request.GET.get('from_month', None)
    month_choice = []
    if from_year and to_year and from_month:
        from_year = int(from_year)
        to_year = int(to_year)
        from_month = int(from_month)
        month_choice = load_flw_to_month(from_year, to_year, from_month)
    return render(request, 'load_to_month.html', {'months': month_choice})


def load_to_day(request):
    from_year = request.GET.get('from_year', None)
    to_year = request.GET.get('to_year', None)
    from_month = request.GET.get('from_month', None)
    to_month = request.GET.get('to_month', None)
    from_day = request.GET.get('from_day', None)

    days = []

    if from_month and from_year and from_day and to_year and to_month:
        from_day = int(from_day)
        from_month = int(from_month)
        from_year = int(from_year)
        to_year = int(to_year)
        to_month = int(to_month)
        days = load_flw_to_day(
            from_year, to_year, from_month, to_month, from_day)
    return render(request, 'load_to_day.html', {'days': days})


def load_city(request):
    print('load_city')
    country_id = int(request.GET.get('country'))
    print(country_id)
    cities = City.objects.filter(country_id=country_id)
    print(cities)
    return render(request, 'ajax_city.html', {'cities': cities})


urlpatterns = [
    path('load_from_month/', load_from_month),
    path('load_from_day/', load_from_day),
    path('load_city/', load_city),
    path('load_to_year/', load_to_year),
    path('load_to_month/', load_to_month),
    path('load_to_day/', load_to_day),
]
