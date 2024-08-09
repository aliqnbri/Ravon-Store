from rest_framework import serializers
from .models import Cart
from product.serializers import ProductSerializer

class CartItemSerializer(serializers.Serializer):
    product = ProductSerializer()
    quantity = serializers.IntegerField()
    total_price = serializers.DecimalField(max_digits=3,decimal_places=2)




class CartSerializer(serializers.Serializer):
    items = CartItemSerializer(many=True)
    subtotal = serializers.DecimalField(max_digits=10, decimal_places=2)
    tax = serializers.DecimalField(max_digits=10, decimal_places=2)
    discount = serializers.DecimalField(max_digits=10, decimal_places=2)
    total_amount = serializers.DecimalField(max_digits=10, decimal_places=2)
    coupon = serializers.SerializerMethodField()


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