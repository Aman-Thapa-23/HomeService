from django.db import models
from authentication.models import CustomUser, Worker
from django.utils import timezone
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.kltb

class Booking(models.Model):
    STATUS =(
        ('Pending', 'Pending'),
        ('Accepted', 'Accepted'),
        ('Rejected', 'Rejected')
    )
    customer = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    worker = models.ForeignKey(Worker, on_delete=models.CASCADE)
    booking_date = models.DateField()
    booking_time = models.TimeField()
    problem_description = models.TextField()
    problem_picture = models.ImageField(null=True, blank=True, upload_to='problem_picture')
    status = models.CharField(choices=STATUS, default='Pending', max_length=20)
    is_complete = models.BooleanField(default=False)
    accepted_date = models.DateTimeField(auto_now_add=False, null=True, blank=True)

    def __str__(self):
        return f'{self.customer.name} book {self.worker.user.name}'
    

    class Meta:
        ordering = ['-booking_date']
 

class WorkerAvailability(models.Model):
    worker = models.OneToOneField(Worker, on_delete=models.CASCADE)
    date_from = models.DateTimeField()
    date_to = models.DateTimeField()
    unavailable_status = models.BooleanField('Make Unavailable', default=False)
