from typing import Any, Dict, Optional
from cart.models import Cart  # Assuming you have this Cart model defined somewhere
from order.models import Coupon, Order, OrderItem
from django.core.exceptions import ValidationError

from typing import Any, Dict, List, Optional
from django.db import transaction
from rest_framework import serializers
from order.models import Order, Coupon, OrderItem
from cart.models import Cart

from product.serializers import ProductSerializer
from product.models import Product
from decimal import Decimal


class SimpleProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["name"]


class OrderItemSerializer(serializers.ModelSerializer):
    product = serializers.SerializerMethodField()
    slug = serializers.SerializerMethodField(read_only=True)
    quantity = serializers.ChoiceField(
        choices=[(i, i) for i in range(1, 100)],  # adjust the range as needed
        required=True)

    class Meta:
        model = OrderItem
        fields = ["product", "slug", "price", "quantity"]
        depth = 1

    def get_slug(self, obj):
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


class OrderSerializer(serializers.ModelSerializer):
    customer = serializers.StringRelatedField()
    address = serializers.SerializerMethodField()
    items = OrderItemSerializer(many=True, source='order_items')
    created_at = serializers.SerializerMethodField()
    modified_at = serializers.SerializerMethodField()

    def get_address(self, instance):
        request = self.context.get('request')
        customer = request.user.customer_profile
        return customer.address.get_full_address()

    class Meta:
        model = Order
        fields = ['customer', 'address', 'created_at', 'modified_at', 'items']
        depth = 1

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

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        order = Order.objects.create(**validated_data)
        for item_data in items_data:
            OrderItem.objects.create(order=order, **item_data)
        return order

    def update(self, instance, validated_data):
        items_data = validated_data.pop('items', [])
        instance.status = validated_data.get('status', instance.status)
        instance.coupon = validated_data.get('coupon', instance.coupon)
        instance.discount = validated_data.get('discount', instance.discount)
        instance.save()
        for item_data in items_data:
            order_item = OrderItem.objects.filter(
                id=item_data['id'], order=instance).first()
            if order_item:
                order_item.quantity = item_data.get(
                    'quantity', order_item.quantity)
                order_item.price = item_data.get('price', order_item.price)
                order_item.save()
            else:
                OrderItem.objects.create(order=instance, **item_data)
        return instance

    def to_representation(self, instance):
        data = super().to_representation(instance)
        items = data.pop('items')
        data['items'] = items
        return data


class CreateOrderSerializer(serializers.Serializer):
    coupon_code = serializers.CharField(required=False, allow_blank=True)

    def validate(self, attrs: Dict[str, Any]) -> Dict[str, Any]:
        coupon_code = attrs.get('coupon_code')
        if not coupon_code:
            return None
        if not (coupon := Coupon.objects.filter(code=coupon_code, is_active=True).first()):
            raise serializers.ValidationError(
                "Invalid or inactive coupon code.")
        attrs['coupon'] = coupon
        return attrs

    def create_order_items(self, order: Order, products: List[Product], quantity: int, coupon_code: Optional[str] = None) -> None:
        order_items = []
        total_price = 0
        coupon = Coupon.objects.filter(
            code=coupon_code, is_active=True).first() if coupon_code else None

        for product_data in products:
            product = Product.objects.get(id=product_data['id'])
            price = product.price
            if coupon:
                discounted_price = coupon.calculate_discounted_price(price)
                price = min(price, discounted_price)

            order_item = OrderItem(
                order=order, product=product, quantity=quantity, price=price)
            order_items.append(order_item)
            total_price += price * quantity

            # Update product's available quantity
            product.available_quantity -= quantity
            product.save()

        OrderItem.objects.bulk_create(order_items)
        order.total_amount = total_price
        order.save()

    def create(self, validated_data: Dict[str, Any]) -> Order:
        request = self.context.get('request')
        cart = Cart(request)
        products = validated_data.get('products')
        quantity = validated_data.get('quantity', 1)
        cart.add(product=products, quantity=quantity)

        coupon_code = validated_data.get("coupon_code", None)
        customer = request.user.customer_profile

        with transaction.atomic():
            coupon = None
            if coupon_code:
                coupon = Coupon.objects.filter(
                    code=coupon_code, is_active=True).first()
                if not coupon:
                    raise ValidationError("Invalid coupon code provided.")
            order = Order.objects.create(customer=customer,
                                         coupon=coupon, status=Order.OrderStatus.PENDING,
                                         address=customer.address.get_full_address(),
                                         total_amount=Decimal(0))

            self.create_order_items(order, products, quantity, coupon_code)
            cart.save()
            return order

    class CouponSerializer(serializers.ModelSerializer):
        product = ProductSerializer(read_only=True)

        class Meta:
            model = Coupon
            fields = ['id', 'product', 'code', 'discount',
                      'discount_amount', 'valid_from', 'expiration_date', 'count']
            read_only_fields = ['calculate_discounted_price']

        def to_representation(self, instance):
            data = super().to_representation(instance)
            data['calculate_discounted_price'] = instance.calculate_discounted_price()
            return data
