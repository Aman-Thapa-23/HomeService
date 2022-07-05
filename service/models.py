from django.db import models
from authentication.models import CustomUser, Worker
from django.utils import timezone

# Create your models here.

class Booking(models.Model):
    customer = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    worker = models.ForeignKey(Worker, on_delete=models.CASCADE)
    booking_date = models.DateField()
    booking_time = models.TimeField()
    problem_description = models.TextField()
    problem_picture = models.ImageField(null=True, blank=True, upload_to='problem_picture')
    accepted_status = models.BooleanField(default=False)
    is_complete = models.BooleanField(default=False)
    accepted_date = models.DateTimeField(auto_now_add=False, null=True, blank=True)

    def __str__(self):
        return f'{self.customer.name} book {self.worker.user.name}'
    

    class Meta:
        ordering = ['-booking_date']
 