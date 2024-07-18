from django.db import models
from django.urls import reverse
from core.models import BaseModel
from django.utils.text import slugify
from account.models import CustomerProfile

# Create your models here.

class Category(BaseModel):
    """
    model representing a book category in an online bookstore.
    """
    name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    image = models.ImageField(upload_to='media/category/', blank=True, null=True)
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True,related_name="child")

    def get_descendants(self, include_self=False):
        descendants = []
        if include_self:
            descendants.append(self)
        children = self.child.all()

        for child in children:
            descendants.append(child)  # Add the direct child
            descendants.extend(child.get_descendants(include_self=True))  # Recursively fetch descendants
        return descendants

    def __str__(self)-> str:
        return f"{self.name} --> {self.parent.__str__()}" if self.parent else self.name

    def __repr__(self)-> str:
        return f"{self.name} --> {self.parent.__repr__()}" if self.parent else self.name
    
    @property
    def is_subcategory(self):
        return self.parent is not None 
    
    class Meta:
        ordering = ['name']
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def get_absolute_url(self):
        return reverse("product:category_filter", args=[self.slug])
    

    def save(self, **kwargs):
        """
        Overridden save method to create a unique slug based on the name.
        """
        self.slug = slugify(self.name)
        super().save(**kwargs)


class Brand(BaseModel):
    name = models.CharField(max_length=200)
    about = models.TextField(null = True , blank = True)

    def __str__(self):
        return self.name


class Review(BaseModel):
    """
    A Django model representing a review for a specific book.
    """
    user = models.ForeignKey(CustomerProfile, on_delete=models.CASCADE)
    rating = models.IntegerField(
        choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')])
    comment = models.TextField(max_length=1000, blank=True)

    def __str__(self):
        return f"{self.CustomerProfile.username} commets:{self.comment}"
    

class Product(BaseModel):

    """
    A Django model representing a specific product in an online bookstore.
    """

    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    image = models.ImageField(upload_to='media/products/', blank=True, null=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.DecimalField(max_digits=20,decimal_places=2)
    is_available = models.BooleanField(default=True)
    brand = models.ForeignKey(Brand,on_delete=models.CASCADE )
    review = models.ForeignKey(Review, null=True,blank=True, on_delete=models.CASCADE, related_name='reviews')
    category = models.ManyToManyField(Category, related_name='products')    
    
    class Meta:
        ordering = ('name',)

    def save(self, **kwargs):
        """
        Overridden save method to create a unique slug based on the name.
        """
        self.slug = slugify(self.name)
        super().save(**kwargs)


    def __str__(self):
        return self.name

    # def get_absolute_url(self):
    #     return f'/{self.category.slug}/{self.slug}/'    

    def get_absolute_url(self) -> object:
        return reverse('productdetail', args=[self.pk])




class WishList(models.Model):
    user = models.OneToOneField(CustomerProfile, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product)