from django import forms
from .models import UserDetail, User


class UserDetailForm(forms.ModelForm):
    class Meta:
        model = UserDetail
        fields = ['mobile', 'description', 'img']


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']