from django.shortcuts import render

# Create your views here.


def search_restaurant(request):
    if request.method == 'POST':
        form = SearchRestaurantForm()
        return render(request, 'search_restaurant.html')