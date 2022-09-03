from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from authentication.models import CustomUser, Worker

# Create your models here.
class ReviewWorker(models.Model):
    worker = models.ForeignKey(Worker, on_delete=models.CASCADE)
    customer = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    comment = models.TextField('Review', null=False, blank=False)
    rate = models.IntegerField(default=0, validators=[
        MaxValueValidator(5),
        MinValueValidator(0)
    ])
    review_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.worker} has been rated {self.rate} by {self.customer}.' 