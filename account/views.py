
from django.contrib.auth import authenticate, logout
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.exceptions import AuthenticationFailed
from rest_framework import permissions, status, generics
from rest_framework.generics import GenericAPIView
from account import serializers, utils, authentications
from account.authentications import CustomJWTAuthentication
from rest_framework.response import Response
from django.views.generic import TemplateView
from rest_framework.views import APIView
from account.models import CustomUser
from rest_framework.reverse import reverse
from django.shortcuts import redirect
from django.conf import settings
from typing import Any, Dict, Optional

# Create your views here.

class RegisterUserView(generics.CreateAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = serializers.RegisterSerializer
    authentication_classes = (CustomJWTAuthentication, )

    def post(self, request: Any) -> Response:
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.save()
        access_token, refresh_token = utils.generate_tokens(user)

        try:
            utils.send_otp(user.email)

        except Exception as error:
            return Response({'Error': 'Error sending verification email code', 'Message': str(error)},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        response = redirect(reverse('account:verify-otp'))
        response.set_cookie(key='access_token', value=str(access_token))
        response.set_cookie(key='refresh_token', value=str(refresh_token))

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



        email = payload['email']
        otp = serializer.validated_data['otp']

        if utils.check_otp(email=email, otp=otp):
            user = CustomUser.objects.get(email=email)
            user.is_verified = True
            user.save()

            return Response({"message": "your Account verified"}, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request: Any) -> Response:
        access_token = request.COOKIES.get('access_token')
        refresh_token = request.COOKIES.get('refresh_token')
        return Response({"message": "register successful ! Verify code sent to Email",
                         'access_toke': str(access_token),
                         'refresh_token': str(refresh_token)}, status=status.HTTP_201_CREATED)


class LogoutView(APIView):
    authentication_classes = [CustomJWTAuthentication,]
    permission_classes = [permissions.AllowAny,]

    def post(self, request: Any) -> Response:
        if (a:= request.user.is_authenticated):
            print(a)
            logout(request)
            response = Response({'message': 'Logout successful'}, status=status.HTTP_200_OK)
            response.delete_cookie('access_token', '/')
            response.delete_cookie('refresh_token', '/')
     
            return response
        return Response({'message': 'User is not authenticated'}, status=status.HTTP_401_UNAUTHORIZED)

class MyTokenObtainPairView(TokenObtainPairView):  # I use this for login user.
    serializer_class = serializers.MyTokenObtainPairSerializer

    def post(self, request, *args, **kwargs)-> Response:
        response = super().post(request, *args, **kwargs)

        email: Optional[str] = request.data.get('email')
        password: Optional[str] = request.data.get('password')
        user = authenticate(email=email, password=password)

        if user:
            if not user.is_verified:
                return Response({"message": "Email verification required"}, status=status.HTTP_403_FORBIDDEN)

            response.set_cookie(
                key='access_token',
                value=response.data['access'],
                httponly=settings.SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY'],
                max_age=settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'],
                secure=settings.SIMPLE_JWT['AUTH_COOKIE_SECURE']
            )
            response.set_cookie(
                key='refresh_token',
                value=response.data['refresh'],
                httponly=settings.SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY'],
                max_age=settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME'],
                secure=settings.SIMPLE_JWT['AUTH_COOKIE_SECURE']
            )

            response.data = {"message": "login successfull"}
            response.status = status.HTTP_200_OK
            return response

        raise AuthenticationFailed('Invalid email or password')


class CustomTokenRefreshView(TokenRefreshView):
    authentication_classes = [CustomJWTAuthentication,]

    def post(self, request, *args, **kwargs)-> Response:
        response = super().post(request, *args, **kwargs)
        response.set_cookie(
            key='access_token',
            value=response.data['access'],
            httponly=settings.SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY'],
            max_age=settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'],
            secure=settings.SIMPLE_JWT['AUTH_COOKIE_SECURE']
        )
        response.data = {"message": "New access token set in cookies"}
        return response


# # # Create your views here.
# class SignUpView(TemplateView):
#     template_name = 'signup.html'
