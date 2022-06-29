from django import dispatch
from django.shortcuts import render, redirect
from authentication.models import WorkerCategory, Worker, CustomUser
from django.views import View
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from .forms import BookingForm
from .models import Booking

import datetime

# Create your views here.

def landingPage(request):
    services = WorkerCategory.objects.all()
    context = {
        'services': services
    }
    return render(request, 'landing.html', context)

@login_required
def LoggedInDashboard(request):
    return render(request, 'dashboard.html')


def about(request):
    return render(request, 'about_us.html')


def ServiceList(request):
    services = WorkerCategory.objects.all()
    context = {
        'services':services
    }
    return render(request, 'service/service_list.html', context)


@method_decorator(login_required(login_url='/authentication/login'), name='dispatch')
class BookingView(View):
    def get(self, request, pk):
        worker = Worker.objects.get(user__pk=pk)
        form = BookingForm(instance=worker)
        context = {
            'form': form,
            'worker':worker
        }
        return render(request, 'service/booking_form.html' ,context)

    def post(self, request, pk):
        worker = Worker.objects.get(user__pk=pk)
        form = BookingForm(request.POST, request.FILES, instance=worker)
        context = {
            'form': form,
            'worker':worker
        }
        if form.is_valid():
            booking_date = form.cleaned_data['booking_date']
            booking_time = form.cleaned_data['booking_time']
            date_and_time = datetime.datetime.combine(booking_date, booking_time)
            if date_and_time > datetime.datetime.now():
                booking = form.save(commit=False)
                booking.customer = request.user
                booking.worker = worker
                booking.save()
                messages.success(request, f'your booking request is successfully sent to {worker.user.name}.')
                return redirect('service:service-list')
            else:
                messages.error(request, 'Date or time must be greater than today date.')
        return render(request, 'service/booking_form.html', context)


@method_decorator(login_required(login_url='/authentication/login'), name='dispatch')
class WorkerList(View):
    def get(self, request, pk):
        service_category = WorkerCategory.objects.get(pk=pk)
        workers = Worker.objects.filter(category_name=service_category)
        context= {  
            'workers':workers,
            'service_category':service_category
        }
        return render(request, 'service/worker_list.html', context)


#worker list booked by customer for specific customer
@method_decorator(login_required(login_url='/authentication/login'), name='dispatch')
class CustomerBookingList(View):
    def get(self, request):
        customer = CustomUser.objects.get(request.user.pk)
        my_bookings = Booking.objects.filter(customer=customer)
        context = {
            'my_bookings':my_bookings
        }
        return render(request, 'service/my_booking_list.html', context)

    def post(self, request):
        pass

#customer list who booked the worker to specific worker
@method_decorator(login_required(login_url='/authentication/login'), name='dispatch')
class WorkerBookingRequestList(View):
    def get(self, request):
        pass

    def post(self, request):
        pass