from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect

from accounts_app.forms import CustomerRegistrationForm, UserLoginForm


# Create your views here.
def customer_register(request):
    if request.method == 'POST':
        form=CustomerRegistrationForm(request.POST)
        if form.is_valid():
            form.save()

            messages.success(request,'Your account has been created!')

            return redirect("customer_register")
    else:
        form=CustomerRegistrationForm()
    return render(request,'customer_register.html',{'form':form})



def customer_login(request):

    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)
            return redirect("customer_dashboard")

        messages.error(request, 'Invalid username and/or password.')

    return render(request, 'customer_login.html')
def customer_dashboard(request):
    return render(request,'customer_dashboard.html')

def customer_logout(request):
    if request.method == 'POST':
        logout(request)
        messages.success(request,'You are logged out!')
        return redirect("customer_login")
    return render(request,'customer_dashboard.html')

