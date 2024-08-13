
from typing import Any, Dict, List, Optional
from django.db import transaction
from rest_framework import serializers
from order.models import Order, Coupon, OrderItem
from cart.models import Cart
from cart.serializers import CartSerializer
from product.serializers import ProductSerializer
from product.models import Product
from decimal import Decimal
from django.urls import reverse_lazy
from cart.serializers import OrderItemSerializer


class OrderSerializer(serializers.ModelSerializer):
    status = serializers.CharField(source='get_status_display')
    customer = serializers.StringRelatedField()
    address = serializers.SerializerMethodField()
    items = OrderItemSerializer(many=True, source='order_items')
    created_at = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = [
            'customer', 'address', 'status', 'payment_id',  'items',
            'created_at',
        ]
        read_only_fields = [
            'items', 'customer', 'created_at',
            'modified_at', 'address', 'status', 'payment_id',
        ]

    def get_address(self, instance):
        return instance.customer.address.get_full_address()

    def get_created_at(self, obj):
        return obj.created_at.strftime("%Y-%m-%d %H:%M:%S") if obj.created_at else None

    def get_modified_at(self, obj):
        return obj.modified_at.strftime("%Y-%m-%d %H:%M:%S") if obj.modified_at else None

    def get_tax(self, obj):
        # Assuming you have a method to calculate tax
        return obj.get_total_cost() * Decimal(0.05)  # Example tax calculation

    def get_coupon(self, obj):
        if obj.coupon:
            return {
                'code': obj.coupon.code,
                'discount': obj.coupon.discount,
                'valid_from': obj.coupon.valid_from,
                'expiration_date': obj.coupon.expiration_date,
            }
        return None

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        # Assuming Cart is session-based and initialized with request
        cart = Cart(self.context['request'])
        representation['items'] = CartSerializer(cart).data

        return representation


class CreateOrderSerializer(serializers.Serializer):
    coupon_code = serializers.CharField(required=False, allow_blank=True)

    def validate(self, attrs: Dict[str, Any]) -> Dict[str, Any]:
        if coupon_code := attrs.get('coupon_code'):
            if not (coupon := Coupon.objects.filter(code=coupon_code, is_active=True).first()):
                raise serializers.ValidationError(
                    "Invalid or inactive coupon code.")
            attrs['coupon'] = coupon
        return attrs

    def create_order_items(self, order: Order, cart: Cart) -> Decimal:
        total_price = Decimal(0)

        order_items = [
            OrderItem(
                order=order,
                product=(product := item['product']),
                quantity=(quantity := item['quantity']),
                price=(price := item['price']),
            ) for item in cart if not (
                setattr(product, 'available_quantity',
                        product.available_quantity - quantity) or product.save()
            ) and not ((total_price := total_price + price * quantity))]

        product.available_quantity -= quantity
        product.save
        total_price += price * quantity

        OrderItem.objects.bulk_create(order_items)
        return total_price

    def create(self, validated_data: Dict[str, Any]) -> Order:
        request = self.context.get('request')
        customer = request.user.customer_profile
        cart = Cart(request)
        with transaction.atomic():
            # Create the order
            order = Order.objects.create(
                customer=customer,
                coupon=validated_data.get('coupon'),
                status=Order.OrderStatus.PENDING,
                address=customer.address.get_full_address(),
                total_amount=Decimal(0)
            )
        total_price = self.create_order_items(order, cart)
        
        if coupon := order.coupon:
            total_price -= (coupon.discount / 100) * total_price

        # Calculate tax and final total
        tax = cart.get_tax()
        order.total_amount = total_price + tax
        order.save()

        # Clear the cart after order is created
        cart.clear()

        return order
