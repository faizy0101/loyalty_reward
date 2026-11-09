

from django import forms
from django.forms import fields, widgets

from business_app.models import business, transaction


class BusinessRegistrationForm(forms.ModelForm):
    username=forms.CharField(max_length=50,widget=forms.TextInput(attrs={'class':'form-control','placeholder':'give a username'}))
    password1=forms.CharField(label='password',widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'password'}))
    password2=forms.CharField(label='confirm password',widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'confirm password'}))
    class Meta:
        model=business
        fields=['business_name','owner_name','business_email','phone','category','address',]
        widgets={'business_name':forms.TextInput(attrs={'class':'form-control','placeholder':'business name'}),
                 'owner_name':forms.TextInput(attrs={'class':'form-control','placeholder':'owner name'}),
                 'business_email':forms.EmailInput(attrs={'class':'form-control','placeholder':'email'}),
                 'phone':forms.TextInput(attrs={'class':'form-control','placeholder':'phone number'}),
                 'category':forms.Select(attrs={'class':'form-control'}),
                 'address':forms.TextInput(attrs={'class':'form-control'})}
def clean(self):
    cleaned_data=super().clean()
    password1=cleaned_data.get('password1')
    password2=cleaned_data.get('password2')
    if password1 and password2 and password1 != password2:
        self.add_error('password1',"Please enter the same password")
    return cleaned_data

class BusinessLoginForm(forms.Form):
    username=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Enter username'}))
    password=forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Enter password'}))
    

class BusinessProfileForm(forms.ModelForm):
    class Meta:
        model=business
        fields=['business_name','owner_name','business_email','phone','category','address']
        widgets={'business_name':forms.TextInput(attrs={'class':'form-control','placeholder':'business name'}),
                 'owner_name':forms.TextInput(attrs={'class':'form-control','placeholder':'owner name'}),
                 'business_email':forms.EmailInput(attrs={'class':'form-control','placeholder':'email'}),
                 'phone':forms.TextInput(attrs={'class':'form-control','placeholder':'phone number'}),
                 'category':forms.Select(attrs={'class':'form-control'}),}

class LoyaltySettingsForm(forms.ModelForm):
    class Meta:
        model=business
        fields=['loyalty_program_active','purchase_amount_for_points','points_earned','welcome_bonus_points','minimum_purchase_amount']
        widgets={'loyalty_program_active':forms.CheckboxInput(attrs={'class':'form-check-input'}),
        'purchase_amount_for_points':forms.NumberInput(attrs={'class':'form-control','step':'0.01'}),
        'points_earned':forms.NumberInput(attrs={'class':'form-control','step':'0'}),
        'welcome_bonus_points': forms.NumberInput(attrs={'class': 'form-control','min':'0'}),
        'minimum_purchase_amount': forms.NumberInput(attrs={'class': 'form-control','step': '0.01','min': '0'}),}



class CustomerSearchForm(forms.Form):
    customer_email=forms.EmailField(label='Customer Email',widget=forms.EmailInput(attrs={'class':'form-control','placeholder':'Enter Customer Email'}))
    
class TransactionForm(forms.ModelForm):
    class Meta:
        model=transaction
        fields=['customer','purchase_amount']
        widgets={'customer':forms.Select(attrs={'class':'form-select'}),
                'purchase_amount':forms.NumberInput(attrs={'class':'form-control','placeholder':'Enter purchased amount...','min':'0.01','step':'0.01'}),}