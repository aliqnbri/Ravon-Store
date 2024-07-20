
from rest_framework.exceptions import AuthenticationFailed
from rest_framework import permissions, status,generics
from rest_framework.generics import GenericAPIView
from account import serializers ,utils ,authentications
from account.authentications import CustomJWTAuthentication
from rest_framework.response import Response
from django.views.generic import TemplateView 
from rest_framework.views import APIView
from account.models import CustomUser
from rest_framework.reverse import reverse
from django.middleware.csrf import get_token
from django.shortcuts import redirect
from django.conf import settings
import jwt

# Create your views here.




class RegisterUserView(generics.CreateAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = serializers.RegisterSerializer
    authentication_classes = (CustomJWTAuthentication, )
    # template_name = 'signup.html'    


    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if not serializer.is_valid(raise_exception=True):
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
        
        user = serializer.save()
        access, refresh = serializers.MyTokenObtainPairSerializer.get_access_refresh_token(user).values()
        print(access)
        print(refresh)

        # try:
        #     utils.send_otp(serializer.data['email'])
        # except Exception as error:
        #     return Response({'Error': 'Error sending verification email code', 'Message': str(error)},
        #                     status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        response = Response({'message': "Regiser was Successful"})
        # response = redirect(reverse('account:verify-otp'))
        response.set_cookie(key='access_token', value=access)
        response.set_cookie(key='refresh_token', value=refresh)

        return response



class VerifyOtp(APIView):
    serializer_class = serializers.VerifyOtpSerialiser
    permission_classes = [permissions.AllowAny,]
    authentication_classes = (CustomJWTAuthentication,)


    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        jwt_cookie = request.COOKIES.get('access_token')
        if not serializer.is_valid(raise_exception=True):
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
        payload = jwt.decode(
            jwt_cookie, settings.SECRET_KEY, algorithms=['HS256'])
        
        print (payload)
        email = payload['email']

        otp = serializer.validated_data['otp']

        if utils.check_otp(email=email, otp=otp):
            user = CustomUser.objects.get(email=email)
            user.is_verified =True

            return Response({"message": "your Account verified"}, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        access_token = request.COOKIES.get('access_token')
        refresh_token = request.COOKIES.get('refresh_token')
        return Response({"message": "register successful ! Verify code sent to Email",
                         'access_toke': str(access_token),
                         'refresh_token' : str(refresh_token)}, status=status.HTTP_200_CREATED)


class LogoutView(APIView):
    authentication_classes = [CustomJWTAuthentication,]

    def post(self, request):
        if request.user.is_authenticated:
            logout(request)
            response = Response()
            response.delete_cookie('access_token', '/')
            response.delete_cookie('refresh_token', '/')
            response.data = {'message': 'Logout successful'}
            response.status = status.HTTP_200_OK
            return response
        else:
            return Response({'message': 'User is not authenticated'}, status=status.HTTP_401_UNAUTHORIZED)



from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView
from django.contrib.auth import authenticate,logout

class MyTokenObtainPairView(TokenObtainPairView): # I use this for login user.
    serializer_class = serializers.MyTokenObtainPairSerializer


    def post(self,request, *args,**kwargs):
        response = super().post(request, *args, **kwargs)
        
        email = request.data.get('email')
        password = request.data.get('password')
        user = authenticate(email=email , password=password)


        if user is not None:
            if not user.is_verified:
                return Response({"message": "email verification required"},status.HTTP_403_FORBIDDEN)
            
        
            
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

    def post(self,request,*args,**kwargs):
        response = super().post(request, *args, **kwargs)
        response.set_cookie(
            key='access_token',
            value=response.data['access'],
            httponly=settings.SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY'],
            max_age=settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'],
            secure=settings.SIMPLE_JWT['AUTH_COOKIE_SECURE']
        )
        response.data = "new access set to cookies"
        return response            
    

# # Create your views here.
class SignUpView(TemplateView):
    template_name = 'signup.html'