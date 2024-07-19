from django.db import models

# Create your models here.
class Address(BaseModel):
    """
    Address Model for user's address 
    """
    street = models.CharField(max_length=100)
    city = models.CharField(max_length=50)
    postal_code = models.CharField(max_length=20)
    detail = models.TextField()

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