from pyexpat import model
from attr import fields
from django import forms
from .models import ReviewWorker

class ReviewWorkerForm(forms.ModelForm):
    class Meta:
        model= ReviewWorker
        fields = '__all__'