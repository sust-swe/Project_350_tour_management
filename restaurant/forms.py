from django import forms
from .models import Restaurant, Food


class RestaurantForm(forms.ModelForm):
    class Meta:
        model = Restaurant
        fields = ['name', 'city', 'address', 'mobile', 'description', 'img', ]
        labels = {
            'name': 'Restaurant Name', 'city': 'City', 'address': 'Address',
            'mobile': 'Mobile No', 'description': 'Description', 'img': 'Photo'
        }


class FoodForm(forms.ModelForm):
    class Meta:
        model = Food
        fields = ['name', 'img', 'price', 'person', 'available_at_time']
