from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit
from django import forms
from django.contrib.auth.models import User
from homepage.models import UserDetail
from crispy_forms.helper import FormHelper


class UserDetailForm(forms.ModelForm):
    mobile = forms.IntegerField(
        label='Mobile Number (to be unique)', required=True)

    class Meta:
        model = UserDetail
        fields = ['mobile', 'img']
        labels = {
            'mobile': 'Mobile NO*', 'img': 'Your Photo', 'description': 'Description'
        }
        widgets = {
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),


        }


class UserForm(forms.ModelForm):
    password = forms.CharField(max_length=100, min_length=8, label='Password (Minimum 8 characters)',
                               widget=forms.PasswordInput(attrs={'class': 'form-control'}), required=True)
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput(attrs={'class': 'form-control'}), required=True, max_length=100,
                                min_length=8)
    email = forms.EmailField(label='Email Address',
                             widget=forms.EmailInput(attrs={'class': 'form-control'}), required=True)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password']
        labels = {
            'username': 'Username', 'first_name': 'First Name', 'last_name': 'Last Name',
            'email': 'Email Address', 'password': 'Password'
        }
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),


        }


class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}))
