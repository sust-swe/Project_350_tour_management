from homepage.base import *


month_array = ['', 'January', 'February', 'March', 'April', 'May', 'June',
               'July', 'August', 'September', 'Octobor', 'November', 'December']


def load_month(request):
    #    print(type(request.GET)) <class 'django.http.request.QueryDict'>
    year = int(request.GET.get('year'))
    today_ = datetime.today()
    this_month = today_.month
    this_year = today_.year

    if year == this_year:
        month = [(str(i), month_array[i]) for i in range(this_month, 13)]
    else:
        month = [(str(i), month_array[i]) for i in range(1, 13)]
    # print(month)
    for m, n in month:
        print(m, n)
    return render(request, 'load_month.html', {'month': month})


def load_city(request):
    print('load_city')
    country_id = int(request.GET.get('country'))
    print(country_id)
    cities = City.objects.filter(country_id=country_id)
    print(cities)
    return render(request, 'ajax_city.html', {'cities': cities})


def load_day(request):
    print('load_day')
    year = int(request.GET.get('year'))
    month = int(request.GET.get('month'))

    if month in [1, 3, 5, 7, 8, 10, 12]:
        ub = 31
    elif month in [4, 6, 9, 11]:
        ub = 30

    day_arr = [str(i) for i in range(1, ub+1)]
    return render(request, 'load_day.html', {'day_arr': day_arr})


urlpatterns = [
    path('load_month/', load_month),
    path('load_day/', load_day),
    path('load_city/', load_city),
]
