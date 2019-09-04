from django.shortcuts import render, redirect
from django.contrib import messages
from .models import UserDetail
from .forms import UserForm, UserDetailForm, UpdateUserForm, PasswordChangeForm

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
        current_user = request.user
        user_detail = UserDetail.objects.get(user=current_user)
        if request.method == 'POST':
            pass
        else:
            context = {'user': current_user, 'user_detail': user_detail}
            return render(request, 'profile.html', context)

    else:
        messages.info(request, 'You must log in first')
        return redirect('/')


def edit_profile(request):
    if request.user.is_authenticated:
        user = request.user
        user_detail = UserDetail.objects.get(user=user)

        if request.method == 'GET':
            user_form = UpdateUserForm(instance=user)
            user_detail_form = UserDetailForm(instance=user_detail)
            context = {
                'user_form': user_form, 'user_detail_form': user_detail_form
            }
            return render(request, 'edit_profile.html', context)

        else:
            user_form = UpdateUserForm(request.POST or None, instance=user)
            user_detail_form = UserDetailForm(request.POST, request.FILES, instance=user_detail)
            if user_form.is_valid() and user_detail_form.is_valid():
                user_form.save()
                user_detail_form.save()
                messages.info(request, 'Successfully updated')
                return redirect('/profile/')
            else:
                context = {
                    'user_form': user_form, 'user_detail_form': user_detail_form
                }
                return render(request, 'edit_profile.html', context)

    else:
        messages.info(request, 'Log in first')
        return redirect('/')


def change_password(request):
    if request.user.is_authenticated:
        user = request.user

        if request.method == 'GET':
            form = PasswordChangeForm()
            context = {'form': form}
            return render(request, 'change_password.html', context)

        else:
            form = PasswordChangeForm(request.POST or None)
            if form.is_valid():
                cur_pass = form.cleaned_data['current_password']
                new_pass = form.cleaned_data['new_password']
                con_pass = form.cleaned_data['confirm_password']

                if new_pass == con_pass:
                    username = user.username
                    auth_user = authenticate(request, username=username, password=cur_pass)
                    if auth_user is not None:
                        user.set_password(new_pass)
                        user.save()
                        return redirect('/profile/')

                    else:
                        messages.info(request, 'Wrong Password')
                        return redirect('/change_password/')
                else:
                    messages.info(request, 'Passwords not matching')
                    return redirect('/change_password/')
            else:
                messages.info(request, 'Passwords must be between 8 to 100 characters inclusive')
                return redirect('/change_password/')
    else:
        messages.info(request, 'You must log in first')
        return redirect('/')
