from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
import re

""""
CustomUserManager

This class extends the functionality of BaseUserManager provided by Django's authentication framework. It provides methods for creating different types of users with custom fields and roles.

Attributes:
    None

Methods:
    _create_user(email, phone_number, password=None, **extra_fields): 
        This method creates a regular user with the provided email, phone_number, and password (optional). 
        
        Parameters:
    
            email (str): The email address of the user to be created.
            phone_number (str): The phone_number number of the user to be created.
            password (str): The password for the user. If not provided, a default password will be set.
            **extra_fields: Additional fields to be set for the user.
        
        Returns:
            User: The created user object.

    create_superuser(email, phone_number, password=None, **extra_fields): 
        This method creates a superuser with the provided , email, phone_number, and password (optional). 
        
        Parameters:
            email (str): The email address of the superuser to be created.
            phone_number (str): The phone_number number of the superuser to be created.
            password (str): The password for the superuser. If not provided, a default password will be set.
            **extra_fields: Additional fields to be set for the superuser.
        
        Returns:
            User: The created superuser object.

    create_customer(, email, phone_number, first_name=None, last_name=None, password=None, **extra_fields): 
        This method creates a customer user with the provided , email, phone_number, first name, last name, and password (optional).
        
        Parameters:

            email (str): The email address of the customer user to be created.
            phone_number (str): The phone_number number of the customer user to be created.
            password (str): The password for the customer user. If not provided, a default password will be set.
            **extra_fields: Additional fields to be set for the customer user.
        
        Returns:
            User: The created customer user object.
"""




class CustomUserManager(BaseUserManager):

    def _create_user (self,username=None, email=None, phone_number=None, password=None  ,**extra_fields):
        """
        Create and save a user with the given email and password.
        """
        if not email:
            raise ValueError(_("The Email must be set"))

        if not password:
            raise ValueError (_("The Password must be set"))  
          
        if not phone_number:
            raise ValueError (_("The Password must be set"))    

        # if phone_number:
        #     if not re.match(r'^(\+98|0)?9\d{9}$', phone_number):
        #         raise ValidationError(_("Invalid phone_number number format for Iran. It should start with '+98' followed by 10 digits.")
        #             )    

        email = self.normalize_email(email)
        user = self.model(email=email,phone_number=phone_number, **extra_fields)
        user.set_password(password) # change user passwoed
        user.save()
        return user




    def create_staffuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', False)
        extra_fields.setdefault('is_verified', True)
        extra_fields.setdefault('role', self.model.Role.STAFF)


        if extra_fields.get('is_staff') is not True:
            raise ValueError(_("Superuser must have is_staff=True."))
       
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))
       
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, phone_number,password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', self.model.Role.ADMIN)


        if not extra_fields.get('is_staff'):
            raise ValueError(_("Superuser must have is_staff=True."))

        if not extra_fields.get('is_superuser'):
            raise ValueError(_("Superuser must have is_superuser=True."))
       
        return self._create_user(None, email , phone_number,  password, **extra_fields)


    def update_user(self, user_instance, **update_fields):
        for field, value in update_fields.items():
            setattr(user_instance, field, value)
        user_instance.save()
        return user_instance

    def delete_user(self, user_instance):
        user_instance.is_deleted = True
        user_instance.delete()
        user_instance.save()
            

