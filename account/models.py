from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from django.db import models

# Create your models here.
class CustomUser( AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = (
        ('ad', 'Admin'),
        ('op', 'Operator'),
        ('cu', 'Customer'),
    )    
    username = models.CharField(max_length=16, unique=True, null=True,)
    phone_number = models.CharField(max_length=11, null=True)
    email = models.EmailField(unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=False)
    role = models.CharField(max_length=2, choices=ROLE_CHOICES, default='cu')

    USERNAME_FIELD = "email"

    # email and passwrod required by default
    REQUIRED_FIELDS = ['phone_number']



    def __str__(self):
        return f"{self.email}"

