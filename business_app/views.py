from email import message
from multiprocessing import resource_sharer

from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.db import transaction
from django.db.models import Model, Q
from django.shortcuts import render, redirect
from business_app.models import business as Business, business, customer
from accounts_app.models import User
from business_app.forms import BusinessRegistrationForm, BusinessLoginForm, BusinessProfileForm, LoyaltySettingsForm, CustomerSearchForm, TransactionForm



def business_register(request):
    if request.method == 'POST':
        form=BusinessRegistrationForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
                user=User.objects.create_user(username=form.cleaned_data['username'],email=form.cleaned_data['business_email'], password=form.cleaned_data['password1'])
                business=form.save(commit=False)
                business.owner=user
                business.approval_status='pending'
                business.save()
            messages.success(request, 'Registered Successfully, please wait for approval')
            return redirect('business_register')
    else:
        form=BusinessRegistrationForm()
    return render(request,'business_register.html',{'form':form})



def business_login(request):
    if request.method == 'POST':
        form = BusinessLoginForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(
                request,
                username=username,
                password=password
            )

            if user is not None:
                try:
                    business_details = user.business

                    if business_details.approval_status == 'approved':
                        login(request, user)
                        return redirect('business_dashboard')
                    else:
                        messages.error(request, 'Approval pending')

                except Business.DoesNotExist:
                    messages.error(request, 'Account was not created!')

            else:
                messages.error(request, 'Invalid username or password')

    else:
        form = BusinessLoginForm()

    return render(
        request,
        'business_login.html',
        {'form': form}
    )

def business_dashboard(request):
    try:
        business_details=request.user.business
    except business.DoesNotExist:
        return redirect('business_login')
    if business_details.approval_status != 'approved':
        return redirect('business_login')
    return render(request, 'business_dashboard.html',{'business':business_details})

def business_profile(request):
    try:
        business_details=request.user.business
    except business.DoesNotExist:
        return redirect('business_login')
    if request.method == 'POST':
        form=BusinessProfileForm(request.POST, instance=business_details)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile Updated Successfully')
            return redirect('business_profile')
    else:
        form=BusinessProfileForm(instance=business_details)
    return render(request, 'business_profile.html',{'form':form})


def loyalty_settings(request):
    try:
        business_details=request.user.business
    except business.DoesNotExist:
        return redirect('business_login')
    if request.method=='POST':
        form=LoyaltySettingsForm(request.POST, instance=business_details)
        if form.is_valid():
            form.save()
            messages.success(request, 'Loyalty settings updated.')
            return redirect('loyalty_settings')
    else:
        form=LoyaltySettingsForm(instance=business_details)
    return render(request, 'loyalty_settings.html',{'form':form, 'business':business_details})



def add_customer(request):
    try:
        business_details=request.user.business
    except business.DoesNotExist:
        return redirect('business_login')
    if request.method=='POST':
        form=CustomerSearchForm(request.POST)
        if form.is_valid():
            customer_email=form.cleaned_data['customer_email']
            customer_user=User.objects.filter(email=customer_email).first()
            if customer_user is None:
                messages.error(request, 'No customer available with this mail')
            else:
                customer_membership=customer.objects.filter(user=customer_user, business=business_details).first()
                if customer_membership:
                    messages.warning(request, 'This customer is already added')
                else:
                    customer.objects.create(user=customer_user, business=business_details)
                    messages.success(request, 'Customer Added')
            return redirect('add_customer')
    else:
        form=CustomerSearchForm()
    return render(request, 'add_customer.html',  {'form': form})

def customer_list(request):
    try:
        business_details = request.user.business
    except business.DoesNotExist:
        return redirect('business_login')
    customers=business_details.customer.select_related('user').all()
    search_query=request.GET.get('q','').strip()
    if search_query:
        customers=customers.filter(
            Q(user__first_name__icontains=search_query) |
            Q(user__last_name__icontains=search_query)
        )
    return render(request, 'customer_list.html', {'customers':customers, 'search_query':search_query})


def add_transactions(request):
    try:
        business_details = request.user.business
    except Business.DoesNotExist:
        return redirect('business_login')
    if request.method=='POST':
        form=TransactionForm(request.POST)
        form.fields['customer'].queryset=customer.objects.filter(business=business_details)
        if form.is_valid():
            customer_details=form.cleaned_data['customer']
            purchase_amount=form.cleaned_data['purchase_amount']
            if not business_details.loyalty_program_active:
                messages.error(request, 'Inactive...')
            elif purchase_amount<business_details.minimum_purchase_amount:
                messages.error(request, 'purchase amount is below of minimum...')
            else:
                points=int(purchase_amount//business_details.purchase_amount_for_points)*business_details.points_earned

                transaction_details=form.save(commit=False)
                transaction_details.business=business_details
                transaction_details.points_earned=points
                transaction_details.save()

                messages.success(request, f'Done - {points} earned ')
                return redirect('add_transactions')
    else:
        form=TransactionForm()
        form.fields['customer'].queryset=customer.objects.filter(business=business_details)
    return render(request, 'add_transaction.html', {'form':form})