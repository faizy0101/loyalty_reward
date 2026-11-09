from django.db import models

from accounts_app.models import User



class business(models.Model):
    APPROVAL_STATUS = [('pending','Pending Approval'),
                       ('approved','Approved'),
                       ('rejected','Rejected'),]
    BUSINESS_CATEGORIES=[('retail','Retail'),
                         ('restaurant','Restaurant'),
                         ('grocery', 'Grocery'),
                         ('fashion', 'Fashion'),
                         ('electronics', 'Electronics'),
                         ('other', 'Other'),]
    owner=models.OneToOneField(User, on_delete=models.CASCADE, related_name='business')
    business_name=models.CharField(max_length=100,null=True,blank=True)
    business_email=models.EmailField(max_length=100,null=True,blank=True)
    owner_name=models.CharField(max_length=100,null=True,blank=True)
    phone=models.CharField(max_length=100,null=True,blank=True)
    category=models.CharField(max_length=30,choices=BUSINESS_CATEGORIES)
    address=models.CharField(max_length=100,null=True,blank=True)
    approval_status=models.CharField(max_length=30,choices=APPROVAL_STATUS)
    created_at=models.DateTimeField(auto_now_add=True)
    #points setting
    loyalty_program_active=models.BooleanField(default=True)
    purchase_amount_for_points=models.DecimalField(max_digits=10,decimal_places=2,default=0.00)
    points_earned=models.PositiveIntegerField(default=0)
    welcome_bonus_points=models.PositiveIntegerField(default=0)
    minimum_purchase_amount=models.DecimalField(max_digits=10,decimal_places=2,default=0.00)
    def __str__(self):
        return self.business_name

class customer(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE, related_name='business_memberships')
    business=models.ForeignKey(business, on_delete=models.CASCADE, related_name='customers')
    loyalty_points=models.PositiveIntegerField(default=0)
    created_at=models.DateTimeField(auto_now_add=True)
    class Meta:
        unique_together=('user','business')
    def __str__(self):
        return f"{self.user.username} - {self.business.business_name}"

class transaction(models.Model):
    business=models.ForeignKey(business, on_delete=models.CASCADE, related_name='transactions')
    customer=models.ForeignKey(customer, on_delete=models.CASCADE, related_name='transactions')
    purchase_amount=models.DecimalField(max_digits=10,decimal_places=2,default=0.00)
    points_earned=models.PositiveIntegerField(default=0)
    created_at=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.customer.user.username} - {self.purchase_amount}"



