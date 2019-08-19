from django.contrib import messages
from django.contrib.auth.models import User, auth
from django.shortcuts import render, redirect
from django.http import HttpResponse

# Create your views here.


def register(request):
    if request.method == 'GET':
        return render(request, 'register.html')

    else:
        fn = request.POST['first_name']
        lun = request.POST['last_name']
        un = request.POST['username']
        pw1 = request.POST['password1']
        pw2 = request.POST['password2']

        if pw1 != pw2:
            messages.info(request, 'ERROR : Passwords do not match ')
            # return render(request, 'register.html')
            return redirect('/accounts/register/')

        elif len(pw1)<8:
            messages.info(request, 'ERROR : Password must have at least 8 characters')
            return redirect('/accounts/register/')

        elif User.objects.filter(username=un).exists():
            messages.info(request, 'ERROR : Username Taken')
            return redirect('/accounts/register/')

        else:
            notun_user = User.objects.create_user(username=un, email=None, password=pw1,first_name=fn,last_name=lun)
            notun_user.save()
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
