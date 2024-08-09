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
    queryset = Order.objects.all().select_related('customer').prefetch_related('order_items')
    serializer_class = OrderSerializer
    permission_classes = [permissions.AllowAny]
    authentication_classes = [CustomJWTAuthentication]

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return CreateOrderSerializer
        return OrderSerializer
    
    def create(self, request, *args, **kwargs):

        serializer = self.get_serializer_class()(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        order = serializer.save()
        response_serializer = OrderSerializer(order)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)
    
    @action(detail=False, methods=['get'])
    def cart(self, request):
        cart = Cart(request)
        serializer = OrderSerializer(cart, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['post'])
    def add_to_cart(self, request):
        product_id = request.data.get('product_id')
        quantity = request.data.get('quantity')
        cart = Cart(request)
        product = Product.objects.get(id=product_id)
        cart.add(product=product, quantity=quantity)
        return Response({'message': 'Product added to cart'}, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['post'])
    def remove_from_cart(self, request):
        product_id = request.data.get('product_id')
        cart = Cart(request)
        product = Product.objects.get(id=product_id)
        cart.remove(product)
        return Response({'message': 'Product removed from cart'}, status=status.HTTP_200_OK)


class OrderItemViewSet(viewsets.ModelViewSet):
    queryset = OrderItem.objects.all().select_related('order', 'product')
    serializer_class = OrderItemSerializer
    permission_classes = [permissions.AllowAny]
    authentication_classes = [CustomJWTAuthentication,]

    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        order_item = serializer.save()
        response_serializer = OrderItemSerializer(order_item)
        headers = self.get_success_headers(response_serializer.data)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
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
from cart.models import Cart
from cart.serializers import CartSerializer, CartItemSerializer 

class CartViewSet(viewsets.ViewSet):

    serializer_class = CartSerializer
    permission_classes = [permissions.AllowAny]
    authentication_classes = [CustomJWTAuthentication]

    def list(self, request):
        cart = Cart(request)
        serializer = CartSerializer(cart)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        product_id = request.data.get('product_id')
        quantity = request.data.get('quantity')
        cart = Cart(request)
        product = Product.objects.get(id=product_id)
        cart.add(product=product, quantity=quantity)
        serializer = CartSerializer(cart)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        product_id = kwargs.get('pk')
        quantity = request.data.get('quantity')
        cart = Cart(request)
        product = Product.objects.get(id=product_id)
        cart.update(product=product, quantity=quantity)
        serializer = CartSerializer(cart)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        product_id = kwargs.get('pk')
        cart = Cart(request)
        product = Product.objects.get(id=product_id)
        cart.remove(product)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['get'])
    def get_total(self, request):
        cart = Cart(request)
        total = cart.get_total_price()
        return Response({'total': total}, status=status.HTTP_200_OK)


























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
    
