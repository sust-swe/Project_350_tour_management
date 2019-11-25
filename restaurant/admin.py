from django.contrib import admin
from .models import Restaurant, Food, Order, OrderDetail
# Register your models here.

admin.site.register(Restaurant)
admin.site.register(Food)
admin.site.register(Order)
admin.site.register(OrderDetail)
