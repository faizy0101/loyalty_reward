from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms

from accounts_app.models import User


class CustomerRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email','phone')

class UserLoginForm(AuthenticationForm):
    username = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(attrs={'class':'form-control', 'placeholder':'Email',})
    )
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'Password',}))
