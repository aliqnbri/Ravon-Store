from django.db.models.signals import post_save,pre_save
from django.dispatch import receiver
from account.models import CustomUser
from customer.models import CustomerProfile
from typing import Any



@receiver(post_save, sender=CustomUser)
def create_customer_profile(sender , instance, created, **kwargs):
    """
    Signal receiver function that creates a CustomerProfile instance when a CustomUser is created with role 'cu'.

    """
    if created and instance.role == instance.Role.CUSTOMER:

        CustomerProfile.objects.create(customer=instance)



@receiver(pre_save, sender=CustomUser)
def set_role_privileges(sender: Any, instance: CustomUser, **kwargs: Any) -> None:
    """
    Signal to set the role privileges for a user before saving.
    Adjusts is_staff, is_superuser, and staff_role based on the user's role.
    """
    instance.role = get_set_role(instance)


def get_set_role(user_instance: CustomUser) -> str:
    """
    Sets the user instance's privileges based on their role.
    Returns a string representing the role, or an error message if the role is invalid.
    """
    match user_instance.role:
        case CustomUser.Role.ADMIN:
            user_instance.is_staff = True
            user_instance.is_superuser = True
            user_instance.staff_role = None
            return "ADMIN"
        case CustomUser.Role.STAFF:
            user_instance.is_staff = True
            user_instance.is_superuser = False
            return "STAFF"
        case CustomUser.Role.CUSTOMER:
            user_instance.is_staff = False
            user_instance.is_superuser = False
            user_instance.staff_role = None
            return "CUSTOMER"
        case _:
            return "Invalid role ID"
