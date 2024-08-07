from django.db import transaction
from rest_framework import serializers
from order.models import Order, Coupon, OrderItem

from customer.models import Address
from cart.models import Cart

from product.serializers import ProductSerializer
from product.models import Product

class SimpleProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'price']

class OrderItemSerializer(serializers.ModelSerializer):
    product = SimpleProductSerializer()

    class Meta:
        model = OrderItem
        fields = ["id", "product", "price", "quantity","total_price"]
        depth = 1


class OrderSerializer(serializers.ModelSerializer):
    customer = serializers.StringRelatedField()

    items = OrderItemSerializer(many=True)
    modified_at = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ["id", "customer", "items", "status", "coupon", "discount","modified_at",
                  "total_amount", "get_total_cost", "get_discount", "__len__"]
        read_only_fields = ['items', 'customer',
                            'get_total_cost', 'created_at', 'modified_at']

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


class CouponSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coupon
        fields = ['id', 'code', 'valid_from', 'valid_to', 'discount', 'is_active', 'count']


# incompite cart
class CreateOrderSerializer(serializers.Serializer):
    
    def save(self, **kwargs):
        with transaction.atomic():
            request = self.context.get("request")
            address = Address.objects.filter(id = request.data['address']).first()

            order = Order.objects.create(customer = request.user,
                                         city = request.user.address.city,
                                         postal_code = request.user.address.postal_code,
                                        address = request.user.address.detail,
                                         )
            cart = Cart(request)
            orderitems = [
                OrderItem(order=order, 
                    product=Product.objects.get(id = item['product']['id']), 
                    quantity=item['quantity'],
                    price = item['price']
                    )
            for item in cart
            ]
            OrderItem.objects.bulk_create(orderitems)
            cart.clear()
            return order
