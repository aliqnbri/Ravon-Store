from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from core.models import BaseModel
from account.managers import CustomUserManager
from django.contrib import admin
from django.utils import timezone
# Create your models here.

class CustomUser(AbstractBaseUser, PermissionsMixin):
    class Role(models.TextChoices):
        ADMIN = 'admin', _('Admin')
        STAFF= "staff",_("Staff")
        CUSTOMER = 'customer', _('Customer')

    class StaffRoles(models.TextChoices):
        PRODUCT_MANAGER = "PM" , _("ProductManager")    
        SUPERVISOR = "SV" , _("Supervisor")
        OPERATOR = "OP", _("Operator")    

    username = models.CharField(max_length = 20, unique = True, null=True, blank=True)
    email = models.EmailField(max_length=255, unique=True)
    phone_number = models.CharField(max_length=13,null=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default = True)
    date_joined = models.DateField(default=timezone.now)
    role = models.CharField(max_length=8, choices=Role.choices, default=Role.CUSTOMER)
    staff_role = models.CharField(choices = StaffRoles, max_length = 2, null=True, blank=True, default=None)



    USERNAME_FIELD = ('email')
    REQUIRED_FIELDS = ('phone_number',)


    objects = CustomUserManager()


    def __str__(self) -> str:
        return f"user : {self.email} with {self.role} Role"
    
    



