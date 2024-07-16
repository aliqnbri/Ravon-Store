from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from core.models import BaseModel
from account.utils.managers import CustomUserManager
# Create your models here.

class CustomUser(AbstractBaseUser, PermissionsMixin, BaseModel):
    class Role(models.TextChoices):
        ADMIN = 'admin', _('Admin')
        OPERATOR = 'operator', _('Operator')
        CUSTOMER = 'customer', _('Customer')
        GUEST = 'guest', _('Guest')

    username = models.CharField(max_length=16,null=True)
    email = models.EmailField(max_length=255, unique=True)
    phone_number = models.CharField(max_length=13,null=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    role = models.CharField(max_length=8, choices=Role.choices, default=Role.CUSTOMER)

    USERNAME_FIELD = 'email'


    objects = CustomUserManager()


    def __str__(self) -> str:
        return f"user : {self.email} with {self.role} Role"
    


    

class Address(BaseModel):
    """
    Address Model for user's address 
    """
    street = models.CharField(max_length=100)
    city = models.CharField(max_length=50)
    postal_code = models.CharField(max_length=20)
    detail = models.TextField()

    def get_address(self):
        return f"Address : {self.city} ,{self.street}, {self.postal_code}"



class CustomerProfile(models.Model):
    class Gender(models.TextChoices):
        MALE = 'male', _('Male')
        FEMALE = 'F', _('Female')

    user = models.OneToOneField(CustomUser ,on_delete=models.CASCADE)
    first_name = models.CharField(max_length=30, verbose_name='First Name')
    last_name = models.CharField(max_length=30,verbose_name='Last Name')
    gender = models.CharField(max_length=6, choices=Gender.choices, null=True, blank=True)
    avatar = models.ImageField(upload_to='media/avatars/', null=True, blank=True)
    address = models.ForeignKey(Address, null=True, blank=True, on_delete=models.CASCADE )



    @property
    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'

    @property
    def get_username(self):
        return f'{self.username}'
    