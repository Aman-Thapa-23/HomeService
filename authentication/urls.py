from django.urls import path
from .views import WorkerSignUpView, CustomerSignUpView, UserTypesRegistration, LoginView, LogoutView, WorkerProfile, CustomerProfile

app_name = 'authentication'

urlpatterns = [
    path('user-type-choice', UserTypesRegistration.as_view(), name='user-type-choice'),
    path('worker-register', WorkerSignUpView.as_view(), name='worker-register'),
    path('customer-register', CustomerSignUpView.as_view(), name='customer-register'),
    path('login', LoginView.as_view(), name='login'),
    path('logout', LogoutView.as_view(), name='logout'), 
    path('worker-profile/<int:pk>/', WorkerProfile.as_view(), name='worker-profile'),
    path('cutomer-profile', CustomerProfile.as_view(), name='cutomer-profile'),
]