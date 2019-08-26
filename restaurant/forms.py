from django import forms
from .models import Restaurant, Food


class RestaurantForm(forms.ModelForm):
    class Meta:
        model = Restaurant
        fields = ['name', 'mobile', 'description', 'img']


class FoodForm(forms.ModelForm):
    class Meta:
        model = Food
        fields = ['name', 'img', 'price', 'person', 'available_at_time']
