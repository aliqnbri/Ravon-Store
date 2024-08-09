from django.db import transaction
from rest_framework import serializers
from order.models import Order, Coupon, OrderItem

from customer.models import Address
from cart.models import Cart

from product.serializers import ProductSerializer
from product.models import Product


class OrderItemSerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all(),
                                                 read_only=False,
                                                 allow_null=False,
                                                 required=True)
    quantity = serializers.ChoiceField(
        choices=[(i, i) for i in range(1, 100)],  # adjust the range as needed
        required=True)
    
    total_price = serializers.SerializerMethodField()
    price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)


    def get_total_price(self, obj):
        return obj.total_price()

    class Meta:
        model = OrderItem
        fields = ["id", "product", "price", "quantity", "total_price"]
        depth = 1

    def validate(self, data):
        product = data['product']
        quantity = data['quantity']
        if product.available_quantity < quantity:
            raise serializers.ValidationError(
                f"Insufficient quantity for product {product.name}"    )
        return data
    
    def create(self, validated_data):
        product = validated_data['product']
        quantity = validated_data['quantity']
        product.available_quantity -= quantity
        product.save()
        return super().create(validated_data)

class OrderSerializer(serializers.ModelSerializer):
    customer = serializers.StringRelatedField()
    items = OrderItemSerializer(many=True,source='order_items')
    modified_at = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ["id", "customer", "items", "status", "coupon", "discount", "modified_at",
                  "total_amount", ]
        read_only_fields = ['items', 'customer', 'created_at', 'modified_at']

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
            order_item = OrderItem.objects.filter(id=item_data['id'], order=instance).first()
            if order_item:
                order_item.quantity = item_data.get('quantity', order_item.quantity)
                order_item.price = item_data.get('price', order_item.price)
                order_item.save()
            else:
                OrderItem.objects.create(order=instance, **item_data)
        return instance        

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




from typing import Any, Dict
from django.db import transaction
from rest_framework import serializers
from django.core.exceptions import ValidationError


class CreateOrderSerializer(serializers.Serializer):
    # products = serializers.ListField(
    #     child=serializers.DictField(),  # Expecting a list of dictionaries with product 'id' and 'quantity'.
    #     allow_empty=False)
    # products = ProductOrderSerializer(many=True)  # Expecting a list of product IDs and quantities
    products = serializers.PrimaryKeyRelatedField(many=True, read_only=False, queryset=Product.objects.all())
    coupon_code = serializers.CharField(required=False, allow_blank=True)



    def validate_products(self, products):
        for product in products:
            if product.available_quantity <1:
                raise serializers.ValidationError(
                    f"Insufficient quantity for product {product.name}"
                )
        return products

    def validate(self, data: Dict[str, Any]) -> Dict[str, Any]:
        products = data.get("products", [])
        self.validate_products(products)
        return data

    def create_order_items(self, order: Order, products: list, coupon: Coupon = None) -> None:
        order_items = []
        total_price = 0
        coupon = None

        for product_data in products:
            # product = Product.objects.select_for_update().get(id=product_data['id'])
            quantity = 1
            price = product_data.price
            
           
            if coupon:
                discounted_price = coupon.calculate_discounted_price()
                price = min(price, discounted_price)  # Ensuring we get the lower price if the coupon applies

            order_item = OrderItem(order=order, product=product_data, quantity=quantity, price=price)
            order_items.append(order_item)
            total_price += price * quantity
            
            # Update product's available quantity
            product_data.available_quantity -= quantity
            product_data.save()

        OrderItem.objects.bulk_create(order_items)
        order.total_amount = total_price
        order.save()

    def create(self, validated_data: Dict[str, Any]) -> Order:
        request = self.context.get('request')
        products = validated_data.pop('products')
        coupon_code = validated_data.get("coupon_code", None)
        customer = request.user.customer_profile
        print(customer, 'this is the customer')
        address = customer.address

        
        with transaction.atomic():
            coupon = None
            if coupon_code:
                coupon = Coupon.objects.filter(code=coupon_code, is_active=True).first()
                if not coupon:
                    raise ValidationError("Invalid coupon code provided.")
            order = Order.objects.create(customer=customer)
            self.create_order_items(order, products, coupon_code)
            return order




    # def save(self, **kwargs) -> Order:
    #     with transaction.atomic():
    #         request = self.context.get("request")
    #         # address = Address.objects.filter(id=request.data['address']).first()

    #         # if not address:
    #         #     raise ValidationError("Invalid address")
    #         print(request, 'this is request in create order')
    #         customer = request.user.customer_profile
    #         address = customer.address

    #         order = Order.objects.create(
    #             customer=customer,
    #             city=address.city,
    #             postal_code=address.postal_code,
    #             address=address.get_address(),
    #         )

    #         cart = Cart(request)
    #         products = [{'product': Product.objects.get(id=item['product']['id']), 'quantity': item['quantity'], 'price': item['price']} for item in cart]

    #         self.validate_products([product['product'] for product in products])

    #         order_items = [
    #             OrderItem(
    #                 order=order,
    #                 product=product['product'],
    #                 quantity=product['quantity'],
    #                 price=product['price']
    #             )
    #             for product in products
    #         ]
    #         OrderItem.objects.bulk_create(order_items)

    #         for item in cart:
    #             product = Product.objects.get(id=item['product']['id'])
    #             product.reduce_quantity(item['quantity'])

    #         cart.clear()
    #         return order


