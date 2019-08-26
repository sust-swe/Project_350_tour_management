from django.contrib import messages
from django.contrib.auth.models import User, auth
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import CreateUser, CreateUserDetail
# Create your views here.


def register(request):
    if request.method == 'GET':

        form = CreateUserDetail()
        form1 = CreateUser()
        forms = [form, form1]
        return render(request, 'register.html', {'form': forms})

    else:
        return render(request, 'index.html', {'msg': 'logged in'})


def login(request):

    if request.method == 'GET':
        return render(request, 'login.html')

    else:
        un = request.POST['username']
        pw = request.POST['password']

        user = auth.authenticate(username=un, password=pw)
        if user is not None:
            auth.login(request, user)
            messages.info(request, 'logged in')
            return render(request, 'index.html')

        return render(request, 'index.html', {'msg': 'logged in'})
