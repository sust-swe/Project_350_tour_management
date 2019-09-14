from django.urls import path
from . import views

urlpatterns = [

    path('', views.index, name='index'),
    path('home/', views.home, name='home'),
    path('profile/', views.profile, name='profile'),
    path('edit_profile/', views.edit_profile, name='edit profile'),
    path('change_password/', views.change_password, name='change password'),
    path('underground/', views.Underground.as_view(), name='Underground')
]