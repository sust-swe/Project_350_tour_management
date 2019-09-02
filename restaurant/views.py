from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.models import User, auth
# from .models import @classname
from .forms import RestaurantForm
from .models import Restaurant
from homepage.models import UserDetail


# Create your views here.


def my_restaurant(request):
    if request.user.is_authenticated:
        if request.method == 'GET':
            user = request.user
            qs = Restaurant.objects.filter(user_detail__user=user)
            return render(request, 'myrestaurant.html', {'qs': qs})

    else:
        messages.info(request, 'You must log in to continue')
        return redirect('/')


def add_restaurant(request):
    if request.user.is_authenticated:
        user = request.user
        user_detail_v = UserDetail.objects.get(user=user)

        if request.method == 'POST':
            rest_form = RestaurantForm(request.POST)

            if rest_form.is_valid():
                try:
                    new_res = rest_form.save(commit=False)
                    new_res.user_detail = user_detail_v
                    new_res.save()
                    qs = Restaurant.objects.filter(user_detail=user_detail_v)
                    return render(request, 'myrestaurant.html', {'qs': qs})

                except Exception as e1:
                    messages.info(request, 'Ambiguous Data Entry')
                    print('add_restaurant, e1')
                    qs = Restaurant.objects.filter(user_detail=user_detail_v)
                    return render(request, 'myrestaurant.html', {'rest_form': rest_form, 'qs': qs})

            else:
                qs = Restaurant.objects.filter(user_detail__user=user)
                messages.info(request, 'Invalid Credentials')
                return render(request, 'myrestaurant.html', {'rest_form': rest_form, 'qs': qs})

        elif request.method == 'GET':
            rest_form = RestaurantForm()
            qs = Restaurant.objects.filter(user_detail=user_detail_v)
            return render(request, 'myrestaurant.html', {'rest_form': rest_form, 'qs': qs})

    else:
        messages.info(request, 'You must log in to continue')
        return redirect('/')


def restaurant_detail(request, restaurant_name):
    if request.method == 'GET':
        user = request.user
        restaurant = Restaurant.objects.get(user_detail__user=user, name=restaurant_name)
        context = {
            'restaurant': restaurant
        }
        return render(request, 'restaurantdetail.html', context)

