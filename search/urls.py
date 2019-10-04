from django.urls import path, include
from . import views

urlpatterns = [
    path('restaurant/', views.SearchRestaurant.as_view(), name='search restaurant'),
    path('sbt/', include('search.search_by_time')),
    path('ajax/', include('search.ajax_handler')),
]
