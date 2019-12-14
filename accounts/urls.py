# from django.contrib import admin
from django.urls import path
from . import views


urlpatterns = [
    path('register/', views.MyRegister.as_view(), name='register'),
    path('login/', views.MyLogin.as_view(), name='login'),
    path('logout/', views.my_logout, name='logout'),
    path("profile/<int:user_id>/", views.ShowProfileDetail.as_view()),
]
