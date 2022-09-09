from django.contrib import admin
from .models import ReviewWorker

# Register your models here.

@admin.register(ReviewWorker)
class ReviewWorkerAdmin(admin.ModelAdmin):
    list_display= ['customer', 'worker', 'rate', 'comment', 'review_date']