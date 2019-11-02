# main urls from django.contrib import admin
from django.urls import path, include
from . import views

# main urls from django.conf import settings
# main urls from django.conf.urls.static import static


urlpatterns = [
    path('my_restaurant/', views.MyRestaurant.as_view(), name='my restaurant'),
    path('add/', views.AddRestaurant.as_view(), name='add new restaurant'),
    path('<int:id>/', views.RestaurantDetail.as_view(), name='restaurant detail'),
    path('<int:id>/update/', views.UpdateRestaurant.as_view(),
         name='update restaurant'),
    path('<int:id>/delete/', views.DeleteRestaurant.as_view(),
         name='delete restaurant'),
    path('<int:id>/menu/', views.Menu.as_view(), name='menu'),
    path("<int:restaurant_id>/orders/", views.ShowRestaurantOrders.as_view()),
    path('all/', views.ShowAllRestaurant.as_view(), name='show all restaurant'),
    path('<int:id>/menu/add_item/', views.AddFood.as_view(), name='add menu item'),
    path('food/<int:food_id>/update/',
         views.UpdateFood.as_view(), name='update menu item'),
    path('food/<int:food_id>/delete/',
         views.DeleteFood.as_view(), name='delete menu item'),
    path("food/<int:food_id>/", views.ShowFoodDetail.as_view()),
    path("addtocart/", views.AddToCart.as_view()),
    path("gotocart/", views.GoToCart.as_view()),
    path("delfromcart/", views.DelFromCart.as_view()),
    path("place_order/", views.PlaceOrder.as_view()),
    path("purchased_order/", views.MyPlacedFoodOrder.as_view()),
    path("order/<int:order_id>/", views.ShowRestaurantOrderDetail.as_view()),
    
]
