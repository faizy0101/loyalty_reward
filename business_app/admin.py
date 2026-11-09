from django.contrib import admin
from .models import business, customer, transaction
# Register your models here.
@admin.register(business)
class BusinessAdmin(admin.ModelAdmin):
    list_display = ('business_name','owner_name','business_email','category','approval_status','created_at',)
    list_filter = ('business_name','approval_status','category',)
    search_fields = ('business_name','owner_name','business_email',)
    list_editable = ('approval_status',)

@admin.register(customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display=('user','business','loyalty_points','created_at',)
    list_filter=('business',)
    search_fields=('user__username','user__first_name','user__last_name','user__email','user__phone',)

@admin.register(transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display=('business','customer','purchase_amount', 'points_earned','created_at')
    list_filter=('business','created_at')
    search_fields=('customer__user__first_name','customer__user__last_name','customer__user__email')

