
from django.contrib.auth import authenticate, logout
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.exceptions import AuthenticationFailed
from rest_framework import permissions, status, generics

from account import serializers, utils, authentications
from account.authentications import CustomJWTAuthentication
from rest_framework.response import Response
from django.views.generic import TemplateView
from rest_framework.views import APIView
from account.models import CustomUser
from rest_framework.reverse import reverse
from django.shortcuts import redirect
from django.conf import settings
from typing import Any, Dict, Optional, Union

# Create your views here.


class CustomLoginView(TemplateView):
    template_name='login.html'
    
class VerifyTemplateView(TemplateView):
    template_name = 'verifyotp.html'

class RegisterUserView(generics.CreateAPIView, TemplateView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = serializers.RegisterSerializer
    authentication_classes = (CustomJWTAuthentication, )
    template_name = 'signup.html'

    def get(self, request: Any, *args: Any, **kwargs: Any) -> Response:
        """
        Handle GET requests and render the signup template.
        """
        return self.render_to_response(self.get_context_data())

    def post(self, request: Any) -> Response:
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.save()
        access_token, refresh_token = utils.generate_tokens(user)

        if not self._send_verification_email(user.email):
            return Response(
                {'Error': 'Error sending verification email code'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        response = self._create_response_with_tokens(reverse('account:verify-otp'), access_token, refresh_token)
        return response
    
    def _send_verification_email(self, email: str) -> bool:
        try:
            utils.send_otp(email)
            return True
        except Exception as error:
            # Log the error for debugging purposes
            print(f"Error sending verification email: {error}")
            return False

    def _create_response_with_tokens(self, redirect_url: str, access_token: str, refresh_token: str) -> Response:
        response = redirect(redirect_url)
        response.set_cookie(key='access_token', value=access_token, httponly=True, secure=settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'])
        response.set_cookie(key='refresh_token', value=refresh_token, httponly=True, secure=settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'])
        return response


class VerifyOtp(APIView):
    serializer_class = serializers.VerifyOtpSerialiser
    permission_classes = [permissions.AllowAny,]
    authentication_classes = (CustomJWTAuthentication,)

    def post(self, request: Any) -> Response:
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        access_token: Optional[str] = request.COOKIES.get('access_token')
        if not access_token:
            return Response({'detail': 'Access token missing.'}, status=status.HTTP_400_BAD_REQUEST)
        
        payload = utils.decode_token(access_token)
        if not payload:
            return Response({'detail': 'Invalid or expired access token.'}, status=status.HTTP_400_BAD_REQUEST)
        
        if not self._verify_user(payload['email'], serializer.validated_data['otp']):
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response({"message": "Your account has been verified"}, status=status.HTTP_202_ACCEPTED)
        



    def get(self, request: Any) -> Response:
        access_token = request.COOKIES.get('access_token')
        refresh_token = request.COOKIES.get('refresh_token')
        return Response({"message": "register successful ! Verify code sent to Email",
                         'access_toke': str(access_token),
                         'refresh_token': str(refresh_token)}, status=status.HTTP_201_CREATED)

    def _verify_user(self, email: str, otp: str) -> bool:
        if utils.check_otp(email=email, otp=otp):
            user = CustomUser.objects.get(email=email)
            user.is_verified = True
            user.save()
            return True
        return False

class LogoutView(APIView):
    authentication_classes = [CustomJWTAuthentication,]
    permission_classes = [permissions.AllowAny,]

    def post(self, request: Any) -> Response:
        if request.user.is_authenticated:
                logout(request)
                response = self._create_logout_response()
                return response
        return Response({'message': 'User is not authenticated'}, status=status.HTTP_401_UNAUTHORIZED)

    def _create_logout_response(self) -> Response:
        response = Response({'message': 'Logout successful'}, status=status.HTTP_200_OK)
        response.delete_cookie('access_token', '/')
        response.delete_cookie('refresh_token', '/')
        return response

class MyTokenObtainPairView(TokenObtainPairView):  # I use this for login user.
    serializer_class = serializers.MyTokenObtainPairSerializer

    def post(self, request, *args, **kwargs)-> Response:
        response = super().post(request, *args, **kwargs)

        email: Optional[str] = request.data.get('email')
        password: Optional[str] = request.data.get('password')
        user = authenticate(email=email, password=password)
        if user is None:
            raise AuthenticationFailed('Invalid email or password')

        if not user.is_verified:
            if not self._send_verification_email(user):
                return Response(
                    {'Error': 'Error sending verification email code'},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
            return self._create_verification_response(user)

        self._set_login_cookies(response, response.data['access'], response.data['refresh'])
        response.data = {"message": "Login successful"}
        response.status_code = status.HTTP_200_OK
        return response

    def _send_verification_email(self, user: CustomUser) -> bool:
        try:
            utils.send_otp(user.email)
            return True
        except Exception as error:
            # Log the error for debugging purposes
            print(f"Error sending verification email: {error}")
            return False

    def _create_verification_response(self, user: CustomUser) -> Response:
        access_token, refresh_token = utils.generate_tokens(user)
        response = redirect(reverse('account:verify-otp'))
        response.set_cookie(key='access_token', value=access_token, httponly=True, secure=settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'])
        response.set_cookie(key='refresh_token', value=refresh_token, httponly=True, secure=settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'])
        return response

    def _set_login_cookies(self, response: Response, access_token: str, refresh_token: str) -> None:
        response.set_cookie(
            key='access_token',
            value=access_token,
            httponly=settings.SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY'],
            max_age=settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'],
            secure=settings.SIMPLE_JWT['AUTH_COOKIE_SECURE']
        )
        response.set_cookie(
            key='refresh_token',
            value=refresh_token,
            httponly=settings.SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY'],
            max_age=settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME'],
            secure=settings.SIMPLE_JWT['AUTH_COOKIE_SECURE']
        )



class CustomTokenRefreshView(TokenRefreshView):
    authentication_classes = [CustomJWTAuthentication,]

    def post(self, request: Any, *args: Any, **kwargs: Any) -> Response:
        response = super().post(request, *args, **kwargs)
        self._set_refresh_cookies(response, response.data['access'])
        response.data = {"message": "New access token set in cookies"}
        return response

    def _set_refresh_cookies(self, response: Response, access_token: str) -> None:
        response.set_cookie(
            key='access_token',
            value=access_token,
            httponly=settings.SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY'],
            max_age=settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'],
            secure=settings.SIMPLE_JWT['AUTH_COOKIE_SECURE']
        )


