from django.shortcuts import render, redirect
from django.contrib import messages
from .models import UserDetail
from .forms import UserForm, UserDetailForm
from django.contrib.auth.models import User
from django.db.models import Q
from django.contrib.auth import login, authenticate, logout
# Create your views here.


def index(request):
    return render(request, 'index.html')


def home(request):
    return render(request, 'home.html')


def profile(request):
    if request.user.is_authenticated:
        user = request.user
        user_d = UserDetail.objects.get(user=user)
        form = UserDetailForm(instance=user_d)

        if request.method == 'POST':
            pass
        else:
            return render(request, 'profile.html', {'user': user, 'user_detail': user_d})

    else:
        messages.info(request, 'You must log in first')
        return redirect('/')


def edit_profile(request):
    if request.user.is_authenticated:
        user = request.user
        user_d = UserDetail.objects.get(user=user)

        if request.method == 'GET':
            user_form = UserForm(instance=user)
            user_detail_form = UserDetailForm(instance=user_d)
            return render(request, 'editprofile.html', {'user_form': user_form, 'user_detail_form': user_detail_form})

        else:
            user_form = UserForm(request.POST)
            user_detail_form = UserDetailForm(request.POST)

            if user_form.is_valid() and user_detail_form.is_valid():
                email = user_form.cleaned_data['email']
                mobile = user_detail_form.cleaned_data['mobile']

                if User.objects.filter(Q(email=email),Q(id!=user.id)).exists():
                    messages.info(request, 'Email already used')
                    return render(request, 'editprofile.html', {'user_form': user_form, 'user_detail_form': user_detail_form})

                elif UserDetail.objects.filter(Q(mobile=mobile), Q(user != user)).exists():
                    messages.info(request, 'Mobile No already used')
                    return render(request, 'editprofile.html', {'user_form': user_form, 'user_detail_form': user_detail_form})

                else:
                    user_form.save()
                    user_detail_form.save()
                    return redirect('/profile/')

            else:
                messages.info(request, 'Invalid Credentials')
                return render(request, 'editprofile.html', {'user_form': user_form, 'user_detail_form': user_detail_form})

    else:
        messages.info(request, 'Log in first')
        return redirect('/')


def change_password(request):
    if request.user.is_authenticated:
        user = request.user
        user_d = UserDetail.objects.get(user=user)

        if request.method == 'GET':
            return render(request, 'changepassword.html')

        else:
            current_password = request.POST['current_password']
            new_password = request.POST['new_password']
            confirm_password = request.POST['confirm_password']
            user_2 = authenticate(request, username=user.username, password=current_password)

            if user_2 is not None and user_2 == user:
                if new_password == confirm_password:
                    user.set_password(new_password)
                    messages.info(request, 'Password successfully changed')
                    return redirect('/profile/')

                else:
                    messages.info(request, 'Passwords not matching')
                    return redirect('/change_password/')

            else:
                messages.info(request, 'Wrong Password')
                return redirect('/change_password/')