# class CreateOrderSerializer(serializers.Serializer):
#     products = serializers.PrimaryKeyRelatedField(many=True, read_only=False, queryset=Product.objects.all())
#     coupon_code = serializers.CharField(required=False)


#     def validate(self, data):
#         products = data["products"]
#         for product_data in products:
#             product_id = product_data["id"]
#             quantity = product_data["quantity"]
#             product = Product.objects.get(id=product_id)
#             if product.available_quantity < quantity:
#                 raise serializers.ValidationError(
#                     f"Insufficient quantity for product {product.name}"
#                 )
#         return data
    

#     def create(self, validated_data):
#         # products = validated_data["products"]
#         products = validated_data.pop('products')

#         coupon_code = validated_data.get("coupon_code")
#         order = Order.objects.create(customer=self.context["request"].user)
#         order_items = []
#         total_price = 0
#         for product_data in products:
#             product_id = product_data["id"]
#             quantity = product_data["quantity"]
#             product = Product.objects.get(id=product_id)
#             price = product.price
#             if coupon_code:
#                 coupon = Coupon.objects.get(code=coupon_code)
#                 if coupon.is_active:
#                     discount_percentage = coupon.discount_percentage
#                     price -= (price * discount_percentage) / 100
#             order_item = OrderItem(order=order, product=product, quantity=quantity, price=price)
#             order_items.append(order_item)
#             total_price += price * quantity
#         OrderItem.objects.bulk_create(order_items)
#         order.total_price = total_price
#         order.save()
#         return order

#     def save(self, **kwargs):
#         with transaction.atomic():
#             request = self.context.get("request")
#             address = Address.objects.filter(
#                 id=request.data['address']).first()

#             order = Order.objects.create(customer=request.user,
#                                          city=request.user.address.city,
#                                          postal_code=request.user.address.postal_code,
#                                          address=request.user.address.detail,
#                                          )
#             cart = Cart(request)
#             for item in cart:
#                 product = Product.objects.get(id=item['product']['id'])
#                 if product.available_quantity < item['quantity']:
#                     raise serializers.ValidationError(
#                         f"Insufficient quantity for product {product.name}"
#                     )
#             orderitems = [
#                 OrderItem(order=order,
#                           product=Product.objects.get(
#                               id=item['product']['id']),
#                           quantity=item['quantity'],
#                           price=item['price']
#                           )
#                 for item in cart
#             ]
#             OrderItem.objects.bulk_create(orderitems)
#             product.reduce_quantity(item['quantity'])
#             cart.clear()
#             return order



# class CreateOrderSerializer(serializers.Serializer):
#     products = serializers.ListField(child=serializers.DictField())
#     coupon_code = serializers.CharField(required=False)

#     def validate(self, data):
#         products = data["products"]
#         for product_data in products:
#             product_id = product_data["id"]
#             quantity = product_data["quantity"]
#             product = Product.objects.get(id=product_id)
#             if product.available_quantity < quantity:
#                 raise serializers.ValidationError(
#                     f"Insufficient quantity for product {product.name}"
#                 )
#         return data

#     def create(self, validated_data):
#         products = validated_data["products"]
#         coupon_code = validated_data.get("coupon_code")
#         order = Order.objects.create(customer=self.context["request"].user)
#         order_items = []
#         total_price = 0
#         for product_data in products:
#             product_id = product_data["id"]
#             quantity = product_data["quantity"]
#             product = Product.objects.get(id=product_id)
#             price = product.price
#             if coupon_code:
#                 coupon = Coupon.objects.get(code=coupon_code)
#                 if coupon.is_active:
#                     discount_percentage = coupon.discount_percentage
#                     price -= (price * discount_percentage) / 100
#             order_item = OrderItem(order=order, product=product, quantity=quantity, price=price)
#             order_items.append(order_item)
#             total_price += price * quantity
#         OrderItem.objects.bulk_create(order_items)
#         order.total_price = total_price
#         order.save()
#         return order

