from cart.serializers import CartSerializer, CartItemSerializer
from rest_framework import viewsets, status
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from rest_framework import filters, viewsets, permissions, status
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

# Create your views here.
# class OrderViewSet(viewsets.ModelViewSet):
#     queryset = Order.objects.all()
#     serializer_class = OrderSerializer
#     permission_classes = [permissions.AllowAny]
#     authentication_classes = [CustomJWTAuthentication]

#     def create(self, request, *args, **kwargs):
#         cart = Cart(request)
#         order = Order.objects.create(user=request.user, total=cart.get_total_price())
#         for item in cart.items.all():
#             OrderItem.objects.create(order=order, product=item.product, quantity=item.quantity)
#         cart.clear()
#         serializer = OrderSerializer(order)
#         return Response(serializer.data, status=status.HTTP_201_CREATED)

#     def list(self, request, *args, **kwargs):
#         orders = Order.objects.filter(user=request.user)
#         serializer = OrderSerializer(orders, many=True)
#         return Response(serializer.data)

#     def retrieve(self, request, *args, **kwargs):
#         order = Order.objects.get(id=kwargs.get('pk'))
#         serializer = OrderSerializer(order)
#         return Response(serializer.data)


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
        if self.action in ['create', 'update', 'partial_update']:
            return CreateOrderSerializer
        return OrderSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        order = serializer.save()
        print(order, 'this is order in orderviewset')
        return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        customer = request.user.customer_profile
        if instance.customer != customer:
            return Response("You are not authorized to view this order.", status=status.HTTP_403_FORBIDDEN)
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        return Response("Orders cannot be updated.", status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def destroy(self, request, *args, **kwargs):
        return Response("Orders cannot be deleted.", status=status.HTTP_405_METHOD_NOT_ALLOWED)


class OrderItemViewSet(viewsets.ModelViewSet):
    queryset = OrderItem.objects.all().select_related('order', 'product')
    serializer_class = OrderSerializer
    permission_classes = [permissions.AllowAny]
    authentication_classes = [CustomJWTAuthentication,]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(
            data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        order_item = serializer.save()
        response_serializer = OrderItemSerializer(order_item)
        headers = self.get_success_headers(response_serializer.data)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(
            instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.db import transaction
from typing import Optional
from decimal import Decimal
from product.models import Product
from cart.models import Cart
from cart.serializers import CartSerializer

class CartViewSet(viewsets.ViewSet):

    serializer_class = CartSerializer
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


# class ConformationTemplateView(TemplateView):
#     template_name = 'conformorder.html'
#     def dispatch(self, request, *args, **kwargs):
#         # print(request.user)
#         if request.COOKIES.get('username') != None:

#             return super().dispatch(request, *args, **kwargs)
#         else :
#             return redirect(reverse_lazy('login'))


# class OrderViewSet(viewsets.ModelViewSet):
#     permission_classes = [permissions.IsAuthenticated]
#     authentication_classes = [CustomJWTAuthentication]
#     queryset = Order.objects.all()
#     serializer_class = OrderSerializer
#     filterset_fields = ['payment_id']

#     def create(self, request, *args, **kwargs):
#         serializer = CreateOrderSerializer(data=request.data, context={ "request":request})
#         serializer.is_valid(raise_exception=True)
#         order = serializer.save()
#         serializer = OrderSerializer(order)
#         return Response(serializer.data)

#     def get_queryset(self):
#         user = self.request.user
#         if user.is_staff:
#             return Order.objects.all()
#         return Order.objects.filter(customer=user)
