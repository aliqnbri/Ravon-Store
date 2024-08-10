from rest_framework import serializers
from typing import Any, Dict, Optional
from decimal import Decimal
from product.models import Product
from cart.models import Cart
from product.serializers import ProductSerializer
from order.models import Coupon, OrderItem



class OrderItemSerializer(serializers.ModelSerializer):
    product = serializers.SerializerMethodField()
    slug = serializers.SerializerMethodField(read_only=True)
    quantity = serializers.ChoiceField(
        choices=[(i, i) for i in range(1, 100)],  # adjust the range as needed
        required=True)

    class Meta:
        model = OrderItem
        fields = ["product","slug", "price", "quantity"]
        depth = 1

    def get_slug(self,obj):
        if obj.product: 
            return obj.product.slug
    def get_product(self, obj):
        if obj.product:
            return obj.product.name
        return "Product not in list"    

    def validate(self, data):
        product = data['product']
        quantity = data['quantity']
        if product.available_quantity < quantity:
            raise serializers.ValidationError(
                f"Insufficient quantity for product {product.name}")
        return data

    def create(self, validated_data):
        product = validated_data['product']
        quantity = validated_data['quantity']
        product.available_quantity -= quantity
        product.save()
        return super().create(validated_data)



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
                'code': obj.coupon.code,
                'discount': obj.coupon.discount,
                'discount_amount': obj.coupon.discount_amount,
                'valid_from': obj.coupon.valid_from,
                'expiration_date': obj.coupon.expiration_date,
                'count': obj.coupon.count,
            }
        return None

    def to_representation(self, instance: Cart) -> Dict[str, Any]:
        items = [OrderItemSerializer(item).data for item in instance.get_items()]
        return {
            'subtotal': instance.get_subtotal(),
            'discount': instance.get_discount(),
            'tax': instance.get_tax(),
            'total_price': instance.get_total_price(tax_rate=Decimal(0.5)),
            'coupon': self.get_coupon(instance),
            'items': items,
            "total_items_quantity": instance.__len__()
        }
