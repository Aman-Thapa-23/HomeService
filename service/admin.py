from django.contrib import admin
from .models import Booking,WorkerAvailability, Contact

# Register your models here.

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display= ['customer', 'worker','booking_date', 'booking_time', 'status']
    
admin.site.register(WorkerAvailability)
admin.site.register(Contact)
