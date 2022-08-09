from django.contrib import admin
from .models import Booking,WorkerAvailability, Contact

# Register your models here.

admin.site.register(Booking)
admin.site.register(WorkerAvailability)
admin.site.register(Contact)
