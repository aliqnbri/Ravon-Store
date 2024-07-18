from django.db import transaction
from rest_framework import serializers
from order.models import Order,Coupon,OrderItem

from product.serializers import ProductSerializer,SimpleProductSerializer
from product.models import Product



class OrderItemSerializer(serializers.ModelSerializer):
    product = SimpleProductSerializer()
    class Meta:
        model = OrderItem 
        fields = ["id", "product", "price","quantity"]
        depth = 1


        