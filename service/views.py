from django.shortcuts import get_object_or_404, render, redirect
from authentication.models import WorkerCategory, Worker, CustomUser
from django.views import View
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
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
    return render(request, 'dashboard2.html')

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
        form = BookingForm(request.POST, request.FILES)
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
                print(booking)
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
        my_bookings = Booking.objects.filter(customer=request.user).order_by('-booking_date')
        paginator = Paginator(my_bookings, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context = {
            'my_bookings':my_bookings,
            'page_obj':page_obj
        }
        return render(request, 'service/customer_booking_list.html', context)

#customer list who booked the worker to specific worker
@method_decorator(login_required(login_url='/authentication/login'), name='dispatch')
class WorkerBookingRequestList(View):
    def get(self, request):
        worker = Worker.objects.get(pk=request.user)
        bookings_request = Booking.objects.filter(worker=worker).order_by('-booking_date')
        paginator = Paginator(bookings_request, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context = {
            'bookings_request':bookings_request,
            'page_obj':page_obj
        }
        return render(request, 'service/worker_booking_request.html', context)


def BookingStatusView(request):
    if request.is_ajax():
        id=request.GET.get('id')
        st=get_object_or_404(Booking,pk=id)
        print(st.status)
        if st.status == False:
            st.status=True
            # notice = get_object_or_404(Notice, status=True)
            # notice.status=False#make previous inactive
            # notice.save()
            st.save()
        else:
            st.status=False
            st.save()

        booking_data = Booking.objects.all()

    '''Due to   design fluctuation, I am rendering to notice_list.html'''
    return render(request, 'admin/notices/notice_list.html', {'notices':booking_data})