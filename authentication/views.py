from multiprocessing import context
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages


from .models import CustomUser, Worker, WorkerCategory
from .forms import WorkerSignUpForm, CustomerSignUpForm
# Create your views here.

def landingPage(request):
    return render(request, 'landing.html')

def LoggedInDashboard(request):
    return render(request, 'dashboard.html')

class UserTypesRegistration(View):
    def get(self, request):
        return render(request, 'authentication/user_type_choose.html')

class CustomerSignUpView(View):
    def get(self, request):
        form = CustomerSignUpForm()
        context ={
            'form':form
        }
        return render(request, 'authentication/customer_register.html', context)
    
    def post(self, request):
        form = CustomerSignUpForm(request.POST)
        context = {
            'form':form,
            'fieldvalues':request.POST
        }

        if form.is_valid():
            form.save()
            messages.success(request, 'Account successfully created.')
            return redirect('authentication:login')
        return render(request, 'authentication/customer_register.html', context)

class WorkerSignUpView(View):
    def get(self, request):
        form = WorkerSignUpForm()
        context ={
            'form':form
        }
        return render(request, 'authentication/worker_register.html', context)
    
    def post(self, request):
        form = WorkerSignUpForm(request.POST)
        context = {
            'form':form,
            'fieldvalues':request.POST
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
                messages.success(request, f"You are now logged in as {request.user.name}.")
                return redirect("dashboard")
            else:
                messages.error(request,"Invalid email or password.")
        else:
            messages.error(request,"Invalid email or password.")
        
        return render(request, 'authentication/login.html')


class LogoutView(View):
    def get(self, request):
        logout(request)
        messages.success(request, f'You have been logged out.')
        return redirect('authentication:login')