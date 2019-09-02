# main urls from django.contrib import admin
from django.urls import path, include
from . import views
# main urls from django.conf import settings
# main urls from django.conf.urls.static import static


urlpatterns = [
    path('myrestaurant/', views.my_restaurant, name='my restaurant'),
    path('addres/', views.add_restaurant, name='add restaurants'),
    path('detail/<slug:restaurant_name>/', views.restaurant_detail, name='restaurant detail'),
]


# urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)