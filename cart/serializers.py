from rest_framework import serializers
from decimal import Decimal
from cart.models import Cart
from order.models import Coupon, OrderItem
from django.db import transaction
from typing import Any, Dict, Optional, TypeAlias, Union
from product.models import Product
from order.models import Coupon, Order, OrderItem


# Type aliases for improved readability
ValidatedData: TypeAlias = Dict[str, Any]


class CreateOrderItemSerializer(serializers.Serializer):
    product: serializers.SlugRelatedField = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Product.objects.all(),
        required=True,
        write_only=True
    )
    quantity: serializers.ChoiceField = serializers.ChoiceField(
        choices=[(i, i) for i in range(1, 100)],  # Adjust the range as needed
        required=True
    )
    coupon_code: serializers.CharField = serializers.CharField(
        required=False,
        allow_blank=True
    )

    def validate(self, attrs: ValidatedData) -> ValidatedData:
        product: Product = attrs['product']
        quantity: int = attrs['quantity']
        coupon_code: Optional[str] = attrs.get('coupon_code')

        # Lock the product row for update to prevent race conditions
        product = Product.objects.select_for_update().get(pk=product.pk)
        if product.available_quantity < quantity:
            raise serializers.ValidationError(
                f"Product {product.name} is out of stock"
            )

        # Validate coupon code if provided
        if coupon_code:
            if not (coupon := Coupon.objects.filter(code=coupon_code, is_active=True).first()):
                raise serializers.ValidationError(
                    "Invalid or inactive coupon code.")
            attrs['coupon'] = coupon

        return attrs

    def create_order_item(self, order: Order, product: Product, quantity: int, price: Decimal) -> OrderItem:
        """Helper method to create an OrderItem and update product stock."""
        # Update product's available quantity
        product.available_quantity -= quantity
        product.save()

        # Create and return the order item
        return OrderItem.objects.create(
            order=order,
            product=product,
            quantity=quantity,
            price=price
        )

    def create(self, validated_data: ValidatedData) -> OrderItem:
        request = self.context['request']
        customer = request.user.customer_profile
        product: Product = validated_data['product']
        quantity: int = validated_data['quantity']
        coupon: Optional[Coupon] = validated_data.get('coupon')

        # Calculate price with potential discount
        price: Decimal = product.price
        if coupon:
            discounted_price: Decimal = coupon.calculate_discounted_price(
                price)
            price = min(price, discounted_price)

        with transaction.atomic():
            # Create a new order
            order: Order = Order.objects.create(
                customer=customer,
                coupon=coupon,
                status=Order.OrderStatus.PENDING,
                address=customer.address.get_full_address(),
                total_amount=Decimal(0)
            )

            # Create the order item and update the product quantity
            order_item: OrderItem = self.create_order_item(
                order, product, quantity, price)

            # Update order total amount
            order.total_amount += price * quantity
            order.save()

            return order_item


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


class CartSerializer(serializers.Serializer):
    items = OrderItemSerializer(many=True, source='order_items')
    subtotal = serializers.DecimalField(max_digits=10, decimal_places=2)
    tax = serializers.DecimalField(max_digits=10, decimal_places=2)
    discount = serializers.DecimalField(max_digits=10, decimal_places=2)
    total_amount = serializers.DecimalField(
        max_digits=100000, decimal_places=2)
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
        items = [OrderItemSerializer(
            item).data for item in instance.get_items()]
        return {
            'subtotal': instance.get_subtotal(),
            'discount': instance.get_discount(),
            'tax': instance.get_tax(),
            'total_price': instance.get_total_price(tax_rate=Decimal(0.5)),
            'coupon': self.get_coupon(instance),
            'items': items,
            "total_items_quantity": instance.__len__()
        }
