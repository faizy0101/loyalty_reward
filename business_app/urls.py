from business_app import views
from django.urls import path

urlpatterns=[
    path('business_register/',views.business_register,name='business_register'),
    path('business_login/',views.business_login,name='business_login'),
    path('business_dashboard/',views.business_dashboard,name='business_dashboard'),
    path('business_profile/',views.business_profile,name='business_profile'),
    path('loyalty_settings/',views.loyalty_settings, name='loyalty_settings'),
    path('add_customer/',views.add_customer, name='add_customer'),
    path('customer_list/', views.customer_list, name='customer_list'),
    path('add_transactions/',views.add_transactions, name='add_transactions'),
]