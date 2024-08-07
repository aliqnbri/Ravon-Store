from typing import Optional, Union
from django.contrib.auth import get_user_model
from django.core.exceptions import ImproperlyConfigured
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import AbstractBaseUser
from django.db.models import Q


class CustomBackendAuthenticate(ModelBackend):

    """ This class serves as a custom authentication backend for authenticating users in a Django application."""

    def __init__(self):
        self.User = get_user_model()
        if not issubclass(self.User, AbstractBaseUser):
            raise ImproperlyConfigured(_("You must define a User model"))

    def authenticate(self, request, username: Optional[str] = None, email: Optional[str] = None, password: Optional[str] = None, **kwargs) -> Optional[AbstractBaseUser]:
        user = None
        try:
            user = self.User.objects.filter(Q(email=username) | Q(username=username)).first()
        except self.User.DoesNotExist:
            pass

        if user and user.check_password(password):
            if not user.is_active:
                return None
            return user
        return None


    def get_user(self, user_id: int) -> object:
        '''Attempt to retrieve the user object based on the provided user ID'''
        if self.User.objects.filter(pk=user_id).exists():
            return self.User.objects.get(pk=user_id)
        return None