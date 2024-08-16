from django.db import models
from core.models import BaseModel
from account.models import CustomUser
from django.utils.translation import gettext_lazy as _
from django.contrib import admin


from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType

# Create your models here.



class Address(BaseModel):
    """
    Address Model for user's address 
    """
    customer_profile = models.ForeignKey('CustomerProfile', on_delete=models.CASCADE, related_name='addresses')
    country = models.CharField(max_length=200, null=True, blank=True)
    state = models.CharField(max_length=200, null=True, blank=True)
    city = models.CharField(max_length=50)
    street = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    latitude = models.DecimalField(
        max_digits=9, decimal_places=2, null=True, blank=True)
    longitude = models.DecimalField(
        max_digits=9, decimal_places=2, null=True, blank=True)
    secondary_address = models.TextField(null=True, blank=True)
    is_default = models.BooleanField(default=False)


    def get_full_address(self) -> str:
        """Returns the full address in a formatted string"""
        return f"Address: {self.country},{self.city}, {self.state},{self.street}, {self.postal_code}"

    def __str__(self) -> str:
        return self.get_full_address()


class CustomerProfile(models.Model):
    """
    Customer Profile Model
    """
    class Gender(models.TextChoices):
        MALE = 'male', _('Male')
        FEMALE = 'female', _('Female')

    customer = models.OneToOneField(
        CustomUser, on_delete=models.CASCADE, related_name='customer_profile')
    gender = models.CharField(
        max_length=6, choices=Gender.choices, null=True, blank=True)
    avatar = models.ImageField(
        upload_to='media/avatars/', null=True, blank=True)

    @admin.display
    def full_name(self):
        return self.customer.first_name + " " + self.customer.last_name
    

    
    def get_default_address(self) -> Address:
        """Returns the customer's default address"""
        if (default_address := self.addresses.filter(is_default=True).first()):
            return default_address.get_full_address()
        return None
    
    def get_default_address(self):
        return self.address_set.filter(is_default=True).first()
    
    def __str__(self) -> str:
        return f"{self.customer.first_name} {self.customer.last_name}"





class Comment(BaseModel):
    body = models.TextField()
    is_published = models.BooleanField(default=False)
    customer = models.ForeignKey(CustomerProfile, on_delete=models.PROTECT)

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    object_id = models.CharField(max_length=200)
    content_object = GenericForeignKey('content_type', 'object_id')

    comment = GenericRelation("Comment", related_query_name='comments', related_name='parent_comment')


    def __str__(self):
        return self.body
    
    def get_comment_thread(self):
        comments = [self]
        parent = self.parent
        while parent:
            comments.insert(0, parent)
            parent = parent.parent
        return comments
