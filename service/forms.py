from dataclasses import fields
from django import forms
from .models import Booking, WorkerAvailability

# date picker widget




class DatePickerInput(forms.DateInput):
    input_type = 'date'
    input_formats=['%m/%d/%y']

# time picker widget
class TimePickerInput(forms.TimeInput):
    input_type = 'time'
    input_formats=['%H:%M %p']

class DateTimePickerInput(forms.DateTimeInput):
    input_type= 'datetime-local'
    input_formats=['%m/%d/%y %H:%M %p']
    
class BookingForm(forms.ModelForm):
    class Meta:
        model= Booking
        fields = ('booking_date', 'booking_time', 'problem_description', 'problem_picture')

        widgets = {
            'booking_date': DatePickerInput(),
            'booking_time': TimePickerInput()
        }

        # widgets = {
        #     'booking_date': forms.DateField(widget=forms.DateInput(attrs={'class': 'datepicker'}),format='%Y-%m-%d'),
        #     'booking_time': forms.DateField(widget=forms.DateInput(attrs={'class': 'timepicker'}),format="%H:%M")
        # }


class WorkerAvailabilityForm(forms.ModelForm):
    class Meta:
        model = WorkerAvailability
        fields = ('date_from', 'date_to')
        widgets = {
            'date_from': DateTimePickerInput(),
            'date_to': DateTimePickerInput()
        }
