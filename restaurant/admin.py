from django.contrib import admin
from .models import RestaurantOwner, Restaurant, Food, Orders, OrderDetail
# Register your models here.

admin.site.register(Restaurant)
admin.site.register(RestaurantOwner)
admin.site.register(Food)
admin.site.register(Orders)
admin.site.register(OrderDetail)
