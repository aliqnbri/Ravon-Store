from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.authentication import CSRFCheck
from rest_framework import exceptions
from django.conf import settings
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import authenticate,logout
from rest_framework.response import Response 
from rest_framework import status
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
     
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['email'] = user.email
        token['phone_number'] = user.phone_number
        token['password'] = user.password
        return token



          

            



def get_tokens_for_user(user) -> dict:
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token), }


def enforce_csrf(request):
    check = CSRFCheck(request)
    check.process_request(request)
    reason = check.process_view(request, None, (), {})
    if reason:
        raise exceptions.PermissionDenied('CSRF Failed: %s' % reason)



class CustomJWTAuthentication(JWTAuthentication):
    """"
    This class extends the functionality of JWTAuthentication provided by the Django REST Framework Simple JWT library.
    It provides custom authentication for JWT (JSON Web Tokens) in Django REST Framework.

    """

    def authenticate(self, request) -> tuple:
        # Retrieve the JWT token from the request header
        header = self.get_header(request)
        if header is None:
            # If the token is not found in the header, try to get it from the AUTH_COOKIE (configured in settings)
            raw_token = request.COOKIES.get(
                settings.SIMPLE_JWT['AUTH_COOKIE'],) or None
        else:
            # If the token is found in the header, extract it
            raw_token = self.get_raw_token(header)
     #  If the token is still not found, return None
        if raw_token is None:
            return None

         # Validate the token
        validated_token = self.get_validated_token(raw_token)

        # for more secure force CSRF token
        enforce_csrf(request)

        # Get the user associated with the validated token
        return self.get_user(validated_token), validated_token
