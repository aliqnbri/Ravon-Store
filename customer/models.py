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

    def get_address(self):
        return f"Address : {self.city} ,{self.street}, {self.postal_code}"

    def get_full_address(self):
        return f"{self.country},{self.city}, {self.state},{self.street}, {self.postal_code}"


class CustomerProfile(models.Model):
    class Gender(models.TextChoices):
        MALE = 'male', _('Male')
        FEMALE = 'female', _('Female')

    customer = models.OneToOneField(
        CustomUser, on_delete=models.CASCADE, related_name='customer_profile')
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    gender = models.CharField(
        max_length=6, choices=Gender.choices, null=True, blank=True)
    avatar = models.ImageField(
        upload_to='media/avatars/', null=True, blank=True)
    address = models.ForeignKey(
        Address, null=True, blank=True, on_delete=models.CASCADE)

    @admin.display
    def full_name(self):
        return self.first_name + " " + self.last_name

    @property
    def get_username(self):
        return f'{self.username}'
    
    def get_default_address(self):
        return self.address_set.filter(is_default=True).first()


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
