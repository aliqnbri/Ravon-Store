from rest_framework import serializers
from typing import Any, Dict, Optional
from decimal import Decimal
from product.models import Product
from cart.models import Cart
from product.serializers import ProductSerializer
from order.models import Coupon, OrderItem
from order.serializers import OrderItemSerializer


class CartSerializer(serializers.Serializer):
    items = OrderItemSerializer(many=True, source='order_items')
    subtotal = serializers.DecimalField(max_digits=10, decimal_places=2)
    tax = serializers.DecimalField(max_digits=10, decimal_places=2)
    discount = serializers.DecimalField(max_digits=10, decimal_places=2)
    total_amount = serializers.DecimalField(max_digits=100000, decimal_places=2)
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

    def to_representation(self, instance: Cart) -> Dict[str, Any]:
        items = [OrderItemSerializer(
            item).data for item in instance.get_items()]
        return {
            'items': items,
            'subtotal': instance.get_subtotal(),
            'tax': instance.get_tax(),
            'discount': instance.get_discount(),
            'total_amount': instance.get_total_price(Decimal(0.1)),
            'coupon': self.get_coupon(instance),
        }
