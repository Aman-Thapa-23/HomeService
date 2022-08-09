from django.urls import path
# from .views import SearchWorker, SearchCustomer
from .views import BookingView, WorkerList, ServiceList, UserStatistics ,CustomerBookingList ,WorkerBookingRequestList, BookingStatusView, WorkerAvailabilityView, ContactView
from django.views.decorators.csrf import csrf_exempt

app_name='service'

urlpatterns = [
    path('<int:pk>/woker-booking-form', BookingView.as_view(), name='worker-booking-form'),
    path('worker-list/<int:pk>', WorkerList.as_view(), name='worker-list'),
    path('service-list', ServiceList, name='service-list'),
    path('customer-booking-list', CustomerBookingList.as_view(), name='customer-booking-list'),
    path('woker-booking-request-list', WorkerBookingRequestList.as_view(), name='woker-booking-request-list'),
    path('booking-status', BookingStatusView, name='booking-status'),
    path('profile-statistics', UserStatistics, name='profile-statistics'),
    # path('search-worker', csrf_exempt(SearchWorker), name='search-worker'),
    # path('search-customer', csrf_exempt(SearchWorker), name='search-customer'),

    path('contact-form',ContactView.as_view(), name='contact-form'),

    path('worker-availability-form', WorkerAvailabilityView.as_view(), name='worker-availability-form'),
]