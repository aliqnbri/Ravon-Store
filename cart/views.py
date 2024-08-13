
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
from typing import Optional, Any, LiteralString



class CartViewSet(viewsets.ViewSet):

    serializer_class = CreateOrderItemSerializer
    permission_classes = [permissions.AllowAny]
    authentication_classes = [CustomJWTAuthentication]
    lookup_field = 'slug'

    def list(self, request: Any) -> Response:
        """
        Display the current items in the cart, along with the total price and total items.
        """
        cart = Cart(request)
        serializer = CartSerializer(cart)
        return Response(serializer.data)

    @transaction.atomic
    def create(self, request: Any, *args: Any, **kwargs: Any) -> Response:
        """
        Add a product to the cart or update its quantity.
        """
        product_slug: Optional[str] = request.data.get('product')

        quantity: int = int(request.data.get('quantity', 1))

        if not product_slug:
            return Response({"error": "Product slug is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        

        product = self._get_product_by_slug(product_slug)


        if product.available_quantity < quantity:
            return Response({"error": "Insufficient product quantity available"}, status=status.HTTP_400_BAD_REQUEST)
        
    

        cart = Cart(request)
        cart.add(product=product, quantity=quantity)

        serializer = CartSerializer(cart)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @transaction.atomic
    def update(self, request, slug: Optional[str] = None) -> Response:
        """
        Update the quantity of a product in the cart.
        """
        product_slug: Optional[LiteralString] = request.query_params.get('slug')

        quantity: int = int(request.data.get('quantity', 1))

        product = self._get_product_by_slug(product_slug)


        if product.available_quantity < quantity:
            return Response({"error": "Insufficient product quantity available"}, status=status.HTTP_400_BAD_REQUEST)

        cart = Cart(request)
        if cart.has_product(product=product):
            cart.update(old_product=product, new_product=None, quantity=quantity)
        else:    
            cart.update(old_product=None, new_product=product, quantity=quantity)
        serializer = CartSerializer(cart)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @transaction.atomic
    def destroy(self, request, slug: Optional[LiteralString] = None) -> Response:
        """
        Remove a product from the cart.
        """
        product_slug: Optional[LiteralString] = request.query_params.get('slug')
        product = self._get_product_by_slug(product_slug)

        cart = Cart(request)
        cart.remove(product)
        serializer = CartSerializer(cart)
        return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)

    
    def _get_product_by_slug(self, slug: LiteralString) -> Product:
        """
        Retrieve a product by its slug, ensuring that it exists.
        """
        return get_object_or_404(Product, slug=slug)


class OrderItemViewSet(viewsets.ViewSet):
    """
    ViewSet to manage OrderItem operations like listing items, adding items, updating items, and removing items.
    """

    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [CustomJWTAuthentication]

    def get_order(self):
        """
        Retrieve or create the current user's pending order.
        """
        request = self.request
        order = Order.objects.get_or_create(
            customer=request.user.customer_profile,
            status=Order.OrderStatus.PENDING,
            defaults={'total_amount': Decimal(0)}
        )
        return order

    def list(self, request: Any, *args: Any, **kwargs: Any) -> Response:
        """
        List all items in the user's current order.
        """
        order = Order.objects.get(customer=request.user.customer_profile)
        serializer = CreateOrderItemSerializer(order.order_items.all(), many=True)
        return Response(serializer.data)
    

    @action(detail=False, methods=['post'])
    def add(self, request: Any, *args: Any, **kwargs: Any) -> Response:
        """
        Add an item to the user's current order.
        """
        order = self.get_order()
        serializer = CreateOrderItemSerializer(data=request.data, context={'order': order})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request: Any, pk: Optional[int] = None) -> Response:
        """
        Update an existing order item.
        """
        order_item = get_object_or_404(OrderItem, pk=pk)
        serializer = CreateOrderItemSerializer(order_item, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.update(order_item, serializer.validated_data)
        return Response(serializer.data)

    @action(detail=True, methods=['delete'])
    def remove(self, request: Any, pk: Optional[int] = None) -> Response:
        """
        Remove an item from the user's current order.
        """
        order_item = get_object_or_404(OrderItem, pk=pk)
        order_item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)