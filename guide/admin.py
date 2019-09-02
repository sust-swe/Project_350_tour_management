from django.contrib import admin
from .models import Guide, GuideAvailable, GuideBooking
# Register your models here.

admin.site.register(Guide)
admin.site.register(GuideAvailable)
admin.site.register(GuideBooking)
