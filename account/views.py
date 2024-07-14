
from rest_framework import permissions , status
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from account import serializers
from account.utils.emails import send_otp 
from account.utils import authentications

from rest_framework.views import APIView
from django.conf import settings
# Create your views here.


class RegisterUserView(GenericAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = serializers.RegisterSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save(commit=False)
            email = user.email
            try:

                # send verification mail to the registered user
                send_otp(email=email)
                user.save()
                return Response({"message": "register successful ! Verify code sent to Email"}, status=status.HTTP_201_CREATED)
            
            except Exception as error:
                return Response({'Error': 'Error sending verification email code', 'Message': error},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

from account.models import CustomUser
from rest_framework.exceptions import AuthenticationFailed
import jwt
import datetime

class LoginView(APIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = serializers.LoginSerializer

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
                token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')

                response = Response({'Message': 'User loged in successfuly',
                                 'jwt':token}, status=200)
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

        return Response ({'message': token})
    






from rest_framework.response import Response
from rest_framework.views import APIView
from cutomserilizer import TokenAPISerializer

class TokenAPIView(APIView):
    def post(self, request):
        serializer = TokenAPISerializer(data=request.data)
        if serializer.is_valid():
            return Response(serializer.validated_data)
        return Response(serializer.errors, status=400)