from django.contrib import admin
from .models import Guide, GuideAvailable, GuideBooking, Gender
# Register your models here.

admin.site.register(Guide)
admin.site.register(GuideAvailable)
admin.site.register(GuideBooking)
admin.site.register(Gender)
