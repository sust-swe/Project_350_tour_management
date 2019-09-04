from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit
from django import forms
from django.contrib.auth.models import User
from homepage.models import UserDetail


class UserDetailForm(forms.ModelForm):
    mobile = forms.IntegerField(label='Mobile Number (Not used here before)', required=True)

    class Meta:
        model = UserDetail
        fields = ['mobile', 'city', 'address', 'img', 'description']
        labels = {
            'mobile': 'Mobile NO', 'img': 'Your Photo', 'description': 'Description'
        }


class UserForm(forms.ModelForm):
    password = forms.CharField(max_length=20, min_length=8, label='Password (Minimum 8 characters)',
                               widget=forms.PasswordInput, required=True)
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput, required=True)
    email = forms.EmailField(label='Email Address', widget=forms.EmailInput, required=True)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password']
        labels = {
            'username': 'Username', 'first_name': 'First Name', 'last_name': 'Last Name',
            'email': 'Email Address', 'password': 'Password'
        }


class UpdateUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']


class PasswordChangeForm(forms.Form):
    current_password = forms.CharField(max_length=100, widget=forms.PasswordInput, required=True,
                                       label='Current Password')
    new_password = forms.CharField(max_length=100, widget=forms.PasswordInput, required=True,
                                   label='New Password')
    confirm_password = forms.CharField(max_length=100, widget=forms.PasswordInput, required=True,
                                       label='Confirm Password')

# pip install django-crispy-forms
