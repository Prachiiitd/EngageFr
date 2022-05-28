from django.contrib import admin
from .models import Customer, CameraIP

# Register your models here.

admin.site.register(Customer)  # Register the Customer model in the admin site
admin.site.register(CameraIP)  # Register the CameraIP model in the admin site
