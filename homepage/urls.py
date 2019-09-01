from django.urls import path
from . import views

urlpatterns = [

    path('', views.index, name='index'),
    path('home/', views.home, name='home'),
    path('userdetail/', views.user_detail, name='user detail')

]