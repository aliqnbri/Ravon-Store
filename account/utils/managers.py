from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
import re



class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """

    def _create_user(self, email, password,username=None ,phone_number=None ,**extra_fields):
        """
        Create and save a user with the given email and password.
        """
        if not email:
            raise ValueError(_("The Email must be set"))

        if not password:
            raise ValueError (_("The Password must be set"))    

        if phone_number:
            if not re.match(r'^(\+98|0)?9\d{9}$', phone_number):
                raise ValidationError(_("Invalid phone number format for Iran. It should start with '+98' followed by 10 digits.")
                    )    

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
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('role', 'Operator')


        if extra_fields.get('is_staff') is not True:
            raise ValueError(_("Superuser must have is_staff=True."))
       
        if extra_fields.get('is_superuser') is True:
            raise ValueError(_("Superuser must have is_superuser=False."))
       
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('role', 'Role.ADMIN')


        if extra_fields.get('is_staff') is not True:
            raise ValueError(_("Superuser must have is_staff=True."))
       
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))
       
        return self._create_user(email, password, **extra_fields)


    def update_user(self, user_instance, **update_fields):
        for field, value in update_fields.items():
            setattr(user_instance, field, value)
        user_instance.save()
        return user_instance

    def delete_user(self, user_instance):
        user_instance.is_deleted = True
        user_instance.delete()
        user_instance.save()
            

