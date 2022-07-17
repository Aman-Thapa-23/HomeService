from django.shortcuts import get_object_or_404, render, redirect
from authentication.models import WorkerCategory, Worker, CustomUser
from django.views import View
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from .forms import BookingForm
from .models import Booking
from django.http import JsonResponse
from django.db.models import Q

import json
import datetime

# Create your views here.


def landingPage(request):
    service_list = WorkerCategory.objects.all()
    context = {
        'service_list': service_list
    }
    return render(request, 'landing.html', context)


@login_required
def LoggedInDashboard(request):
    return render(request, 'dashboard2.html')


def about(request):
    return render(request, 'about_us.html')


def ServiceList(request):
    worker_services = WorkerCategory.objects.all()
    context = {
        'worker_services': worker_services
    }
    return render(request, 'service/service_list.html', context)


# Customer search box from worker list
@login_required
def SearchWorker(request):
    if request.method == "POST":
        search_str = json.loads(request.body).get('searchText')
        worker = Booking.objects.filter(worker__icontains=search_str, customer=request.user) | Booking.objects.filter(worker__user__address__icontains=search_str,  customer=request.user) | Booking.objects.filter(
            status__icontains=search_str,  customer=request.user)
        data = worker.values()

        return JsonResponse(list(data), safe=False)

# WOrker search for customer list


@login_required
def SearchCustomer(request):
    if request.method == "POST":
        search_str = json.loads(request.body).get('searchText')
        customer = Booking.objects.filter(
            Q(customer__icontains=search_str) &
            Q(customer__phone_number__icontains=search_str) &
            Q(customer__address__icontains=search_str)
        )
        data = customer.values()

        return JsonResponse(list(data), safe=False)


@method_decorator(login_required(login_url='/authentication/login'), name='dispatch')
class BookingView(View):
    def get(self, request, pk):
        worker = Worker.objects.get(user__pk=pk)
        form = BookingForm(instance=worker)
        context = {
            'form': form,
            'worker': worker
        }
        return render(request, 'service/booking_form.html', context)

    def post(self, request, pk):
        worker = Worker.objects.get(user__pk=pk)
        form = BookingForm(request.POST, request.FILES)
        context = {
            'form': form,
            'worker': worker
        }
        if form.is_valid():
            booking_date = form.cleaned_data['booking_date']
            booking_time = form.cleaned_data['booking_time']
            date_and_time = datetime.datetime.combine(
                booking_date, booking_time)
            if date_and_time > datetime.datetime.now():
                booking = form.save(commit=False)
                booking.customer = request.user
                booking.worker = worker
                print(booking)
                booking.save()
                messages.success(
                    request, f'your booking request is successfully sent to {worker.user.name}.')
                return redirect('service:service-list')
            else:
                messages.error(
                    request, 'Date or time must be greater than today date.')
        return render(request, 'service/booking_form.html', context)


@method_decorator(login_required(login_url='/authentication/login'), name='dispatch')
class WorkerList(View):
    def get(self, request, pk):
        service_category = WorkerCategory.objects.get(pk=pk)
        workers = Worker.objects.filter(category_name=service_category)
        context = {
            'workers': workers,
            'service_category': service_category
        }
        return render(request, 'service/worker_list.html', context)


# worker list booked by customer for specific customer
@method_decorator(login_required(login_url='/authentication/login'), name='dispatch')
class CustomerBookingList(View):
    def get(self, request):
        my_bookings = Booking.objects.filter(
            customer=request.user).order_by('-booking_date')
        paginator = Paginator(my_bookings, 7)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context = {
            'my_bookings': my_bookings,
            'page_obj': page_obj
        }
        return render(request, 'service/customer_booking_list.html', context)


# customer list who booked the worker to specific worker
@method_decorator(login_required(login_url='/authentication/login'), name='dispatch')
class WorkerBookingRequestList(View):
    def get(self, request):
        worker = Worker.objects.get(pk=request.user)
        booking_requests = Booking.objects.filter(
            worker=worker).order_by('-booking_date')
        paginator = Paginator(booking_requests, 7)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context = {
            'booking_requests': booking_requests,
            'page_obj': page_obj
        }
        return render(request, 'service/worker_booking_request.html', context)


def BookingStatusView(request):
    booking_id = request.GET.get('booking_id')
    coming_status = request.GET.get('status')
    booking = Booking.objects.get(pk=booking_id)
    if coming_status == 'Accept':
        booking.status = 'Accepted'
        booking.save()
        messages.success(
            request, f'Your booking request is accepted by {booking.worker.user.name}.')
        return redirect('service:customer-booking-list')
    if coming_status == 'Reject':
        booking.status = 'Rejected'
        booking.save()
        messages.success(
            request, f'Your booking request is rejected by {booking.worker.user.name}.')
        return redirect('service:customer-booking-list')
    return render(request, 'service/worker_booking_request.html')


@login_required
def UserStatistics(request):
    if request.user.is_customer:
        my_bookings = Booking.objects.filter(
                customer=request.user)
        accepted = Booking.objects.filter(customer=request.user, status="Accepted")
        rejected = Booking.objects.filter(customer=request.user, status ="Rejected")
        pending = Booking.objects.filter(customer=request.user, status ="Pending")
        context = {
        'my_bookings':my_bookings,
        'accepted':accepted,
        'rejected':rejected,
        'pending':pending
        }
        return render(request, 'service/profile_statistics.html', context)

    if request.user.is_worker:
        worker = Worker.objects.get(pk=request.user)
        booking_requests = Booking.objects.filter(
            worker=worker)
        accepted = Booking.objects.filter(worker=worker, status="Accepted")
        rejected = Booking.objects.filter(worker=worker, status ="Rejected")
        pending = Booking.objects.filter(worker=worker, status ="Pending")
        context = {
            'booking_requests':booking_requests,
            'accepted':accepted,
            'rejected':rejected,
            'pending':pending
        }
        return render(request, 'service/profile_statistics.html', context)
