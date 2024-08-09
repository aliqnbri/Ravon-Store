from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from rest_framework import filters, viewsets, permissions ,status
from rest_framework.response import Response
from rest_framework.decorators import action

from account.authentications import CustomJWTAuthentication
from order.models import Order, Coupon, OrderItem
from order.serializers import (
    OrderSerializer, 
    CouponSerializer, 
    CreateOrderSerializer, 
    OrderItemSerializer
)

# Create your views here.

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


class CouponViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAdminUser]
    authentication_classes = [CustomJWTAuthentication]
    queryset = Coupon.objects.all()
    serializer_class = CouponSerializer
























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
    
