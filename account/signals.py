from django.db.models.signals import post_save
from django.dispatch import receiver
from account.models import CustomUser
from customer.models import CustomerProfile



@receiver(post_save, sender=CustomUser)
def create_customer_profile(sender, instance, created, **kwargs):
    """
    Signal receiver function that creates a CustomerProfile instance when a CustomUser is created with role 'cu'.

    Args:
        sender: The model class that sends the signal (CustomUser in this case).
        instance: The instance of the model that triggered the signal (CustomUser instance).
        created (bool): A boolean indicating if the instance was created or updated.
        **kwargs: Additional keyword arguments.

    Returns:
        None
    """
    if created and instance.Role.CUSTOMER :
        CustomerProfile.objects.create(customer=instance)
