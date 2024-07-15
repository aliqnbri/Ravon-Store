from django.db import models
from core.models import BaseModel
from django.utils.text import slugify

# Create your models here.

class Category(BaseModel):
    """
    A Django model representing a book category in an online bookstore.
    """
    name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)
    image = models.ImageField(upload_to='media/category/', blank=True, null=True)
    
    
    class Meta:
        ordering = ['name']
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name
    
    # def get_absolute_url(self):
    #     return reverse("product:category_list", args=[self.slug])
    


    def save(self, **kwargs):
        """
        Overridden save method to create a unique slug based on the name.
        """
        self.slug = slugify(self.name)
        super().save(**kwargs)