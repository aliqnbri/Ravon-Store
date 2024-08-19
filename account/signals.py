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
def set_role_privileges(sender: type[CustomUser], instance: CustomUser, **kwargs: Any) -> None:
    """
    Signal to set the role privileges for a user before saving.
    Adjusts role-related settings based on the user's role.
    """
    match instance.role:
        case CustomUser.Role.ADMIN:
            instance.is_superuser = True
            instance.staff_role = CustomUser.StaffRoles.SUPERVISOR  # Admins are supervisor too have a specific staff role
        case CustomUser.Role.STAFF:
            instance.is_superuser = False
            if not instance.staff_role:
                instance.staff_role = CustomUser.StaffRoles.OPERATOR  # Default staff role if not set
        case CustomUser.Role.CUSTOMER:
            instance.is_superuser = False
            instance.staff_role = None  # Customers do not have a staff role
        case _:
            raise ValueError(f"Invalid role ID: {instance.role}")
