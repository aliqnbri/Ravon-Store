# from django.contrib.auth import get_user_model, user_login_failed
# from django.contrib.auth.backends import ModelBackend
# from django.contrib.auth.models import update_last_login
# from django.core.cache import cache
# from django.views.decorators.debug import sensitive_variables
# from rest_framework import serializers
# from rest_framework.exceptions import AuthenticationFailed
# from rest_framework_simplejwt.tokens import RefreshToken

# UserModel = get_user_model()


# class TokenAPISerializer(serializers.Serializer):
#     email_field = 'email'
#     token_class = RefreshToken

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)

#         self.user = None
#         self.fields[self.email_field] = serializers.EmailField()
#         self.fields["otp"] = serializers.CharField()

#     def validate(self, attrs):
#         authenticate_kwargs = {
#             self.email_field: attrs[self.email_field],
#             "otp": attrs["otp"],
#         }
#         try:
#             authenticate_kwargs["request"] = self.context["request"]
#         except KeyError:
#             pass

#         self.user = booking_authenticate(**authenticate_kwargs)

#         if not self.user:
#             raise AuthenticationFailed("invalid_otp", )

#         refresh = self.get_token(self.user)

#         data = {"refresh": str(refresh), "access": str(refresh.access_token)}

#         update_last_login(None, self.user)

#         return data

#     @classmethod
#     def get_token(cls, user):
#         return cls.token_class.for_user(user)

#     def update(self, instance, validated_data):
#         pass

#     def create(self, validated_data):
#         pass


# class BookingBackend(ModelBackend):
#     def authenticate(self, request, email=None, otp=None, **kwargs):
#         if email is None:
#             email = kwargs.get('email')
#         if email is None or otp is None:
#             return
#         try:
#             user = UserModel._default_manager.get_by_natural_key(email)
#         except UserModel.DoesNotExist:
#             pass
#         else:
#             if otp == str(cache.get(email)) and self.user_can_authenticate(user):
#                 return user


# @sensitive_variables("credentials")
# def booking_authenticate(request=None, **credentials):
#     backend = BookingBackend()
#     user = backend.authenticate(request, **credentials)

#     if user is None:
#         user_login_failed.send(
#             sender=__name__, request=request
#         )

#     return user