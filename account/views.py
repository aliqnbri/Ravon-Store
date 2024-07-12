from rest_framework import permissions , status
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from account import serializers
from account.utils.emails import send_otp 
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




class VerifyOtp(GenericAPIView):

    permission_classes = [permissions.AllowAny,]

    def get(self, request):
        otp = request.query_params['otp']
        pass 




        # if serializer.is_valid(raise_exception=True):
        #     email = serializer.validated_data['email']
        #     otp = serializer.validated_data['otp']
           
        #     if check_otp(email=email, otp=otp):
        #         return Response({"message": "your Account verified"} ,status=status.HTTP_202_ACCEPTED)
        # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)    
