from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from authentication.models import CustomUser, Worker

# Create your models here.
class ReviewWorker(models.Model):
    RATING = (
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5', '5'),
    )
    worker = models.ForeignKey(Worker, on_delete=models.CASCADE)
    customer = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    comment = models.TextField(max_length=300)
    rate = models.CharField(max_length=10, choices=RATING, null=True, blank=True)
    review_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.worker} has been rated {self.rate} by {self.customer}.' 