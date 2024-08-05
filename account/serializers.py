from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import serializers
from account.models import CustomUser
from django.db.models import Q
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _
from django.core.validators import EmailValidator, RegexValidator
from typing import Any, Dict


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True,  style={'input_type': 'password'},
        min_length=8, max_length=128,)
    
    password2 = serializers.CharField(
        write_only=True, style={'input_type': 'password'})
    
    email = serializers.EmailField(
        validators=[EmailValidator()]
    )
    phone_number = serializers.CharField(
        validators=[RegexValidator(
            regex=r'^(\+98|0)?9\d{9}$',
            message=_("Invalid phone number format for Iran. It should start with '+98' followed by 10 digits.")
        )]
    )

    class Meta:
        model = CustomUser
        fields = ('email', 'phone_number', 'password', 'password2')

    def validate(self, attrs: Dict[str, Any]) -> Dict[str, Any]:

        # Check if both passwords match
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({'password': _('Passwords do not match.')})
        
        # Check for existing email or phone number
        if CustomUser.objects.filter(Q(email=attrs['email']) | Q(phone_number=attrs['phone_number'])).exists():
            raise serializers.ValidationError({
                'email': _('Email or phone number already exists.')
            })

        attrs.pop('password2')
        return attrs


    def create(self, validated_data: Dict[str, Any]) -> CustomUser:
        user = CustomUser.objects._create_user(**validated_data)
        return user

    def update(self, instance: CustomUser, validated_data: Dict[str, Any]) -> CustomUser:
        instance.email = validated_data.get('email', instance.email)
        instance.phone_number = validated_data.get('phone_number', instance.phone_number)
        if 'password' in validated_data:
            instance.set_password(validated_data['password'])
        instance.save()
        return instance


class VerifyOtpSerialiser(serializers.Serializer):
    otp = serializers.CharField(max_length=6, required=True)


class LoginSerializer(serializers.Serializer):

    email = serializers.EmailField()
    password = serializers.CharField(
        write_only=True, style={'input_type': 'password'})
    
    def validate(self, attrs: Dict[str, str]) -> Dict[str, Any]:
        email = attrs.get('email')
        password = attrs.get('password')

        user = authenticate(request=self.context.get('request'), email=email, password=password)
        if not user:
            raise serializers.ValidationError(_('Unable to log in with provided credentials.'))
        
        attrs['user'] = user
        return attrs


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_access_token(cls, user)-> str:
        access_token = super().get_token(user)
        access_token['email'] = user.email
        access_token['phone_number'] = user.phone_number

        return str(access_token)

    @classmethod
    def get_refresh_token(cls, user):
        refresh_token = RefreshToken.for_user(user)
        return str(refresh_token)

    @classmethod
    def get_access_refresh_token(cls, user):
        access_token = cls.get_access_token(user)
        refresh_token = cls.get_refresh_token(user)
        return {
            'refresh_token': str(refresh_token),
            'access_token': str(access_token), }
