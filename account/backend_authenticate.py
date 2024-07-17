from django.contrib.auth.backends import BaseBackend
from django.contrib.auth import get_user_model


"""
CustomBackend

This class serves as a custom authentication backend for authenticating users in a Django application.

Attributes:
    None

Methods:
    authenticate(request, username=None, password=None, **kwargs): 
        This method attempts to authenticate a user based on the provided username and password.
        
        Parameters:
            request (HttpRequest): The HTTP request object containing the incoming request.
    
            password (str): The password of the user attempting to authenticate.
            **kwargs: Additional keyword arguments passed to the method.
            
        Returns:
            User or None: 
                - The authenticated user object if authentication is successful.
                - None if authentication fails or if the user does not exist.

    get_user(user_id): 
        This method retrieves a user object based on the user ID.
        
        Parameters:
            user_id (int): The ID of the user to retrieve.
            
        Returns:
            User or None: 
                - The user object corresponding to the provided user ID.
                - None if the user does not exist.
"""

class CustomBackend(BaseBackend):
    def authenticate(self, request, email=None , password=None, **kwargs):
        
        # Retrieve the User model
        User = get_user_model()
        
        # Attempt to retrieve the user object based on the provided username
        try:
            user = User.objects.get(email =email)
        except User.DoesNotExist:
            # If the user does not exist, return None
            return None
        
        # Check if the provided password matches the user's password
        if user.check_password(password):
            # If the passwords match, return the authenticated user object
            return user
        
        # If the passwords do not match, return None
        return None

    def get_user(self, user_id):
        
        # Retrieve the User model
        User = get_user_model()
        
        # Attempt to retrieve the user object based on the provided user ID
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            # If the user does not exist, return None
            return None