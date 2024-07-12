from django.shortcuts import render
from rest_framework import permissions , status
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from account import serializers
from account.utils.emails import send
# Create your views here.


class RegisterUserView(GenericAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = serializers.RegisterSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            email = user.email

            # send verification mail to the registered user
            emails.send_otp(email=email)

            return Response({"message": f"register successful ! Verify code sent to {email}"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

