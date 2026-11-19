from email import message
from multiprocessing import resource_sharer
from django.db import transaction as db_transaction
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.db import transaction
from django.db.models import Model, Q
from django.shortcuts import render, redirect, get_object_or_404
from business_app.models import business as Business, business, customer, reward, redemption
from accounts_app.models import User
from business_app.forms import BusinessRegistrationForm, BusinessLoginForm, BusinessProfileForm, LoyaltySettingsForm, CustomerSearchForm, TransactionForm, RewardForm



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
    total_customers=business_details.customers.count()
    total_transactions=business_details.transactions.count()
    total_points_issued=sum(business_details.transactions.values_list('points_earned',flat=True))
    total_sales = sum(business_details.transactions.values_list('purchase_amount', flat=True))

    return render(request, 'business_dashboard.html',{'business':business_details,'total_customers': total_customers,
        'total_transactions': total_transactions,
        'total_points_issued': total_points_issued,
        'total_sales': total_sales,})

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
            elif business_details.purchase_amount_for_points <= 0:
                messages.error(request,'Invalid - Purchase amount per point must be greater than zero.')
            elif purchase_amount < business_details.minimum_purchase_amount:
                messages.error(request,'Purchase amount is below the minimum required amount.')
            else:
                points = int(purchase_amount // business_details.purchase_amount_for_points) * business_details.points_earned

                transaction_details=form.save(commit=False)
                transaction_details.business=business_details
                transaction_details.points_earned=points
                transaction_details.save()
                customer_details.loyalty_points += points
                customer_details.save()

                messages.success(request, f'Done - {points} points earned ')
                return redirect('add_transactions')
    else:
        form=TransactionForm()
        form.fields['customer'].queryset=customer.objects.filter(business=business_details)
    return render(request, 'add_transaction.html', {'form':form})

def transaction_history(request):
    try:
        business_details = request.user.business
    except Business.DoesNotExist:
        return redirect('business_login')
    transactions=business_details.transactions.select_related('customer__user').order_by('-created_at')
    return render(request, 'transaction_history.html', {'transactions':transactions})

def add_reward(request):
    try:
        business_details = request.user.business
    except Business.DoesNotExist:
        return redirect('business_login')
    if request.method=='POST':
        form=RewardForm(request.POST)
        if form.is_valid():
            reward_detail=form.save(commit=False)
            reward_detail.business=business_details
            reward_detail.save()

            messages.success(request, 'Reward Added')
    else:
        form=RewardForm()
    return render(request, 'add_reward.html', {'form': form})

def reward_list(request):
    try:
        business_details = request.user.business
    except Business.DoesNotExist:
        return redirect('business_login')
    rewards=business_details.rewards.all().order_by('-created_at')
    return render(request, 'reward_list.html', {'rewards':rewards})

def edit_reward(request, reward_id):
    try:
        business_details = request.user.business
    except Business.DoesNotExist:
        return redirect('business_login')
    reward_details=get_object_or_404(reward, id=reward_id, business=business_details)
    if request.method=='POST':
        form=RewardForm(request.POST, instance=reward_details)
        if form.is_valid():
            form.save()
            messages.success(request, 'Reward Updated')
            return redirect('reward_list')
    else:
        form=RewardForm(instance=reward_details)
    return render(request, 'edit_reward.html', {'form': form, 'reward_details':reward_details})

def toggle_reward_status(request,reward_id):
    try:
        business_details = request.user.business
    except Business.DoesNotExist:
        return redirect('business_login')
    reward_details=get_object_or_404(reward, id=reward_id, business=business_details)
    if request.method=='POST':
        reward_details.is_active= not reward_details.is_active
        reward_details.save()

        messages.success(request, 'Reward Updated')
    return redirect('reward_list')

def redemption_requests(request):
    try:
        business_details = request.user.business
    except Business.DoesNotExist:
        return redirect('business_login')
    redemptions=redemption.objects.filter(reward__business=business_details).select_related('customer__user','reward').order_by('-created_at')
    return render(request, 'redemption_requests.html', {'redemptions':redemptions})


def update_redemption_status(request, redemption_id):

    if request.method != 'POST':
        return redirect('redemption_requests')

    try:
        business_details = request.user.business
    except Business.DoesNotExist:
        return redirect('business_login')

    with db_transaction.atomic():

        redemption_details = get_object_or_404(
            redemption.objects.select_for_update(),
            id=redemption_id,
            reward__business=business_details
        )

        new_status = request.POST.get('status')

        if new_status == 'approved':

            if redemption_details.status != 'pending':
                messages.error(request, 'This request has already been processed.')
                return redirect('redemption_requests')

            redemption_details.status = 'approved'
            redemption_details.save()

            messages.success(request, 'Redemption request approved.')

        elif new_status == 'fulfilled':

            if redemption_details.status != 'approved':
                messages.error(request, 'Only approved requests can be fulfilled.')
                return redirect('redemption_requests')

            redemption_details.status = 'fulfilled'
            redemption_details.save()

            messages.success(request, 'Reward successfully fulfilled.')

        elif new_status == 'rejected':

            if redemption_details.status not in ['pending', 'approved']:
                messages.error(request, 'This request cannot be rejected.')
                return redirect('redemption_requests')

            customer_details = customer.objects.select_for_update().get(
                id=redemption_details.customer_id
            )

            customer_details.loyalty_points += redemption_details.points_deducted
            customer_details.save()

            redemption_details.status = 'rejected'
            redemption_details.save()

            messages.success(request, 'Request rejected. Customer points refunded.')
        else:
            messages.error(request, 'Invalid status.')
    return redirect('redemption_requests')

def business_fulfillment_history(request):
    try:
        business_details = request.user.business
    except business.DoesNotExist:
        return redirect('business_login')
    fulfilled_redemptions=redemption.objects.filter(reward__business=business_details, status='fulfilled').select_related('customer__user','reward').order_by('-created_at')
    return render(request, 'business_fulfillment_history.html', {'business': business_details,'fulfilled_redemptions': fulfilled_redemptions,})

