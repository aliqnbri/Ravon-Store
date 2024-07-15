
from account.models import CustomUser
import datetime
import jwt
from rest_framework.exceptions import AuthenticationFailed
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from account import serializers
from account.utils.emails import send_otp, check_otp
from account.utils import authentications
from rest_framework.views import APIView
from django.conf import settings
from django.shortcuts import redirect
from django.urls import reverse
# Create your views here.


class RegisterUserView(APIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = serializers.RegisterSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user_data = serializer.validated_data
            user = CustomUser(**user_data)
            email = user.email
            try:

                # send verification mail to the registered user
                send_otp(email=email)
                payload = {
                    'id': user.id,
                    'email':user.email,
                    'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
                    'iat': datetime.datetime.utcnow()
                }
                token = jwt.encode(
                    payload, settings.SECRET_KEY, algorithm='HS256')
                response = Response()
                response.set_cookie(key='jwt', value=token, httponly=True)
                user.save()
               
                

            except Exception as error:
                return Response({'Error': 'Error sending verification email code', 'Message': str(error)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            return response
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

    def get_success_url(self,*args,):
        return redirect(reverse('account:verify_otp'))

class VerifyOtp(GenericAPIView):
    serializer_class = serializers.VerifyOtpSerialiser
    permission_classes = [permissions.AllowAny,]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        jwt_cookie  = request.COOKIES.get('jwt')
        print(jwt_cookie)
        payload = jwt.decode(jwt_cookie, settings.SECRET_KEY, algorithms=['HS256'])
        email = payload['email']
  
        otp = serializer.validated_data['otp']

        if check_otp(email=email, otp=otp):
            return Response({"message": "your Account verified"}, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        return Response({"message": "register successful ! Verify code sent to Email"}, status=status.HTTP_201_CREATED)


class LoginView(APIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = serializers.LoginSerializer
    authentication_classes = (authentications.CustomJWTAuthentication,)

    def post(self, request):
        email = request.data['email']
        password = request.data['password']

        user = CustomUser.objects.filter(email=email).first()
        if user:
            if user.check_password(password):

                payload = {
                    'id': user.id,
                    'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
                    'iat': datetime.datetime.utcnow()
                }
                token = jwt.encode(
                    payload, settings.SECRET_KEY, algorithm='HS256')

                response = Response({'Message': 'User loged in successfuly',
                                     'jwt': token}, status=200)
                response.set_cookie(key='jwt', value=token, httponly=True)

                return response
            raise AuthenticationFailed('incorect password')
        else:
            raise AuthenticationFailed('user not find')

    def get(self, request):
        # Check if the user is already logged in
        if request.user.is_authenticated:
            return Response({
                'message': 'You are already logged in'
            })
        return Response({
            'message': 'Please login to continue'
        })


class CheckCookie(APIView):
    permission_classes = (permissions.AllowAny,)

    def get(self, request):
        token = request.COOKIES.get('jwt')

        return Response({'message': token})
