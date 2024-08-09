from rest_framework import serializers
from typing import Any, Dict, Optional
from decimal import Decimal
from product.models import Product
from cart.models import Cart
from product.serializers import ProductSerializer
from order.models import Coupon

class CartItemSerializer(serializers.Serializer):
    product = ProductSerializer()
    quantity = serializers.IntegerField()
    total_price = serializers.DecimalField(max_digits=10, decimal_places=2)
    
    def to_representation(self, instance: Dict[str, Any]) -> Dict[str, Any]:
        product_data = ProductSerializer(instance['product']).data
        return {
            'product': product_data,
            'quantity': instance['quantity'],
            'total_price': instance['total_price']
        }




class CartSerializer(serializers.Serializer):
    items = CartItemSerializer(many=True)
    subtotal = serializers.DecimalField(max_digits=10, decimal_places=2)
    tax = serializers.DecimalField(max_digits=10, decimal_places=2)
    discount = serializers.DecimalField(max_digits=10, decimal_places=2)
    total_amount = serializers.DecimalField(max_digits=10, decimal_places=2)
    coupon = serializers.SerializerMethodField()
    

    def get_coupon(self, obj: Cart) -> Optional[Dict[str, Any]]:
        if obj.coupon:
            return {
                'id': obj.coupon.id,
                'code': obj.coupon.code,
                'discount': obj.coupon.discount,
                'discount_amount': obj.coupon.discount_amount,
                'valid_from': obj.coupon.valid_from,
                'expiration_date': obj.coupon.expiration_date,
                'count': obj.coupon.count,
            }
        return None


    def get_coupon(self, obj):
        if obj.coupon:
            return {
                'id': obj.coupon.id,
                'code': obj.coupon.code,
                'discount': obj.coupon.discount,
                'discount_amount': obj.coupon.discount_amount,
                'valid_from': obj.coupon.valid_from,
                'expiration_date': obj.coupon.expiration_date,
                'count': obj.coupon.count,
            }
        return None
    
    def to_representation(self, instance):
        product = instance['product']
        return {
            'product': ProductSerializer(product).data,
            'quantity': instance['quantity'],
            'total_price': instance['total_price']
        }