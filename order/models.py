from django.db import models
from core.models import BaseModel
from account.models import CustomerProfile
from django.utils.translation import gettext_lazy as _
# Create your models here.

class Order(BaseModel):
    """Reprisent customers orders"""
    
    class ORDER_STATUS(models.TextChoices):
        PENDING = 'pending', _('Pending')
        SHIPPED = 'shipped', _('Shipped'),
        DELIVERD = 'delivered', _('Delivered'),
        CANCELLED = 'cancelled', _('Cancelled'),
        RETURNED = 'returned', _('Returned')




    customer = models.ForeignKey(CustomerProfile, on_delete=models.CASCADE)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    order_status = models.CharField(max_length=10, 
                                    choices=ORDER_STATUS.choices, 
                                    default=ORDER_STATUS.PENDING)
    discount = models.IntegerField(null=True, blank=True)
    class Meta:
        verbose_name = _('Order')
        verbose_name_plural = _('Orders')
        ordering = ['-updated_at']
        indexes = [
            models.Index(fields=['-created_at']),
        ]

    def __str__(self):
        return f'Order {self.id} - {self.customer.first_name} {self.customer.last_name}'
    

    def get_total_cost(self):
        total_cost = self.get_total_cost_before_discount()
        return total_cost - self.get_discount()
    
    def get_discount(self):
        total_cost = self.get_total_cost_before_discount()
        if self.discount:
            return total_cost * (self.discount / float(100))
        return float(0)
  



