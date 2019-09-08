# main urls from django.contrib import admin
from django.urls import path, include
from . import views
# main urls from django.conf import settings
# main urls from django.conf.urls.static import static


urlpatterns = [
    path('my_restaurant/', views.MyRestaurant.as_view(), name='my restaurant'),
    path('detail/<int:id>/', views.RestaurantDetail.as_view(), name='restaurant detail'),
    path('update/<int:id>/', views.UpdateRestaurant.as_view(), name='update restaurant'),
    path('show/', views.ShowAllRestaurant.as_view(), name='show all restaurant'),
]


