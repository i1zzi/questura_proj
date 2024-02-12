from django.contrib import admin
from .models import Citizen, CustomUser, Slot_Type, Appointment

# Register your models here.
admin.site.register(Citizen)
admin.site.register(CustomUser)
admin.site.register(Slot_Type)
admin.site.register(Appointment)