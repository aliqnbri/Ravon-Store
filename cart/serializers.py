from rest_framework import serializers
from .models import Cart
from product.serializers import ProductSerializer

class CartItemSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    price = serializers.DecimalField(max_digits=3,decimal_places=2 )
    quantity = serializers.IntegerField()
    total_price = serializers.DecimalField(max_digits=3,decimal_places=2)




class CartSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    quantity = serializers.IntegerField(default=1)
    coupon = serializers.SerializerMethodField()
    discount = serializers.DecimalField(max_digits=3,decimal_places=2)
    total_price = serializers.DecimalField(max_digits=3,decimal_places=2)
    items = CartItemSerializer(many=True)

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