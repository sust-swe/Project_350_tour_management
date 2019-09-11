# main urls from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [

    # path('login/', views.login, name='login')
    path('my_residence/', views.MyResidence.as_view(), name='my residence'),
    path('add_residence/', views.AddResidence.as_view(), name='add residence'),
    path('<int:id>/', views.ResidenceDetail.as_view(), name='residence detail'),

]

