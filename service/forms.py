from django import forms
from .models import Booking

# date picker widget
class DatePickerInput(forms.DateInput):
    input_type = 'date'
    input_formats=['%m/%d/%y']

# time picker widget
class TimePickerInput(forms.TimeInput):
    input_type = 'time'
    input_formats=['%H:%M %p']


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