from django.contrib import admin
from .models import Residence, Space, SpaceAvailable, SpaceBooking


# Register your models here.
admin.site.register(Residence)
admin.site.register(Space)
admin.site.register(SpaceBooking)
admin.site.register(SpaceAvailable)
