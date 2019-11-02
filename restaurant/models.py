from django.db import models
from django.contrib.auth.models import User
from django.db.models import Q
from homepage.models import City, UserDetail, Address, MyChoice, Country
from homepage.base import *

# Create your models here.


class Restaurant(models.Model):
    user_detail = models.ForeignKey(
        UserDetail, on_delete=models.CASCADE, default=100)
    name = models.CharField(max_length=255)
    country = models.ForeignKey(Country, on_delete=models.CASCADE, null=True, default=None)
    city = models.ForeignKey(City, on_delete=models.CASCADE, null=True, default=None)
    mobile = models.IntegerField(default=None, null=True, blank=True)
    description = models.CharField(max_length=255, null=True, blank=True)
    img = models.ImageField(upload_to='RestaurantPhoto', null=True, blank=True, default=None)

    class Meta:
        ordering = ['user_detail']

    def __str__(self):
        return self.name

    def clean_fields(self, exclude=None):
        super().clean_fields(exclude=exclude)
        if not (exclude and "user_detail" in exclude):
            if Restaurant.objects.filter(user_detail=self.user_detail, name=self.name).exists():
                if Restaurant.objects.get(user_detail=self.user_detail, name=self.name).id != self.id:
                    raise ValidationError("You have already a restaurant of the same name")


class Food(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    img = models.ImageField(upload_to='FoodPhoto',
                            null=True, blank=True, default=None)
    price = models.FloatField()
    person = models.PositiveIntegerField(default=1, blank=True)
    available_at_time = models.CharField(
        max_length=255, choices=MyChoice.Eating_time)
    description = models.CharField(
        max_length=255, blank=True, null=True, default=None)

    class Meta:
        ordering = ['restaurant']

    def clean_fields(self, exclude=None):
        super().clean_fields(exclude=exclude)
        if not (exclude and "restaurant" in exclude):
            if Food.objects.filter(restaurant=self.restaurant, name=self.name).exists():
                if Food.objects.get(restaurant=self.restaurant, name=self.name).id != self.id:
                    raise ValidationError("You have already a restaurant of the same name")
        if self.price < 0:
            raise ValidationError({"price": "Price cannot be negative"})
        if self.person < 1:
            raise ValidationError({"person": "Select at least 1 person"})


class Order(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    bill = models.FloatField()
    order_time = models.DateTimeField()
    status = models.CharField(max_length=255, null=True)

    class Meta:
        ordering = ['-order_time']


class OrderDetail(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True)
    food = models.ForeignKey(Food, on_delete=models.CASCADE)
    quantity = models.IntegerField()

    class Meta:
        ordering = ['order']


class Cart(models.Model):
    owner = models.OneToOneField(User, on_delete=models.CASCADE)
    restaurant = models.ForeignKey(
        Restaurant, on_delete=models.CASCADE, null=True, default=None)
    bill = models.FloatField(null=True, default=None)

    class Meta:
        ordering = ["owner"]


class CartDetail(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    food = models.ForeignKey(Food, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    # erase all the items from other restaurant


# pip install Pillow
# python manage.py makemigrations
# python manage.py sqlmigrate @appname @migrationid
# python manage.py migrate
# django admin username-shoaib password-1234
# python manage.py createsuperuser @username
# python manage.py changepassword @username
# python manage.py createsuperuser -h
