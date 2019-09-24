from django.urls import path
from . import views

urlpatterns = [
    path('restaurant/', views.SearchRestaurant.as_view(), name='search restaurant'),
    path('ajax/load_city/', views.load_city, name='load city'),
]
