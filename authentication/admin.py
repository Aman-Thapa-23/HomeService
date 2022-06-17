from django.contrib import admin
from .models import CustomUser, Worker, WorkerCategory

# Register your models here.

admin.site.register(CustomUser)
admin.site.register(Worker)
admin.site.register(WorkerCategory)
