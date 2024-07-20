from rest_framework import serializers
from account.models import CustomUser
from django.db.models import Q
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _




class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        # todo you can use password validator min_length=8, max_length=128,
        write_only=True,  style={'input_type': 'password'})
    password2 = serializers.CharField(
        write_only=True, style={'input_type': 'password'})

    class Meta:
        model = CustomUser
        fields = ('email','phone_number' ,'password', 'password2')

    def validate(self, attrs):

        email = attrs.get('email')
        phone_number = attrs.get('phone_number')
        password = attrs.get('password')
        password2 = attrs.get('password2')

        # Check if both passwords are the same
        if password != password2:
            raise serializers.ValidationError(
                {'password': 'Passwords do not match.'})
        
        # Check for existing email and phone number
        existing_user = CustomUser.objects.filter(Q(email=email) | Q(phone_number=phone_number)).first()
        if existing_user:
            if existing_user.email == email:
                raise serializers.ValidationError({'email': 'Email already exists.'})
            if existing_user.phone_number == phone_number:
                raise serializers.ValidationError({'phone_number': 'Phone number already exists.'})
        


        #//tod do phone number and password validater
         
        # if phone_number:
        #     if not re.match(r'^(\+98|0)?9\d{9}$', phone_number):
        #         raise ValidationError(_("Invalid phone number format for Iran. It should start with '+98' followed by 10 digits.")
        #             )    

        attrs.pop('password2')  # Remove password2 from attributes since it is
        return attrs

    def create(self, validated_data):
        user = CustomUser.objects._create_user(**validated_data)
        return user

    def update(self, instance, validated_data):

        instance.email = validated_data.get('email')
        instance.password = validated_data.get('password')
        instance.phone_number = validated_data.get('phone_number')
        instance.save()
        return instance


class VerifyOtpSerialiser(serializers.Serializer):
    otp = serializers.CharField(max_length=6, required=True)
  
   

class LoginSerializer(serializers.Serializer):

    email = serializers.EmailField()
    password = serializers.CharField(
        write_only=True, style={'input_type': 'password'})

from rest_framework_simplejwt.tokens import RefreshToken

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_access_token(cls, user):
        access_token = super().get_token(user)
        access_token['email'] = user.email
        access_token['phone_number'] = user.phone_number

        return str(access_token)
    
    @classmethod
    def get_refresh_token(cls, user):
        refresh_token = RefreshToken.for_user(user)
        return str(refresh_token)
    
    @classmethod
    def get_access_refresh_token(cls,user):
        access_token = cls.get_access_token(user)
        refresh_token = cls.get_refresh_token(user)
        return {
        'refresh_token': str(refresh_token),
        'access_token': str(access_token), }






