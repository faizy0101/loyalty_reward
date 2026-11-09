from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class User(AbstractUser):
    email = models.EmailField(max_length=250,unique=True)
    phone=models.CharField(max_length=15)
    created_at=models.DateTimeField(auto_now_add=True)
    USERNAME_FIELD='email'
    REQUIRED_FIELDS=['username']
    def __str__(self):
        return self.username


    