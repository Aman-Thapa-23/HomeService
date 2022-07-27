from django.urls import path
# from .views import PasswordResetView, CompletePasswordReset
from .views import WorkerSignUpView, CustomerSignUpView, UserTypesRegistration, LoginView, LogoutView, WorkerProfile, CustomerProfile, VerificationView, ChangePasswordView

app_name = 'authentication'

urlpatterns = [
    path('user-type-choice', UserTypesRegistration.as_view(), name='user-type-choice'),

    # email verification
    path('activate/<uidb64>/<token>', VerificationView.as_view(), name='activate'),

    path('worker-register', WorkerSignUpView.as_view(), name='worker-register'),
    path('customer-register', CustomerSignUpView.as_view(), name='customer-register'),
    path('login', LoginView.as_view(), name='login'),
    path('logout', LogoutView.as_view(), name='logout'), 
    
    #worker profile
    path('worker-profile/<int:pk>/', WorkerProfile.as_view(), name='worker-profile'),
    #Customer Progile
    path('cutomer-profile', CustomerProfile.as_view(), name='cutomer-profile'),
    path('change-password', ChangePasswordView.as_view(), name='change-password'),

    # #password reset request
    # path('request-password-reset', PasswordResetView.as_view(), name='password-reset'),
    # #link for reseting password
    # path('reset-new-password/<uidb64>/<token>', CompletePasswordReset.as_view(), name='reset-new-password'),
]