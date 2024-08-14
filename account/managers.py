from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
import re
from typing import Any

class CustomUserManager(BaseUserManager):

    """
    This class extends the functionality of BaseUserManager provided by Django's authentication framework.
    It provides methods for creating different types of users with custom fields and roles.'''
"""


    def _create_user(self,email: str, phone_number: str, password: str, **extra_fields) -> object:
        """
        Create and save a user with the given email and password.
        """
        if not email:
            raise ValueError(_("The Email must be set"))

        if not password:
            raise ValueError(_("The Password must be set"))

        if not phone_number:
            raise ValueError(_("The Password must be set"))

        if phone_number:
            if not re.match(r'^(\+98|0)?9\d{9}$', phone_number):
                raise ValidationError(_("Invalid phone_number number format for Iran. It should start with '+98' followed by 10 digits.")
                    )

        email = self.normalize_email(email)
        user = self.model(
            email=email, phone_number=phone_number, **extra_fields)
        user.set_password(password)  # change user passwoed
        user.save()
        return user

    def create_staffuser(self, email:str, password:str, **extra_fields:Any):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault('role' , self.model.Role.STAFF)
        extra_fields.setdefault('staff_role' , self.model.StaffRoles.OPERATOR)

        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, phone_number, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault('role', self.model.Role.ADMIN)
        extra_fields.setdefault('staff_role', self.model.StaffRoles.SUPERVISOR)


        return self._create_user(None, email, phone_number,  password, **extra_fields)

    def update_user(self, user_instance, **update_fields):
        for field, value in update_fields.items():
            setattr(user_instance, field, value)
        user_instance.save()
        return user_instance

    def delete_user(self, user_instance):
        user_instance.is_deleted = True
        user_instance.delete()
        user_instance.save()
