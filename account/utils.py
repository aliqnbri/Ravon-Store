from django.core.mail import send_mail
import string ,random ,time
from django.conf import settings
from celery import shared_task
from typing import Any
from Ecommerce.redis_client import redis_client
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


# get user role number and set instance privileges for that role in pre_save signal
def get_set_role(user_instance):
    match user_instance.role:
        case 'ADMIN':
            user_instance.is_staff = True
            user_instance.is_superuser = True
            user_instance.staff_role = None
            return "ADMIN"
        case 'STAFF':
            user_instance.is_staff = True
            user_instance.is_superuser = False
            return "STAFF"
        case 'CUSTOMER':
            user_instance.is_staff = False
            user_instance.is_superuser = False
            user_instance.staff_role = None
            return "CLIENT"
        case _:
            return "Invalid role ID"
        
        
