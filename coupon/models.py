from django.db import models
from product.models import Product


# Create your models here.


class Coupon(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    code = models.CharField(max_length=10)
    discount = models.DecimalField(
        max_digits=5, decimal_places=2, null=True, blank=True)
    discount_amount = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True)
    expiration_date = models.DateField(editable=True, blank=True, null=True)
    valid_from = models.DateTimeField()
    is_active = models.BooleanField(default=False)

    def calculate_discounted_price(self):
        if self.discount_percent is not None:
            return self.product.price * (1 - (self.discount_percent / 100))
        elif self.discount_amount is not None:
            return self.product.price - self.discount_amount
        else:
            return self.product.price
