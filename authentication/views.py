from multiprocessing import context
import re
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

from .models import CustomUser, Worker, WorkerCategory
from .forms import WorkerSignUpForm, CustomerSignUpForm, WorkerUpdateForm, CustomUserUpdateForm
# Create your views here.

class UserTypesRegistration(View):
    def get(self, request):
        return render(request, 'authentication/user_type_choose.html')


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
            form.save()
            messages.success(request, 'Account successfully created.')
            return redirect('authentication:login')
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
            form.save()
            messages.success(request, 'Account successfully created.')
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
            if user is not None:
                login(request, user)
                messages.success(
                    request, f"You are now logged in as {request.user.name}.")
                return redirect("dashboard")
            else:
                messages.error(request, "Invalid email or password.")
        else:
            messages.error(request, "Invalid email or password.")

        return render(request, 'authentication/login.html')


@method_decorator(login_required(login_url='/authentication/login'), name='dispatch')
class LogoutView(View):
    def get(self, request):
        logout(request)
        messages.success(request, f'You have been logged out.')
        return redirect('authentication:login')


@method_decorator(login_required(login_url='/authentication/login'), name='dispatch')
class WorkerProfile(View):
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
class CustomerProfile(View):
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
