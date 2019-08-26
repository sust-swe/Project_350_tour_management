from django.contrib import admin
from .models import Restaurant, Food, Orders, OrderDetail
# Register your models here.

admin.site.register(Restaurant)
admin.site.register(Food)
admin.site.register(Orders)
admin.site.register(OrderDetail)
