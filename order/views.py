
from decimal import Decimal
from typing import Optional
from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from cart.serializers import CartSerializer

from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from rest_framework import filters, viewsets, permissions ,status
from rest_framework.response import Response
from rest_framework.decorators import action
from cart.models import Cart
from product.models import Product
from account.authentications import CustomJWTAuthentication
from order.models import Order, Coupon, OrderItem
from order.serializers import (
    OrderSerializer,
    CreateOrderSerializer,
    OrderItemSerializer
)


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all().select_related(
        'customer').prefetch_related('items')
    serializer_class = OrderSerializer
    permission_classes = [permissions.AllowAny]
    authentication_classes = [CustomJWTAuthentication]
    filter_backends = [filters.SearchFilter]
    search_fields = ['customer__username', 'customer__email']

    def get_queryset(self):
        user = self.request.user
        if user.is_staff or user.is_superuser:
            return Order.objects.all()
        return self.queryset

    def get_serializer_class(self):
        if self.action in ['create', 'update']:
            return CreateOrderSerializer
        return OrderSerializer
 
    @transaction.atomic
    def create(self, request, *args, **kwargs):
        serializer = CreateOrderSerializer(data=request.data, context={ "request":request})
        serializer.is_valid(raise_exception=True)
        order = serializer.save()
        serializer = OrderSerializer(order)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    


    @transaction.atomic
    def update(self, request, *args, **kwargs) -> Response:
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        order = serializer.save()

        # Update the order's total cost after modifying it
        order.total_amount = order.get_total_cost()
        order.save()

        return Response(OrderSerializer(order).data)

    def destroy(self, request, *args, **kwargs) -> Response:
        return Response("Orders cannot be deleted.", status=status.HTTP_405_METHOD_NOT_ALLOWED)


class CartViewSet(viewsets.ViewSet):

    serializer_class = CreateOrderSerializer
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
        product_slug: Optional[str] = request.data.get('product')
        
        quantity: int = int(request.data.get('quantity', 1))

        if not product_slug:
            return Response({"error": "Product slug is required"}, status=status.HTTP_400_BAD_REQUEST)

        product = get_object_or_404(Product, slug=product_slug)

        if product.available_quantity < quantity:
            return Response({"error": "Insufficient product quantity available"}, status=status.HTTP_400_BAD_REQUEST)

        cart = Cart(request)
        cart.add(product=product, quantity=quantity)
        serializer = CartSerializer(cart)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @transaction.atomic
    def update(self, request, pk: Optional[int] = None) -> Response:
        """
        Update the quantity of a product in the cart.
        """
        quantity: int = int(request.data.get('quantity', 1))

        product = get_object_or_404(Product, id=pk)

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
        product = get_object_or_404(Product, id=pk)
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
