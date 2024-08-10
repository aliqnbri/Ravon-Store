
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
        'customer').prefetch_related('order_items')
    serializer_class = OrderSerializer
    permission_classes = [permissions.AllowAny]
    authentication_classes = [CustomJWTAuthentication]
    filter_backends = [filters.SearchFilter]
    search_fields = ['customer__username', 'customer__email']
    lookup_field = 'slug'

    def get_serializer_class(self):
        if self.action in ['create', 'update']:
            return CreateOrderSerializer
        return OrderSerializer

    @transaction.atomic
    def create(self, request, *args, **kwargs) -> Response:
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        order = serializer.save()

        # Recalculate the total cost after creating the order
        order.total_amount = order.get_total_cost()
        order.save()

        return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)

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


class OrderItemViewSet(viewsets.ModelViewSet):
    queryset = OrderItem.objects.all().select_related('order', 'product')
    serializer_class = OrderSerializer
    permission_classes = [permissions.AllowAny]
    authentication_classes = [CustomJWTAuthentication,]

    @transaction.atomic
    def create(self, request, *args, **kwargs) -> Response:
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        order_item = serializer.save()

        # Update the order's total cost after adding an item
        order = order_item.order
        order.total_amount = order.get_total_cost()
        order.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @transaction.atomic
    def update(self, request, *args, **kwargs) -> Response:
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        order_item = serializer.save()

        # Update the order's total cost after modifying an item
        order = order_item.order
        order.total_amount = order.get_total_cost()
        order.save()

        return Response(serializer.data)

    @transaction.atomic
    def destroy(self, request, *args, **kwargs) -> Response:
        instance = self.get_object()
        order = instance.order
        self.perform_destroy(instance)

        # Update the order's total cost after removing an item
        order.total_amount = order.get_total_cost()
        order.save()

        return Response(status=status.HTTP_204_NO_CONTENT)


class CartViewSet(viewsets.ViewSet):

    serializer_class = CreateOrderSerializer
    permission_classes = [permissions.AllowAny]
    authentication_classes = [CustomJWTAuthentication]

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
        product_id: Optional[int] = request.data.get('product_id')
        quantity: int = int(request.data.get('quantity', 1))

        if not product_id:
            return Response({"error": "Product ID is required"}, status=status.HTTP_400_BAD_REQUEST)

        product = get_object_or_404(Product, id=product_id)

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
