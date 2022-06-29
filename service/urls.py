from django.urls import path
from .views import BookingView, WorkerList, ServiceList

app_name='service'

urlpatterns = [
    path('<int:pk>/woker-booking-form', BookingView.as_view(), name='worker-booking-form'),
    path('worker-list/<int:pk>/', WorkerList.as_view(), name='worker-list'),
    path('service-list', ServiceList, name='service-list'),
]