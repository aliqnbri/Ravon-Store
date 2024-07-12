from rest_framework import serializers
from account.models import CustomUser, CustomerProfile


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,  style={'input_type': 'password'})  #todo you can use password validator min_length=8, max_length=128,
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

