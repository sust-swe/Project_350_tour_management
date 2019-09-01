from django.shortcuts import render, redirect
from django.contrib import messages
from .models import UserDetail
# Create your views here.


def index(request):
    return render(request, 'index.html')


def home(request):
    return render(request, 'home.html')


def user_detail(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            pass
        else:
            pass

    else:
        messages.info(request, 'You must log in first')
        return redirect('/')
