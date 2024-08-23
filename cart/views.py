
from cart.serializers import CreateOrderItemSerializer, CartSerializer
from order.models import OrderItem, Order
from rest_framework import viewsets, permissions, status
from decimal import Decimal
from rest_framework.response import Response
from typing import Optional
from cart.models import Cart
from django.shortcuts import get_object_or_404
from django.db import transaction
from rest_framework.decorators import action
from account.authentications import CustomJWTAuthentication
from product.models import Product
from django.views.generic import TemplateView

from django.urls import reverse_lazy
from django.shortcuts import redirect

class CartTemplateView(TemplateView):
    template_name = "cart/cart.html"


class CheckOutTemplateView(TemplateView):
    template_name = "cart/checkout.html"
    
    def dispatch(self, request, *args, **kwargs):
        if request.COOKIES.get('username') != None:
            
            return super().dispatch(request, *args, **kwargs)
        else :
            return redirect(reverse_lazy('login'))


class CartViewSet(viewsets.ViewSet):

    serializer_class = CreateOrderItemSerializer
    permission_classes = [permissions.AllowAny]
    authentication_classes = [CustomJWTAuthentication]
    lookup_field = 'slug'

    def list(self, request):
        """
        Display the current items in the cart, along with the total price and total items.
        """
        cart = Cart(request)
        serializer = CartSerializer(cart)
        return Response(serializer.data)

    @transaction.atomic
    def create(self, request, *args, **kwargs) -> Response:
        """
        Add a product to the cart or update its quantity.
        """
        print(request.data , 'this is in create cart view')
        product_slug: Optional[str] = request.data.get('product')

        quantity: int = int(request.data.get('quantity', 1))

        if not product_slug:
            return Response({"error": "Product slug is required"}, status=status.HTTP_400_BAD_REQUEST)

        product = get_object_or_404(Product, slug=product_slug)

        if product.available_quantity < quantity:
            return Response({"error": "Insufficient product quantity available"}, status=status.HTTP_400_BAD_REQUEST)

        cart = Cart(request)

        print(cart, 'this is cart in the cartviewset')
        cart.add(product=product, quantity=quantity)
        serializer = CartSerializer(cart)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @transaction.atomic
    def update(self, request, pk: Optional[int] = None) -> Response:
        """
        Update the quantity of a product in the cart.
        """
        product_slug = request.query_params.get('slug')

        quantity: int = int(request.data.get('quantity', 1))

        product = get_object_or_404(Product, slug=product_slug)

        if product.available_quantity < quantity:
            return Response({"error": "Insufficient product quantity available"}, status=status.HTTP_400_BAD_REQUEST)

        cart = Cart(request)
        cart.add(product=product, quantity=quantity, overide_quantity=True)
        serializer = CartSerializer(cart)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @transaction.atomic
    def destroy(self, request, pk: Optional[int] = None) -> Response:
        """
        Remove a product from the cart.
        """
        product_slug = request.query_params.get('slug')
        product = get_object_or_404(Product, slug=product_slug)
        cart = Cart(request)
        cart.remove(product)
        serializer = CartSerializer(cart)
        return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['get'])
    def get_total(self, request) -> Response:
        """
        Get the total price and total number of items in the cart.
        """
        cart = Cart(request)
        total_price: Decimal = cart.get_total_price()
        total_items: int = len(cart)
        return Response({'total_price': total_price, 'total_items': total_items}, status=status.HTTP_200_OK)


class OrderItemViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def get_order(self):
        # Retrieve or create the current user's pending order
        request = self.request
        order, created = Order.objects.get_or_create(
            customer=request.user.customer_profile,
            status=Order.OrderStatus.PENDING,
            defaults={'total_amount': Decimal(0)}
        )
        return order

    def list(self, request, *args, **kwargs):
        order = self.get_order()
        serializer = CreateOrderItemSerializer(order.items.all(), many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['post'])
    def add(self, request, *args, **kwargs):
        order = self.get_order()
        serializer = CreateOrderItemSerializer(
            data=request.data, context={'order': order})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None):
        order_item = OrderItem.objects.get(pk=pk)
        serializer = CreateOrderItemSerializer(order_item, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.update(order_item, serializer.validated_data)
        return Response(serializer.data)

    @action(detail=True, methods=['delete'])
    def remove(self, request, pk=None):
        order_item = OrderItem.objects.get(pk=pk)
        serializer = CreateOrderItemSerializer()
        serializer.remove(order_item)
        return Response(status=status.HTTP_204_NO_CONTENT)
