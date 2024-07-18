from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from decimal import Decimal
from django.conf import settings
from product.models import Product
from order.models import Coupon

class CartView(APIView):
    def __init__(self):
        self.cart_session_id = settings.CART_SESSION_ID

    def get_cart(self, request):
        cart = request.session.get(self.cart_session_id)
        if not cart:
            cart = {}
        return cart

    def get_coupon(self, request):
        coupon_id = request.session.get('coupon_id')
        if coupon_id:
            try:
                return Coupon.objects.get(id=coupon_id)
            except Coupon.DoesNotExist:
                pass
        return None

    def add_to_cart(self, request, product_id, quantity=1, override_quantity=False):
        cart = self.get_cart(request)
        product = Product.objects.get(id=product_id)
        product_id = str(product.id)
        if product_id not in cart:
            cart[product_id] = {'quantity': 0, 'price': str(product.price)}
        if override_quantity:
            cart[product_id]['quantity'] = quantity
        else:
            cart[product_id]['quantity'] += quantity
        request.session[self.cart_session_id] = cart
        request.session.modified = True
        return Response(status=status.HTTP_201_CREATED)

    def remove_from_cart(self, request, product_id):
        cart = self.get_cart(request)
        product_id = str(product_id)
        if product_id in cart:
            del cart[product_id]
            request.session[self.cart_session_id] = cart
            request.session.modified = True
        return Response(status=status.HTTP_204_NO_CONTENT)

    def clear_cart(self, request):
        del request.session[self.cart_session_id]
        request.session.modified = True
        return Response(status=status.HTTP_204_NO_CONTENT)

    def get_cart_total(self, request):
        cart = self.get_cart(request)
        total_price = sum(Decimal(item['price']) * item['quantity'] for item in cart.values())
        return Response({'total_price': total_price})

    def get_cart_total_after_discount(self, request):
        cart = self.get_cart(request)
        total_price = sum(Decimal(item['price']) * item['quantity'] for item in cart.values())
        coupon = self.get_coupon(request)
        if coupon:
            discount = (coupon.discount / Decimal(100)) * total_price
            total_price_after_discount = total_price - discount
        else:
            total_price_after_discount = total_price
        return Response({'total_price_after_discount': total_price_after_discount})

    def get(self, request):
        cart = self.get_cart(request)
        products = Product.objects.filter(id__in=cart.keys())
        cart_items = []
        for product in products:
            cart_item = cart[str(product.id)]
            cart_item['product'] = product
            cart_item['price'] = Decimal(cart_item['price'])
            cart_item['total_price'] = cart_item['price'] * cart_item['quantity']
            cart_items.append(cart_item)
        return Response(cart_items)

    def post(self, request):
        product_id = request.data.get('product_id')
        quantity = request.data.get('quantity', 1)
        override_quantity = request.data.get('override_quantity', False)
        return self.add_to_cart(request, product_id, quantity, override_quantity)

    def delete(self, request, product_id):
        return self.remove_from_cart(request, product_id)