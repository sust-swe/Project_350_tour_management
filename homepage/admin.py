from django.contrib import admin
from .models import City, UserDetail


# Register your models here.
# admin.site.register(@class)
admin.site.register(City)
admin.site.register(UserDetail)

