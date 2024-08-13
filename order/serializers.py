from typing import Any, Dict, List, Optional, Union
from django.db import transaction
from rest_framework import serializers
from cart.models import Cart 
from product.models import Product
from order.models import Coupon, Order, OrderItem
from product.serializers import  SimpleProductSerializer
from decimal import Decimal

class OrderItemSerializer(serializers.ModelSerializer):
    product = SimpleProductSerializer()
    class Meta:
        model = OrderItem 
        fields = ["id", "product", "price","quantity"]
        depth = 1



class OrderSerializer(serializers.ModelSerializer):
    customer= serializers.SerializerMethodField()
    count_itmes = serializers.SerializerMethodField()
    sub_total = serializers.SerializerMethodField()
    tax = serializers.SerializerMethodField()
    total_price_cost = serializers.SerializerMethodField()
    items = OrderItemSerializer(many=True, read_only=True)
    discount = serializers.SerializerMethodField()
    
    class Meta:
        model = Order
        exclude = ['id']  # Exclude the id field

        read_only_fields = ['items', 'customer', 'get_total_cost', 'created_at', 'modified_at', 'address', 'status', 'discount', 'tax', 'total_price', 'coupon', 'count_itmes', 'is_active','payment_id','ref_id' ]
     
      
    def get_discount(self,instance: Order) ->Optional[Decimal]:
        return instance.get_discount()
    
    def get_customer(self, instance: Order) -> Optional[str]:
        return instance.customer.full_name() if instance.customer else None

    def get_count_itmes(self, instance: Order) -> int:
        return len(instance)

    def get_sub_total(self, instance: Order) -> Decimal:
        return instance.get_subtotal()

    def get_tax(self, instance: Order) -> Decimal:
        return instance.get_tax()

    def get_total_price_cost(self, instance: Order) -> Decimal:
        return instance.get_total_price_cost()

    def get_created_at(self, instance: Order) -> Optional[str]:
        return instance.created_at.strftime("%Y-%m-%d %H:%M:%S") if instance.created_at else None

    def get_modified_at(self, instance: Order) -> Optional[str]:
        return instance.modified_at.strftime("%Y-%m-%d %H:%M:%S") if instance.modified_at else None


    # def get_total_price_cost(self,instance):
    #     return instance.get_total_price_cost()
    
    # def get_tax(self,instance):
    #     return instance.get_tax()    
    
    # def get_sub_total(self,instance):
    #     return instance.get_subtotal()
    
    # def get_customer(self, instance):
    #     return instance.customer.full_name()  # Assuming `full_name` is the field in `CustomerProfile`
    
    # def get_count_itmes(self,instance):
    #     return len(instance)


    # def get_created_at(self, obj):
    #     try:
    #         return obj.created_at.strftime("%Y-%m-%d %H:%M:%S")
    #     except:
    #         return None

    # def get_modified_at(self, obj):
    #     try:
    #         return obj.modified_at.strftime("%Y-%m-%d %H:%M:%S")
    #     except:
    #         None



   



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




