from rest_framework_simplejwt.tokens import RefreshToken
import string ,random
from django.conf import settings
from celery import shared_task
from django.core.mail import send_mail
from Ecommerce.redis_client import redis_client
import jwt


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
    refresh = RefreshToken.for_user(user)
    access_token = str(refresh.access_token)
    
    # Store email and phone number in the token's payload
    payload = jwt.decode(access_token, settings.SECRET_KEY, algorithms=['HS256'])
    payload['email'] = user.email
    payload['phone_number'] = user.phone_number
    payload['exp'] = settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME']  # Set token expiry
    access_token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')

    return access_token, str(refresh)

def decode_token(token):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None



        
        
