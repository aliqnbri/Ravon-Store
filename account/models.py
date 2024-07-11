from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from core.models import BaseModel

# Create your models here.

class CustomUser(AbstractBaseUser, PermissionsMixin, BaseModel):
    class Role(models.TextChoices):
        ADMIN = 'admin', 'Admin'
        OPERATOR = 'operator', 'Operator'
        CUSTOMER = 'customer', 'Customer'
        GUEST = 'guest', 'Guest'

    email = models.EmailField(max_length=255, unique=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    role = models.CharField(max_length=8, choices=Role, default=Role.CUSTOMER)

    USERNAME_FIELD = 'email'


    objects = CustomUserManager()


    def __str__(self) -> str:
        return f"{self.email} with {self.role} Role"
    


    

  


    def __str__(self):
        return self.email
    