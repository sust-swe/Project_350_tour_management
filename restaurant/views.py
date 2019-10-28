from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.models import User, auth
from .forms import RestaurantForm, FoodForm
from .models import Restaurant, Food, Cart, CartDetail, Order, OrderDetail
from homepage.models import UserDetail
from django import views
from django.core.exceptions import ValidationError, NON_FIELD_ERRORS
from homepage.base import *


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
    template_name = 'restaurant_detail.html'

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
                form = self.form_class(
                    request.POST, request.FILES, instance=restaurant)
                # print(form.as_table())
                if form.is_valid():
                    ob = form.save(commit=False)
                    # print(ob.user_detail_id, 'hi')
                    # print(ob.user_detail_id)
                    try:
                        ob.full_clean()
                        ob.save()
                        return redirect('/restaurant/{}/'.format(id))
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

###########################################        Food               ######################################################


class Menu(views.View):
    template_name = 'menu.html'

    def get(self, request, id):
        restaurant = Restaurant.objects.get(pk=id)
        menu = Food.objects.filter(restaurant=restaurant)
        return render(request, self.template_name, {'menu': menu, 'restaurant': restaurant})


class AddFood(views.View):
    template_name = 'add_menu_item.html'
    form_class = FoodForm

    def get(self, request, id):
        if request.user.is_authenticated:
            restaurant = Restaurant.objects.get(pk=id)
            if restaurant.user_detail.user == request.user:
                form = self.form_class()
                return render(request, self.template_name, {'form': form})
            else:
                return redirect("/permission_denied/")
        else:
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
                        for kk in e.message_dict:
                            form.add_error(kk, e.message_dict[kk])
                        return render(request, self.template_name, {'form': form})
                else:
                    return render(request, self.template_name, {'form': form})
            else:
                return redirect("/permission_denied/")
        else:
            return redirect("/login_required/")


class ShowFoodDetail(views.View):
    template_name = "food_detail.html"

    def get(self, request, food_id):
        food = Food.objects.get(pk=food_id)
        return render(request, self.template_name, {"food": food})


class UpdateFood(views.View):
    form_class = FoodForm
    template_name = 'update_menu_item.html'

    def get(self, request, food_id):
        print('update menu item get')
        if request.user.is_authenticated:
            food = Food.objects.get(pk=food_id)
            if food.restaurant.user_detail.user == request.user:
                form = self.form_class(instance=food)
                return render(request, self.template_name, {'form': form})
            else:
                messages.info(request, 'Permission denied')
                return redirect('/homepage/underground/')
        else:
            messages.info(request, 'You must login first')
            redirect('/')

    def post(self, request, food_id):
        if request.user.is_authenticated:
            food = Food.objects.get(pk=food_id)
            if food.restaurant.user_detail.user == request.user:
                form = self.form_class(
                    request.POST, request.FILES, instance=food)

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


class DeleteFood(views.View):

    def get(self, request, food_id):
        if request.user.is_authenticated:
            food = Food.objects.get(pk=food_id)
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


############################       Cart         ###################################################


def getCart(request):
    cart = None
    if not Cart.objects.filter(owner=request.user).exists():
        # print("getCart of not having")
        cart = Cart(owner=request.user, restaurant=None, bill=0)
        cart.save()
    else:
        cart = Cart.objects.get(owner=request.user)
    return cart


def fix_cart(cart_detail):
    if cart_detail.cart.restaurant == cart_detail.food.restaurant:
        if CartDetail.objects.filter(cart=cart_detail.cart, food=cart_detail.food).exists():
            return CartDetail.objects.get(cart=cart_detail.cart, food=cart_detail.food)
        else:
            return cart_detail
    else:
        cart = cart_detail.cart
        cart.restaurant = cart_detail.food.restaurant
        CartDetail.objects.filter(cart=cart_detail.cart).delete()
        cart.bill = 0
        cart.save()
        return cart_detail


class AddToCart(views.View):

    def get(self, request):
        cart = getCart(request)
        # print("280", cart.restaurant)
        food_id = int(request.GET.get("item_id"))
        food = Food.objects.get(id=food_id)
        cart_detail = CartDetail(cart=cart, food=food, quantity=0)
        cart_detail = fix_cart(cart_detail)
        cart_detail.quantity += 1
        cart.bill += food.price
        try:
            cart_detail.full_clean()
            cart_detail.save()
            cart.full_clean()
            cart.save()
            # print("287", cart_detail.cart.restaurant)
            return render(request, "response.html", {"response": "ADDED"})
        except:
            return render(request, "response.html", {"response": "Failed"})


class DelFromCart(views.View):
    
    def get(self, request):
        cart=getCart(request)
        food_id=int(request.GET.get("item_id"))
        food = Food.objects.get(id=food_id)
        cart_detail = CartDetail.objects.get(cart=cart, food=food)
        
        if cart_detail.quantity == 1:
            if CartDetail.objects.filter(cart__owner=request.user).count() == 1:
                cart.restaurant = None
                cart.bill = 0
                cart.save()
            cart_detail.delete()
            
            return render(request, "response.html", {"response": "Deleted"})
        cart.bill-=food.price
        cart_detail.quantity -= 1
        try:
            cart_detail.full_clean()
            cart_detail.save()
            cart.full_clean()
            cart.save()
            return render(request, "response.html", {"response": "Deleted"})
        except:
            return render(request, "response.html", {"response": "Failed"})


class GoToCart(views.View):
    template_name = "cart.html"

    def get(self, request):
        cart = getCart(request)
        cart_detail = CartDetail.objects.filter(cart__owner=request.user)
        print(cart.bill)
        return render(request, self.template_name, {"cart_detail": cart_detail, "cart": cart})
    
#############################################      Order       #########################################################


class PlaceOrder(views.View):
    
    def get(self, request):
        cart = Cart.objects.get(owner=request.user)
        new_order = Order(customer=request.user, restaurant=cart.restaurant, bill=cart.bill, order_time=datetime.now())
        new_order.save()
        cart_details = CartDetail.objects.filter(cart__owner=request.user)
        for item in cart_details:
            order_detail = OrderDetail(order=new_order, food=item.food, quantity=item.quantity)
            order_detail.save()
            item.delete()
        cart.restaurant = None
        cart.bill = 0
        return redirect("/restaurant/my_food_orders/")
    

class MyPlacedFoodOrder(views.View):
    
    def get(self, request):
        orders = Order.objects.filter(customer=request.user)
        return render(request, "my_food_order.html", {"orders": orders})
    
    
class ShowOrderDetail(views.View):
    template_name="order_detail.html"
    
    def get(self, request, order_id):
        order = Order.objects.get(pk=order_id)
        order_details = OrderDetail.objects.filter(order=order)
        return render(request, self.template_name, {"order": order, "order_details": order_details})

        
