from django.db import models
from core.models import BaseModel
from customer.models import CustomerProfile
from product.models import Product
from decimal import Decimal
from django.utils.translation import gettext_lazy as _
# Create your models here.
from typing import List, Optional


class Coupon(BaseModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    code = models.CharField(max_length=10)
    discount = models.DecimalField(
        max_digits=5, decimal_places=2, null=True, blank=True)
    discount_amount = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True)
    

    valid_from = models.DateTimeField()
    expiration_date = models.DateField(editable=True, blank=True, null=True)
    count = models.IntegerField()


    def calculate_discounted_price(self):
        if self.discount_percent is not None:
            return self.product.price * (1 - (self.discount_percent / 100))
        elif self.discount_amount is not None:
            return self.product.price - self.discount_amount
        else:
            return self.product.price



class Order(BaseModel):
    """Reprisent customers orders"""

    class OrderStatus(models.TextChoices):
        PENDING = 'pending', _('Pending')
        SHIPPED = 'shipped', _('Shipped'),
        DELIVERD = 'delivered', _('Delivered'),
        CANCELED = 'canceled', _('Canceled'),
        RETURNED = 'returned', _('Returned'),
        CONFIRMED = "confirmed", _("Confirmed")
        PAYED = "paid", _("Paid")

    customer = models.ForeignKey(CustomerProfile, on_delete=models.CASCADE)
    address = models.TextField(null = True , blank = True) 
    payment_id = models.CharField(max_length = 100 ,null = True , blank = True )
    ref_id = models.CharField(max_length = 25,null = True , blank = True)
    discount = models.IntegerField(null=True, blank=True)
    coupon = models.ForeignKey(Coupon,related_name='orders',on_delete = models.SET_NULL,null=True,blank = True)
    status = models.CharField(max_length=10,
                                    choices=OrderStatus.choices,
                                    default=OrderStatus.PENDING, blank=True)

    class Meta:
        verbose_name = _('Order')
        verbose_name_plural = _('Orders')
        ordering = ['-updated_at' , '-created_at']
        indexes = [
            models.Index(fields=['-created_at']),
        ]

    def __str__(self):
        return f'Order {self.id}'
    

    def get_discount(self) -> Decimal:
        """
        Calculate the discount amount.
        """
        return (self.coupon.discount / 100) * self.get_subtotal() if self.coupon else Decimal(0)

    

    def get_subtotal(self):
        return sum(item.price * item.quantity for item in self.items.all())

    def get_tax(self, tax_rate: Decimal = Decimal(0.3)) -> Decimal:
        return round((self.get_subtotal()) * tax_rate / 100, 2)

    def get_total_price_cost(self, tax_rate=Decimal(0.3)) -> Decimal:
        return Decimal((self.get_subtotal()) + Decimal(self.get_tax(tax_rate)) - Decimal(self.get_discount()))

    def get_items(self) -> List:
        return self.items.all()
    


    
    def __len__(self):
        """
        Count all items in the order
        """
        return sum(item["quantity"] for item in self.items.values())


class OrderItem(BaseModel):
    order = models.ForeignKey(Order,
                              related_name='items',
                              on_delete=models.CASCADE)
    product = models.ForeignKey(Product,
                                related_name='order_items',
                                on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=1000,
                                decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        verbose_name = _('Order Item')
        verbose_name_plural = _('Order Items')
        ordering = ['-created_at']

    def __str__(self):
        return f"Order Item #{self.id} - Product: {self.product.name} X Quantity: {self.quantity}"
    
    def get_cost(self):
        return self.price * self.quantity

    
    def get_customer_name(self):
        return self.order.customer.full_name() if self.order.customer else "Unknown"
