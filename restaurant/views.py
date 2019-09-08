from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.models import User, auth
# from .models import @classname
from .forms import RestaurantForm, FoodForm
from .models import Restaurant, Food
from homepage.models import UserDetail
from django import views


# Create your views here.
class MyRestaurant(views.View):
    context = {}
    template_name = 'my_restaurant.html'

    def get(self, request):
        if request.user.is_authenticated:
            user = request.user
            qs = Restaurant.objects.filter(user_detail__user=user)
            self.context = {'qs': qs}
            return render(request, self.template_name, self.context)
        else:
            messages.info(request, 'You must log in to continue')
            return redirect('/')


class RestaurantDetail(views.View):
    context = {}
    template_name = 'detail.html'

    def get(self, request, id):
        restaurant = Restaurant.objects.get(pk=id)
        self.context = {'restaurant': restaurant}
        return render(request, self.template_name, self.context)


class AddRestaurant(views.View):
    form_class = RestaurantForm
    template_name = 'add_restaurant.html'

    def post(self, request):
        if request.user.is_authenticated:
            user = request.user
            user_detail_v = UserDetail.objects.get(user=user)
            form = self.form_class(request.POST, request.FILES)
            if form.is_valid():
                new_restaurant = form.save(commit=False)
                new_restaurant.user_detail = user_detail_v
                new_restaurant.save()
                return redirect('/restaurant/my_restaurant/')
            else:
                messages.info(request, 'Invalid Credentials')
                return render(request, self.template_name, {'form': form})
        else:
            messages.info(request, 'You must log in to continue')
            return redirect('/')

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})


class UpdateRestaurant(views.View):
    form_class = RestaurantForm
    template_name = 'update_restaurant.html'

    def get(self, request, id):
        if request.user.is_authenticated:
            restaurant = Restaurant.objects.get(pk=id)
            if restaurant.user_detail.user == request.user:
                form = self.form_class(instance=restaurant)
                return render(request, self.template_name, {'form': form})
            else:
                messages.info('Permission denied')
                return redirect('')
        else:
            messages.info(request, 'Permission denied')
            return redirect('/')

    def post(self, request, id):
        if request.user.is_authenticated:
            restaurant = Restaurant.objects.get(pk=id)
            if restaurant.user_detail.user == request.user:
                form = self.form_class(request.POST, request.FILES, instance=restaurant)
                if form.is_valid():
                    form.save()
                    return redirect('/restaurant/detail/{}'.format(id))
                else:
                    messages.info(request, 'Invalid Credentials')
                    return render(request, self.form_class, {'form': form})
            else:
                messages.info(request, 'Permission denied')
                return redirect('/home/')
        else:
            messages.info(request, 'You must login first')
            return redirect('/')


def delete_restaurant(request, id):
    if request.user.is_authenticated:
        user = request.user
        if request.method == 'GET':
            restaurant = Restaurant.objects.get(pk=id)
            restaurant.delete()
            return redirect('/restaurant/my_restaurant/')
        else:
            pass
    else:
        messages.info(request, 'You must login first')
        return redirect('/')


def show_menu(request, id):
    if request.user.is_authenticated:
        user = request.user
        restaurant = Restaurant.objects.get(pk=id)
        if request.method == 'GET':
            menu = Food.objects.filter(restaurant=restaurant)
            return render(request, 'menu.html', {'menu': menu, 'restaurant': restaurant})
        else:
            pass
    else:
        messages.info(request, 'You must login first')
        return redirect('/')


def add_item(request, id):
    if request.user.is_authenticated:
        if request.method == 'GET':
            form = FoodForm()
            return render(request, 'add_item.html', {'form': form})
        else:
            restaurant = Restaurant.objects.get(pk=id)
            form = FoodForm(request.POST, request.FILES)
            if form.is_valid():
                tmp_form = form.save(commit=False)
                tmp_form.restaurant = restaurant
                tmp_form.save()
                return redirect('/restaurant/menu/{}'.format(id))
    else:
        messages.info(request, 'You must login first')
        return redirect('/')


def search(request, restaurant):
    pass


class ShowAllRestaurant(views.View):

    def get(self, request):
        qs = Restaurant.objects.all()
        return render(request, 'my_restaurant.html', {'qs': qs})
'''
if request.user.is_authenticated:
    if request.method == 'GET':
        pass
    else:
        pass    
else:
    messages.info(request, 'You must login first')
    return redirect('/')
'''
