from django.urls import path
from .views import BookingView, WorkerList, ServiceList, CustomerBookingList ,WorkerBookingRequestList

app_name='service'

urlpatterns = [
    path('<int:pk>/woker-booking-form', BookingView.as_view(), name='worker-booking-form'),
    path('worker-list/<int:pk>/', WorkerList.as_view(), name='worker-list'),
    path('service-list', ServiceList, name='service-list'),
    path('customer-booking-list', CustomerBookingList.as_view(), name='customer-booking-list'),
    path('woker-booking-request-list', WorkerBookingRequestList.as_view(), name='woker-booking-request-list'),
]