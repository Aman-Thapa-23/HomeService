from django.db import models
from authentication.models import CustomUser, Worker
from django.utils import timezone

# Create your models here.

class Booking(models.Model):
    STATUS =(
        ('pending', 'pending'),
        ('denied', 'denied'),
        ('accepted', 'accepted'),
    )

    customer = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    worker = models.ForeignKey(Worker, on_delete=models.CASCADE)
    booking_date = models.DateField()
    booking_time = models.TimeField()
    problem_description = models.TextField()
    problem_picture = models.ImageField(null=True, blank=True, upload_to='problem_picture')
    is_accept = models.BooleanField(default=False)
    is_denied = models.BooleanField(default=False)
    is_complete = models.BooleanField(default=False)
    accepted_date = models.DateTimeField(auto_now_add=False, null=False, blank=True)
    status = models.CharField(max_length=10, choices=STATUS, default='pending')

    def __str__(self):
        return f'{self.customer} book {self.worker}'
    

    class Meta:
        ordering = ['-booking_date']
