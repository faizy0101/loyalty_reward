from business_app.views import customer_list
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.db.models import Model
from django.shortcuts import render, redirect, get_object_or_404
from business_app.models import customer, transaction, reward, business, redemption
from django.db import transaction as db_transaction
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
    customer_memberships=request.user.business_memberships.select_related('business').all()
    total_points=sum(membership.loyalty_points for membership in customer_memberships)
    return render(request,'customer_dashboard.html', {'customer_memberships': customer_memberships, 'total_points': total_points,})

def customer_logout(request):
    if request.method == 'POST':
        logout(request)
        messages.success(request,'You are logged out!')
        return redirect("customer_login")
    return render(request,'customer_dashboard.html')

def customer_transaction_history(request):
    customer_memberships=request.user.business_memberships.all()
    customer_transactions=transaction.objects.filter(customer__in=customer_memberships).select_related('business','customer').order_by('-created_at')
    return render(request, 'customer_transaction_history.html', {'customer_transactions':customer_transactions})

def customer_rewards(request):
    customer_memberships=request.user.business_memberships.all()
    customer_rewards=reward.objects.filter(business__in=customer_memberships.values('business'), is_active=True).select_related('business').order_by('points_required')
    return render(request, 'customer_rewards.html',{'customer_rewards':customer_rewards})

def redeem_reward(request, reward_id):
    if request.method != 'POST':
        return redirect('customer_rewards')
    reward_details=get_object_or_404(reward, id=reward_id, is_active=True)
    customer_memberships=get_object_or_404(customer, user=request.user, business=reward_details.business)
    with db_transaction.atomic():
        customer_memberships=customer.objects.select_for_update().get(id=customer_memberships.id)
        if customer_memberships.loyalty_points<reward_details.points_required:
            messages.error(request, 'No enough points...')
            return redirect('customer_rewards')
        customer_memberships.loyalty_points-=reward_details.points_required
        customer_memberships.save()
        redemption.objects.create(customer=customer_memberships, reward=reward_details, points_deducted=reward_details.points_required)
    messages.success(request, 'Reward redeemed successfully!')
    return redirect('customer_rewards')

def customer_redemption_history(request):
    redemptions=redemption.objects.filter(customer__user=request.user).select_related('reward','reward__business').order_by('-created_at')
    return render(request, 'customer_redemption_history.html',{'redemptions':redemptions})