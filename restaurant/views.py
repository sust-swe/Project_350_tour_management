from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.models import User, auth
# from .models import @classname

# Create your views here.


def register(request):
    return render(request, 'register.html')