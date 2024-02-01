from django.contrib import admin
from .models import Citizen, CustomUser

# Register your models here.
admin.site.register(Citizen)
admin.site.register(CustomUser)