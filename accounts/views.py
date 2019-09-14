from homepage.models import UserDetail
from django.contrib import messages, auth
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User, auth
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import UserDetailForm, UserForm
import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bravo1.settings")
django.setup()

# Create your views here.


def my_register(request):
    if request.user.is_authenticated:
        return redirect('/home/')
    else:
        form1 = UserForm()
        form2 = UserDetailForm()

        if request.method == 'POST':
            user_form = UserForm(request.POST)
            user_detail_form = UserDetailForm(request.POST)

            if user_form.is_valid() and user_detail_form.is_valid():
                username = user_form.cleaned_data['username']
                first_name = user_form.cleaned_data['first_name']
                last_name = user_form.cleaned_data['last_name']
                password1 = user_form.cleaned_data['password']
                password2 = user_form.cleaned_data['password2']
                email = user_form.cleaned_data['email']
                mobile = user_detail_form.cleaned_data['mobile']

                if password1 != password2:
                    messages.info(request, 'Passwords not matching')
                elif User.objects.filter(email=email).exists():
                    messages.info(request, 'Email Address Taken')
                else:
                    current_user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name,
                                                            password=password1, email=email)
                    current_user_detail = user_detail_form.save(commit=False)
                    current_user_detail.user = current_user
                    current_user_detail.save()
                    login(request, current_user)
                    return redirect('/home/')

                return render(request, 'register.html', {'form1': user_form, 'form2': user_detail_form})
            else:
                messages.info(request, 'Invalid Credentials')
                return render(request, 'register.html', {'form1': user_form, 'form2': user_detail_form})

        else:
            return render(request, 'register.html', {'form1': form1, 'form2': form2})


def my_login(request):
    if request.user.is_authenticated:
        return redirect('/home/')
    else:
        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']
            current_user = authenticate(request, username=username, password=password)
            print(type(current_user))
            if current_user is None:
                messages.info(request, 'Invalid username or password')
                return redirect('/accounts/login/')
            else:
                login(request, current_user)
                return redirect('/home/')

        else:
            return render(request, 'login.html')


def my_logout(request):
    if request.user.is_authenticated:
        logout(request)
        return redirect('/')
    else:
        return redirect('/')


# messages.info(request, '4')
# return HttpResponse('hi') replaces current html content
# render(request, 'base.html', {'a': b} process base with the json data
