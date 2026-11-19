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
    path('transaction_history/',views.transaction_history, name='transaction_history'),
    path('add_reward/',views.add_reward, name='add_reward'),
    path('reward_list/',views.reward_list, name='reward_list'),
    path('edit_reward/<int:reward_id>',views.edit_reward, name='edit_reward'),
    path('toggle_reward_status/<int:reward_id>', views.toggle_reward_status, name='toggle_reward_status'),
    path('redemption_requests/',views.redemption_requests, name='redemption_requests'),
    path('update_redemption_status/<int:redemption_id>',views.update_redemption_status, name='update_redemption_status'),
    path('fulfillment_history/', views.business_fulfillment_history, name='business_fulfillment_history'),
    


]