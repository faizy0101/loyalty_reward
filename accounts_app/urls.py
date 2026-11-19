from django.urls import path

from accounts_app import views

urlpatterns = [
    path("customer_register", views.customer_register, name="customer_register"),
    path("customer_login", views.customer_login, name="customer_login"),
    path("customer_dashboard", views.customer_dashboard, name="customer_dashboard"),
    path("customer_logout",views.customer_logout, name="customer_logout"),
    path("customer_transaction_history", views.customer_transaction_history, name="customer_transaction_history"),
    path('customer_rewards', views.customer_rewards, name="customer_rewards"),
    path('redeem_reward/<int:reward_id>', views.redeem_reward, name='redeem_reward'),
    path('customer_redemption_history',views.customer_redemption_history, name='customer_redemption_history'),

]

