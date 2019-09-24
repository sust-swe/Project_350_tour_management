from django.shortcuts import render, redirect
from django.contrib import messages
from .models import UserDetail
from .forms import UserForm, UserDetailForm, UpdateUserForm, PasswordChangeForm
from django import views
from django.contrib.auth.models import User
from django.db.models import Q
from django.contrib.auth import login, authenticate, logout
# Create your views here.


def index(request):
    return render(request, 'index.html')


def home(request):
    return render(request, 'home.html')


class Profile(views.View):
    template_name = 'profile.html'

    def get(self, request):
        if request.user.is_authenticated:
            user_detail = UserDetail.objects.get(user=request.user)
            context = {'user': request.user, 'user_detail': user_detail}
            return render(request, self.template_name, context)
        else:
            messages.info(request, 'Log in first')
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
            user_detail_form = UserDetailForm(
                request.POST, request.FILES, instance=user_detail)
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


class ChangePassword(views.View):
    template_name = 'change_password.html'
    form_class = PasswordChangeForm

    def get(self, request):
        if request.user.is_authenticated:
            user = request.user
            form = self.form_class()
            return render(request, self.template_name, {'form': form})
        else:
            messages.info(request, 'You must log in first')
            return redirect('/')

    def post(self, request):

        if request.user.is_authenticated:
            user = request.user
            form = self.form_class(request.POST or None)

            if form.is_valid():
                username = user.username
                password = form.cleaned_data['current_password']
                new_pass = form.cleaned_data['new_password']
                confirm_pass = form.cleaned_data['confirm_password']
                auth_user = authenticate(
                    request, username=username, password=password)
                if auth_user is not None:
                    if new_pass == confirm_pass:
                        auth_user.set_password(new_pass)
                        print('cppost')
                        auth_user.save()
                        login(request, auth_user)
                        return redirect('/home/')
                    else:
                        messages.info(request, 'Passwords not matching')
                        return redirect('/change_password/')
                else:
                    messages.info(request, 'Permission denied')
                    return redirect('/underground/')
            else:
                return render(request, self.template_name, {'form': form})
        else:
            messages.info(request, 'You must log in first')
            return redirect('/')


class Underground(views.View):
    template_name = 'underground.html'

    def get(self, request):
        return render(request, self.template_name)


class PermissionDenied(views.View):

    def get(self, request):
        messages.info(request, 'Permission Denied')
        return redirect('/')
