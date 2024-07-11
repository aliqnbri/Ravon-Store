from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from core.models import BaseModel

# Create your models here.

class CustomUser(AbstractBaseUser, PermissionsMixin, BaseModel):
    class Role(models.TextChoices):
        ADMIN = 'admin', _('Admin')
        OPERATOR = 'operator', _('Operator')
        CUSTOMER = 'customer', _('Customer')
        GUEST = 'guest', _('Guest')

    email = models.EmailField(max_length=255, unique=True)
    phone_number = models.CharField(null=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    role = models.CharField(max_length=8, choices=Role, default=Role.CUSTOMER)

    USERNAME_FIELD = 'email'


    objects = CustomUserManager()


    def __str__(self) -> str:
        return f"{self.email} with {self.role} Role"
    


    

  


    def __str__(self):
        return self.email
    