
from decimal import Decimal
from rest_framework import status
from rest_framework.response import Response
from typing import Optional
from cart.models import Cart
from django.shortcuts import get_object_or_404
from django.db import transaction
from rest_framework import viewsets ,status ,permissions
from .models import Cart
from .serializers import CartSerializer 
from rest_framework.decorators import action
from order.serializers import CreateOrderSerializer
from account.authentications import CustomJWTAuthentication
from product.models import Product



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
