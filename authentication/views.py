from django.shortcuts import render, redirect
from django.views import View
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from django.contrib.auth import update_session_auth_hash

from .models import CustomUser, Worker, WorkerCategory
from .forms import WorkerSignUpForm, CustomerSignUpForm, WorkerUpdateForm, CustomUserUpdateForm, UserPasswordChangeForm
from .utils import accout_activation_token
import threading
# Create your views here.

class UserTypesRegistration(View):
    def get(self, request):
        return render(request, 'authentication/user_type_choose.html')


class EmailThread(threading.Thread):
    def __init__(self, email):
        self.email = email
        threading.Thread.__init__(self)

    def run(self):
        self.email.send(fail_silently=False)

class VerificationView(View):
    def get(self, request, uidb64, token):
        try:
            id = force_str(urlsafe_base64_decode(uidb64))
            user = CustomUser.objects.get(pk=id)

            if not accout_activation_token.check_token(user, token):
                return redirect('authentication:login' + '?message= User is already activated.')

            if user.is_active:
                return redirect('authentication:login')
            user.is_active = True
            user.save()

            messages.success(request, 'Account activated successfully.')
            return redirect('authentication:login')
         
        except Exception as ex:
            pass

        return redirect('authentication:login')

class CustomerSignUpView(View):
    def get(self, request):
        form = CustomerSignUpForm()
        context = {
            'form': form
        }
        return render(request, 'authentication/customer_register.html', context)

    def post(self, request):
        form = CustomerSignUpForm(request.POST)
        context = {
            'form': form,
            'fieldvalues': request.POST
        }

        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            phone_number = form.cleaned_data['phone_number']
            address = form.cleaned_data['address']
            password = form.cleaned_data['password1']

            if not CustomUser.objects.filter(email=email).exists():
                user = CustomUser.objects.create_user(name=name, email=email, phone_number= phone_number, address=address, password=password)
                user.set_password(password)
                user.is_active = False
                user.is_customer = True
                user.save()

                current_site = get_current_site(request)
                email_body = {
                    'user': user,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': accout_activation_token.make_token(user)
                }
                link = reverse('authentication:activate', kwargs={'uidb64':email_body['uid'], 'token':email_body['token']})
                activate_url = 'http://'+current_site.domain+link
                email_subject = "Activate your account"
                email_body = f"Hi, {user.name}. Please click this link to verify your account\n" + activate_url
                email = EmailMessage(
                    email_subject,
                    email_body,
                    'noreply@gmail.com',
                    [email]
                )
                EmailThread(email).start()
                messages.success(request, 'Account successfully created. Please check your email to activate your account')
                return redirect('authentication:customer-register')
        return render(request, 'authentication/customer_register.html', context)


class WorkerSignUpView(View):
    def get(self, request):
        form = WorkerSignUpForm()
        context = {
            'form': form
        }
        return render(request, 'authentication/worker_register.html', context)

    def post(self, request):
        form = WorkerSignUpForm(request.POST)
        context = {
            'form': form,
            'fieldvalues': request.POST
        }

        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            phone_number = form.cleaned_data['phone_number']
            address = form.cleaned_data['address']
            password = form.cleaned_data['password1']
            category_name = form.cleaned_data['category_name']

            if not CustomUser.objects.filter(email=email).exists():
                user = CustomUser.objects.create_user(name=name, email=email, phone_number= phone_number, address=address, password=password)
                user.set_password(password)
                user.is_worker = True
                user.is_active = False
                user.save()
                worker = Worker.objects.create(user=user)
                worker.category_name = category_name
                worker.save()

                current_site = get_current_site(request)
                email_body = {
                    'user': user,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': accout_activation_token.make_token(user)
                }
                link = reverse('authentication:activate', kwargs={'uidb64':email_body['uid'], 'token':email_body['token']})
                activate_url = 'http://'+current_site.domain+link
                email_subject = "Activate your account"
                email_body = f"Hi, {user.name}. Please click this link to verify your account\n" + activate_url
                email = EmailMessage(
                    email_subject,
                    email_body,
                    'noreply@gmail.com',
                    [email]
                )
                EmailThread(email).start()
                messages.success(request, 'Account successfully created. Please check your email to activate your account')
                return redirect('authentication:login')
        return render(request, 'authentication/worker_register.html', context)


class LoginView(View):
    def get(self, request):
        return render(request, 'authentication/login.html')

    def post(self, request):
        email = request.POST['email']
        password = request.POST['password']

        if email and password:
            user = authenticate(request, email=email, password=password)
            if user:
                if user.is_active:
                    login(request, user)
                    messages.success(
                        request, f"You are now logged in as {request.user.name}.")
                    return redirect("dashboard")
                messages.error(request, "Account is not active. please check your email.")
                return render(request, 'authentication/login.html')
            else:
                messages.error(request, "Invalid email or password.")
        else:
            messages.error(request, "Invalid email or password.")

        return render(request, 'authentication/login.html')


@method_decorator(login_required(login_url='/authentication/login'), name='dispatch')
class LogoutView(View, LoginRequiredMixin):
    def get(self, request):
        logout(request)
        messages.success(request, f'You have been logged out.')
        return redirect('authentication:login')


@method_decorator(login_required(login_url='/authentication/login'), name='dispatch')
class WorkerProfile(View, LoginRequiredMixin):
    def get(self, request, pk):
        worker = Worker.objects.get(user__pk=pk)
        cu_form = CustomUserUpdateForm(instance=request.user)
        w_form = WorkerUpdateForm(instance=worker)

        context = {
            'cu_form': cu_form,
            'w_form': w_form
        }

        return render(request, 'authentication/worker_profile.html', context)

    def post(self, request, pk):
        worker = Worker.objects.get(user__pk=pk)
        cu_form = CustomUserUpdateForm(request.POST, instance=request.user)
        w_form = WorkerUpdateForm(
            request.POST, request.FILES, instance=worker)

        context = {
            'cu_form': cu_form,
            'w_form': w_form
        }

        if cu_form.is_valid() and w_form.is_valid():
            cu_form.save()
            w_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('dashboard')
        return render(request, 'authentication/worker_profile.html', context)


@method_decorator(login_required(login_url='/authentication/login'), name='dispatch')
class CustomerProfile(View, LoginRequiredMixin):
    def get(self, request):
        cu_form = CustomUserUpdateForm(instance=request.user)
        context = {
            'cu_form': cu_form,
        }

        return render(request, 'authentication/customer_profile.html', context)

    def post(self, request):
        cu_form = CustomUserUpdateForm(request.POST, instance=request.user)
        context = {
            'cu_form': cu_form,
        }
        if cu_form.is_valid():
            cu_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('dashboard')
        return render(request, 'authentication/customer_profile.html', context)


@method_decorator(login_required(login_url='/authentication/login'), name='dispatch')
class ChangePasswordView(View, LoginRequiredMixin):
    def get(self, request):
        form = UserPasswordChangeForm(request.user)
        context = {
            'form':form
        }
        return render(request, 'authentication/change_password.html', context)
    def post(self, request):
        form = UserPasswordChangeForm(request.user, request.POST)
        context = {
            'form':form
        }
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'your password successfully changed!')
            return redirect('dashboard')
        else:
            messages.error(request, 'Please correct the error below.')
        return render(request, 'authentication/change_password.html', context)

    
    