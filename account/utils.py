from rest_framework_simplejwt.tokens import RefreshToken
import string ,random
from django.conf import settings
from celery import shared_task
from django.core.mail import send_mail
from Ecommerce.redis_client import redis_client
import jwt
from typing import Optional
import datetime

cache = redis_client()


# @shared_task
def send_otp(email: str) -> None:
    """
    Function to send an OTP (One Time Password) to the provided email address.
    """
    subject: str = 'Register Verification'
    otp: str = ''.join(random.choices(string.digits, k=6))  # Generate a 6-digit OTP
    print(otp)

    # Cache the OTP and its expiration time (2 minutes)
    # cache = redis_client()
    cache.set(email, otp, ex=120)
    

    message: str = f'Your verification otp is: {otp}'
    email_from: str = settings.EMAIL_HOST

    # Sending the OTP email
    send_mail(subject, message, email_from, [email], fail_silently=False)

    return otp


def check_otp(email: str, otp: str) -> bool:

    cached_otp = cache.get(email)
    
    if cached_otp is None:
        raise ValueError ("OTP has not been sent or has expired")
    
    if cached_otp == otp:
        cache.delete(email)
        return True
    return False





def generate_tokens(user):
    refresh_token = RefreshToken.for_user(user)
    access_token = refresh_token.access_token
    access_token['email'] = user.email
    access_token['phone_number'] = user.phone_number

    return map(str, (access_token, refresh_token))

    

def decode_token(token):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None
    


class JWTService:
    secret_key = settings.SECRET_KEY
    algorithm = 'HS256'

    @classmethod
    def token_generator(cls, user: dict, expiry_days: int = 7) -> str:
        payload = {
            'user_id': user['id'],
            'username': user['username'],
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=expiry_days),
            'iat': datetime.datetime.utcnow()
        }
        token = jwt.encode(payload, cls.secret_key, cls.algorithm)
        return token

    @classmethod
    def refresh_token_generator(self, user: dict, expiry_days: int = 30) -> str:
        """
        Generates a refresh token for a user.
        """
        payload = {
            'user_id': user['id'],
            'username': user['username'],
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=expiry_days),
            'iat': datetime.datetime.utcnow()
        }
        refresh_token = jwt.encode(
            payload, self.secret_key, algorithm=self.algorithm)
        return refresh_token

    @classmethod
    def new_token_generator(cls, refresh_token: str) -> Optional[str]:
        """
        Generates a new access token if the provided refresh token is valid.
        """
        if not (payload := cls.is_token_valid(refresh_token)):
            return None

        user = {
            'id': payload['user_id'],
            'username': payload['username']
        }
        new_access_token = cls.token_generator(user)
        return new_access_token

    @classmethod
    def is_token_valid(cls, token: str) -> Optional[dict]:
        try:
            payload = jwt.decode(token, cls.secret_key,
                                 algorithms=[cls.algorithm])
            return payload
        except jwt.ExpiredSignatureError:
            # Token has expired
            return None
        except jwt.InvalidTokenError:
            # Token is invalid or corrupted
            return None
        except jwt.DecodeError:
            # Token cannot be decoded
            return None
        
    @classmethod
    def decode_token(cls, token: str) -> Optional[dict]:
        """
        Decodes a JWT token and returns the payload.
        """
        try:
            payload = jwt.decode(token, cls.secret_key, algorithms=[cls.algorithm])
            return payload
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None    






        
