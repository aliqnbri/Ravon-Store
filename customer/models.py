from django.db import models
from core.models import BaseModel
from account.models import CustomUser
from product.models import Product
from django.utils.translation import gettext_lazy as _


from django.contrib.contenttypes.fields import GenericForeignKey , GenericRelation
from django.contrib.contenttypes.models import ContentType

# Create your models here.
class Address(BaseModel):
    """
    Address Model for user's address 
    """
    country = models.CharField(max_length = 200,null = True , blank = True)
    state = models.CharField(max_length = 200,null = True , blank = True)
    city = models.CharField(max_length=50)
    street = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    detail = models.TextField()
    latitude = models.DecimalField(max_digits=9, decimal_places=2,null = True , blank = True)
    longitude = models.DecimalField(max_digits=9, decimal_places=2,null = True , blank = True)
    description = models.TextField(null= True , blank = True)

    def get_address(self):
        return f"Address : {self.city} ,{self.street}, {self.postal_code}"



class CustomerProfile(models.Model):
    class Gender(models.TextChoices):
        MALE = 'male', _('Male')
        FEMALE = 'F', _('Female')

    user = models.OneToOneField(CustomUser ,on_delete=models.CASCADE)
    gender = models.CharField(max_length=6, choices=Gender.choices, null=True, blank=True)
    avatar = models.ImageField(upload_to='media/avatars/', null=True, blank=True)
    address = models.ForeignKey(Address, null=True, blank=True, on_delete=models.CASCADE )


class WishListItem(BaseModel):
    customer = models.ForeignKey(CustomerProfile,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete = models.PROTECT)    



class Comment(BaseModel):
    body = models.TextField()
    is_published = models.BooleanField(default=False)
    customer = models.ForeignKey(CustomerProfile , on_delete = models.PROTECT)

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.CharField(max_length=200)
    content_object = GenericForeignKey('content_type', 'object_id')

    comment = GenericRelation("Comment", related_query_name='comment')

    def __str__(self):
        return self.body