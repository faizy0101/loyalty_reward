from django.urls import path

from accounts_app import views

urlpatterns = [
    path("customer_register", views.customer_register, name="customer_register"),
    path("customer_login", views.customer_login, name="customer_login"),
    path("customer_dashboard", views.customer_dashboard, name="customer_dashboard"),
    path("customer_logout",views.customer_logout, name="customer_logout"),

]
