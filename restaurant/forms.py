from django import forms
from .models import Restaurant, Food


class RestaurantForm(forms.ModelForm):
    description = forms.CharField(max_length=255, widget=forms.TextInput(), required=False)

    class Meta:
        model = Restaurant
        exclude = ['user_detail']
        labels = {
            'name': 'Restaurant Name', 'city': 'City', 'address': 'Address',
            'mobile': 'Mobile No', 'description': 'Description', 'img': 'Photo'
        }


class FoodForm(forms.ModelForm):
    class Meta:
        model = Food
        exclude = ['restaurant']
