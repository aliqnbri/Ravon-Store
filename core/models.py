from django.db import models
from core.managers import SoftDeleteManager
from django.utils import timezone

# Create your models here.
class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField()

    objects = SoftDeleteManager()

    def delete(self, using=None, keep_parents=False):
        self.deleted_at = timezone.now()
        self.save()


    class Meta:
        abstract = True




class ShopInfo(BaseModel):
    name = models.CharField(max_length = 500)
    phone = models.CharField(max_length = 11)
    address = models.TextField()
    email = models.EmailField()
    image = models.ImageField(upload_to = 'cafe_info')
    logo = models.ImageField(upload_to='logo')