
from account.models import CustomUser
from rest_framework.exceptions import AuthenticationFailed
from rest_framework import permissions, status, mixins, generics, views
from rest_framework.response import Response
from account import serializers ,utils ,authentications
from rest_framework.views import APIView
from django.conf import settings
from django.views.generic import TemplateView 

# Create your views here.

from django.middleware.csrf import get_token
from rest_framework.generics import GenericAPIView

from rest_framework.reverse import reverse
from django.shortcuts import redirect





class RegisterUserView(generics.CreateAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = serializers.RegisterSerializer
    authentication_classes = (authentications.CustomJWTAuthentication, )

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if not serializer.is_valid(raise_exception=True):
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

        user = serializer.save()
        refresh, access = authentications.get_tokens_for_user(user).values()

        csrf_token = get_token(request)
        try:
            utils.send_otp(serializer.data['email'])
        except Exception as error:
            return Response({'Error': 'Error sending verification email code', 'Message': str(error)},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        response = redirect(reverse('account:verify-otp'))
        response.set_cookie(key='access_token', value=access,)
        response.set_cookie(key='csrftoken', value=csrf_token)
        return response






# class VerifyOtp(GenericAPIView):
#     serializer_class = serializers.VerifyOtpSerialiser
#     permission_classes = [permissions.AllowAny,]

#     def post(self, request):
#         serializer = self.serializer_class(data=request.data)
#         jwt_cookie = request.COOKIES.get('jwt')
#         print(jwt_cookie)
#         payload = jwt.decode(
#             jwt_cookie, settings.SECRET_KEY, algorithms=['HS256'])
#         email = payload['email']

#         otp = serializer.validated_data['otp']

#         if check_otp(email=email, otp=otp):
#             return Response({"message": "your Account verified"}, status=status.HTTP_202_ACCEPTED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def get(self, request):
#         return Response({"message": "register successful ! Verify code sent to Email"}, status=status.HTTP_201_CREATED)


# class LoginView(APIView):
#     permission_classes = (permissions.AllowAny,)
#     serializer_class = serializers.LoginSerializer
#     authentication_classes = (authentications.CustomJWTAuthentication,)

#     def post(self, request):
#         email = request.data['email']
#         password = request.data['password']

#         user = CustomUser.objects.filter(email=email).first()
#         if user:
#             if user.check_password(password):

#                 payload = {
#                     'id': user.id,
#                     'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
#                     'iat': datetime.datetime.utcnow()
#                 }
#                 token = jwt.encode(
#                     payload, settings.SECRET_KEY, algorithm='HS256')

#                 response = Response({'Message': 'User loged in successfuly',
#                                      'jwt': token}, status=200)
#                 response.set_cookie(key='jwt', value=token, httponly=True)

#                 return response
#             raise AuthenticationFailed('incorect password')
#         else:
#             raise AuthenticationFailed('user not find')

#     def get(self, request):
#         # Check if the user is already logged in
#         if request.user.is_authenticated:
#             return Response({
#                 'message': 'You are already logged in'
#             })
#         return Response({
#             'message': 'Please login to continue'
#         })

class LogoutView(APIView):
    authentication_classes = [authentications.CustomJWTAuthentication]

    def post(self, request):
        if request.user.is_authenticated:
            logout(request)
            response = Response()
            response.delete_cookie('access_token', '/')
            response.delete_cookie('refresh_token', '/')
            response.delete_cookie('username','/')
            response.data = {'message': 'Logout successful'}
            response.status = status.HTTP_200_OK
            return response
        else:
            return Response({'message': 'User is not authenticated'}, status=status.HTTP_401_UNAUTHORIZED)



from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView
from django.contrib.auth import authenticate,logout

class MyTokenObtainPairView(TokenObtainPairView):

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

class CustomTokenRefreshView(TokenRefreshView):
    authentication_classes = [authentications.CustomJWTAuthentication]

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