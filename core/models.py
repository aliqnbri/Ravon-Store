from django.db import models

# Create your models here.
class BaseModel(models.Model):
    class Satus(models.TextChoices):
        ACTIVE = 'on' , 'Active'
        DEACTIVE = 'off', 'Deactive'
       
    status = models.CharField(max_length=10, choices=Satus.choices, default=Satus.ACTIVE)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)


    class Meta:
        abstract = True