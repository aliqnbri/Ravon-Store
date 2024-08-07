from typing import Optional, Union
from django.contrib.auth import get_user_model
from django.core.exceptions import ImproperlyConfigured
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import AbstractBaseUser




class CustomBackendAuthenticate(ModelBackend):

    
    """ This class serves as a custom authentication backend for authenticating users in a Django application."""


    def __init__(self):
        self.User = get_user_model()
        if not issubclass(self.User, AbstractBaseUser):
            raise ImproperlyConfigured(_("You must define a User model"))

    def authenticate(self, request, username: Optional[str] = None, email: Optional[str] = None, password: Optional[str] = None, **kwargs) -> Optional[AbstractBaseUser]:

        if password is None:
            return None

        user = self._get_user_by_identifier(username, email)
        if user and user.check_password(password):
            return user
        return None
    
    def _get_user_by_identifier(self, username: Optional[str], email: Optional[str]) -> Optional[AbstractBaseUser]:
        if username:
            return self._get_user_by_username(username)
        if email:
            return self._get_user_by_email(email)
        return None
    
    def _get_user_by_username(self, username: str):
        try:
            return self.User.objects.get(username=username)
        except self.User.DoesNotExist:
            return None

    def _get_user_by_email(self, email: str):
        try:
            return self.User.objects.get(email=email)
        except self.User.DoesNotExist:
            return None

    def get_user(self, user_id: int) -> object:

        '''Attempt to retrieve the user object based on the provided user ID'''
        try:
            return self.User.objects.get(pk=user_id)
        except self.User.DoesNotExist:
            """If the user does not exist, return None"""
            return None
