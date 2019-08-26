from django import forms
from django.contrib.auth.models import User
from homepage.models import UserDetail


class CreateUserDetail(forms.ModelForm):
    class Meta:
        model = UserDetail
        fields = ['mobile', 'img', 'description']


class CreateUser(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password']
