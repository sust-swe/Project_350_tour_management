from django.urls import path
from . import views

urlpatterns = [
    path('restaurant/', views.search_restaurant, name='search restaurant')
]