from rest_framework import serializers
from account.models import CustomUser, CustomerProfile

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
        fields = ('email', 'password', 'password2')

    def validate(self, attrs):

        email = attrs.get('email')
        phone_number = attrs.get('phone_number')
        password = attrs.get('password')
        password2 = attrs.get('password2')

        # Check if both passwords are the same
        if password != password2:
            raise serializers.ValidationError(
                {'password': 'Passwords do not match.'})

        if CustomUser.objects.filter(email=email).exists():
            raise serializers.ValidationError(
                {'email': 'Email already exists.'})

        attrs.pop('password2')  # Remove password2 from attributes since it is
        return attrs

    def create(self, validated_data):
        user = CustomUser.objects._create_user(**validated_data)
        user.set_password(validated_data.get('password'))
        return user

    def update(self, instance, validated_data):

        instance.email = validated_data.get('email')
        instance.password = validated_data.get('password')
        instance.phone_number = validated_data.get('phone_number')
        instance.save()
        return instance


class VerifyOtpSerialiser(serializers.Serializer):
    otp = serializers.CharField(max_length=6, required=True)
    email = serializers.EmailField()
   

class LoginSerializer(serializers.Serializer):

    email = serializers.EmailField()
    password = serializers.CharField(
        write_only=True, style={'input_type': 'password'})

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        user = CustomUser.objects.filter(email=email).first()
        if not user:
            raise serializers.ValidationError('User not found')
        if not user.check_password(password):
            raise serializers.ValidationError('Incorrect password')
        return attrs






# ser = authenticate(request=self.context.get('request'),
#                                 email=email, password=password
#                                 )

#             if not user:
#                 msg = _('Unable to log in with provided credentials.')
#                 raise serializers.ValidationError(msg, code='authorization')
#             attrs['user'] = user
#             return attrs
#         else:
#             msg = _('Must include "username" and "password".')
#             raise serializers.ValidationError(msg, code='authorization')