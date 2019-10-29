# from django.contrib import admin
from django.urls import path
from . import views


urlpatterns = [
    path('register/', views.my_register, name='register'),
    path('login/', views.my_login, name='login'),
    path('logout/', views.my_logout, name='logout'),
    path("profile/<int:user_id>/", views.ShowProfileDetail.as_view()),
]
