from email import message
from django.db import models
from django.dispatch import receiver
from authentication.models import CustomUser

# Create your models here.


class Notification(models.Model):    
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='user_sender')
    receiver = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='user_receiver')
    message = models.CharField(max_length=200)
