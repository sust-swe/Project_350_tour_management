from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.models import User, auth
from .forms import RestaurantForm, FoodForm
from .models import Restaurant, Food
from homepage.models import UserDetail
from django import views
from django.core.exceptions import ValidationError, NON_FIELD_ERRORS


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


class AddRestaurant(views.View):
    form_class = RestaurantForm
    template_name = 'add_restaurant.html'

    def post(self, request):
        if request.user.is_authenticated:
            user = request.user
            user_detail = UserDetail.objects.get(user=user)
            form = self.form_class(request.POST, request.FILES)
            if form.is_valid():
                ob = form.save(commit=False)
                ob.user_detail = user_detail
                try:
                    ob.full_clean()
                    ob.save()
                    return redirect('/restaurant/my_restaurant/')
                except ValidationError as e:
                    nfe = e.message_dict[NON_FIELD_ERRORS]
                    return render(request, self.template_name, {'form': form, 'nfe': nfe})
            else:
                # print(form.as_table())
                messages.info(request, 'Invalid Credentials')
                return render(request, self.template_name, {'form': form})
        else:
            messages.info(request, 'You must log in to continue')
            return redirect('/')

    def get(self, request):
        if request.user.is_authenticated:
            user_detail = UserDetail.objects.get(user=request.user)
            form = self.form_class()
            return render(request, self.template_name, {'form': form})
        else:
            messages.info(request, 'You must log in to continue')
            return redirect('/')


class RestaurantDetail(views.View):
    context = {}
    template_name = 'residence_detail.html'

    def get(self, request, id):
        restaurant = Restaurant.objects.get(pk=id)
        self.context = {'restaurant': restaurant}
        return render(request, self.template_name, self.context)


class UpdateRestaurant(views.View):
    form_class = RestaurantForm
    template_name = 'update_residence.html'

    def get(self, request, id):
        if request.user.is_authenticated:
            restaurant = Restaurant.objects.get(pk=id)
            if restaurant.user_detail.user == request.user:
                form = self.form_class(instance=restaurant)
                return render(request, self.template_name, {'form': form})
            else:
                messages.info('Permission denied')
                return redirect('/homepage/underground/')
        else:
            messages.info(request, 'You must login first')
            return redirect('/')

    def post(self, request, id):
        if request.user.is_authenticated:
            restaurant = Restaurant.objects.get(pk=id)
            if restaurant.user_detail.user == request.user:
                form = self.form_class(request.POST, request.FILES, instance=restaurant)
                # print(form.as_table())
                if form.is_valid():
                    ob = form.save(commit=False)
                    # print(ob.user_detail_id, 'hi')
                    print(ob.user_detail_id)
                    try:
                        ob.full_clean()
                        ob.save()
                        return redirect('/restaurant/detail/{}'.format(id))
                    except ValidationError as e:
                        nfe = e.message_dict[NON_FIELD_ERRORS]
                        return render(request, self.template_name, {'form': form, 'nfe': nfe})
                else:
                    messages.info(request, 'Invalid Credentials')
                    return render(request, self.template_name, {'form': form})
            else:
                messages.info(request, 'Permission denied')
                return redirect('/homepage/underground/')
        else:
            messages.info(request, 'You must login first')
            return redirect('/')


class DeleteRestaurant(views.View):

    def get(self, request, id):
        if request.user.is_authenticated:
            restaurant = Restaurant.objects.get(pk=id)
            if restaurant.user_detail.user == request.user:
                restaurant.delete()
                return redirect('/restaurant/my_restaurant/')
            else:
                messages.info(request, 'Permission Denied')
                return HttpResponse('/homepage/underground/')
        else:
            messages.info(request, 'You must login first')
            redirect('/')


############################################################################################################
class Menu(views.View):
    template_name = 'menu.html'

    def get(self, request, id):
        restaurant = Restaurant.objects.get(pk=id)
        menu = Food.objects.filter(restaurant=restaurant)
        return render(request, self.template_name, {'menu': menu, 'restaurant': restaurant})


class AddMenuItem(views.View):
    template_name = 'add_menu_item.html'
    form_class = FoodForm

    def get(self, request, id):
        if request.user.is_authenticated:
            restaurant = Restaurant.objects.get(pk=id)
            if restaurant.user_detail.user == request.user:
                form = self.form_class()
                return render(request, self.template_name, {'form': form})
            else:
                messages.info(request, 'Permission Denied')
                return HttpResponse('/homepage/underground/')
        else:
            messages.info(request, 'You must login first')
            redirect('/')

    def post(self, request, id):
        if request.user.is_authenticated:
            restaurant = Restaurant.objects.get(pk=id)
            if restaurant.user_detail.user == request.user:
                form = self.form_class(request.POST, request.FILES)
                if form.is_valid():
                    food = form.save(commit=False)
                    food.restaurant = restaurant
                    try:
                        food.full_clean()
                        food.save()
                        return redirect('/restaurant/{}/menu/'.format(id))
                    except ValidationError as e:
                        nfe = e.message_dict[NON_FIELD_ERRORS]
                        return render(request, self.template_name, {'form': form, 'nfe': nfe})
                else:
                    messages.info(request, 'Invalid Credentials')
                    return render(request, self.template_name, {'form': form})
            else:
                messages.info(request, 'Permission Denied')
                return HttpResponse('/homepage/underground/')
        else:
            messages.info(request, 'You must login first')
            redirect('/')


class UpdateMenuItem(views.View):
    form_class = FoodForm
    template_name = 'update_menu_item.html'

    def get(self, request, item_id):
        if request.user.is_authenticated:
            food = Food.objects.get(pk=item_id)
            if food.restaurant.user_detail.user == request.user:
                form = self.form_class(instance=food)
                return render(request, self.template_name, {'form': form})
            else:
                messages.info(request, 'Permission denied')
                return redirect('/homepage/underground/')
        else:
            messages.info(request, 'You must login first')
            redirect('/')

    def post(self, request, item_id):
        if request.user.is_authenticated:
            food = Food.objects.get(pk=item_id)
            if food.restaurant.user_detail.user == request.user:
                form = self.form_class(request.POST, request.FILES, instance=food)
                if form.is_valid():
                    ob = form.save(commit=False)
                    try:
                        ob.full_clean()
                        ob.save()
                        return redirect('/restaurant/{}/menu/'.format(food.restaurant.id))
                    except ValidationError as e:
                        nfe = e.message_dict[NON_FIELD_ERRORS]
                        return render(request, self.template_name, {'form': form, 'nfe': nfe})
                else:
                    messages.info(request, 'Invalid Credentials')
                    return render(request, self.template_name, {'form': form})
            else:
                messages.info(request, 'Permission denied')
                return redirect('/homepage/underground/')
        else:
            messages.info(request, 'You must login first')
            redirect('/')


class DeleteMenuItem(views.View):

    def get(self, request, item_id):
        if request.user.is_authenticated:
            food = Food.objects.get(pk=item_id)
            if food.restaurant.user_detail.user == request.user:
                food.delete()
                return redirect('/restaurant/{}/menu/'.format(food.restaurant.id))
            else:
                messages.info(request, 'Permission denied')
                return redirect('/homepage/underground/')
        else:
            messages.info(request, 'You must login first')
            redirect('/')


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
