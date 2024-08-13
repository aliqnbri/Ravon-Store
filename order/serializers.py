from typing import Any, Dict, Optional
from cart.models import Cart  # Assuming you have this Cart model defined somewhere
from order.models import Coupon, Order, OrderItem
from django.core.exceptions import ValidationError

from typing import Any, Dict, List, Optional
from django.db import transaction
from rest_framework import serializers
from order.models import Order, Coupon, OrderItem
from cart.models import Cart

from product.models import Product
from decimal import Decimal
from django.urls import reverse_lazy

from product.serializers import  SimpleProductSerializer
from cart.serializers import CartSerializer

class OrderItemSerializer(serializers.ModelSerializer):
    product = SimpleProductSerializer()
    class Meta:
        model = OrderItem 
        fields = ["id", "product", "price","quantity"]
        depth = 1



class OrderSerializer(serializers.ModelSerializer):
    items = CartSerializer()

    class Meta:
        model = Order
        fields = ['customer', 'address', 'items']
      

        read_only_fields = ['items', 'customer',
                            'get_total_cost', 'created_at', 'modified_at', 'address', 'status',  'discount', 'tax', 'total_price', 'coupon', 'total_items_quantity']

    def get_created_at(self, obj):
        try:
            return obj.created_at.strftime("%Y-%m-%d %H:%M:%S")
        except:
            return None

    def get_modified_at(self, obj):
        try:
            return obj.modified_at.strftime("%Y-%m-%d %H:%M:%S")
        except:
            None

   

    # def to_representation(self, instance):
   
    #     representation = super().to_representation(instance)
  
    #     return representation



class CreateOrderSerializer(serializers.Serializer):

    def save(self, **kwargs):
        with transaction.atomic():
            request = self.context.get('request')
            user = request.user.customer_profile
            address = user.address.get_full_address()

            order = Order.objects.create(customer = user,
                                         address = address,
                    
                                         )
            cart = Cart(request)
            order_items = [
                OrderItem(order=order, 
                    product=Product.objects.get(id = item['product']['id']), 
                    quantity=item['quantity'],
                    price = item['price']
                    )
            for item in cart
            ]
            OrderItem.objects.bulk_create(order_items)
            cart.clear()
            return order
        
class UpdateOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order 
        fields = ["status"]




