from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from rest_framework import filters, viewsets, permissions
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
    queryset = Order.objects.all().select_related('user').prefetch_related('order_items')
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [CustomJWTAuthentication]

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return CreateOrderSerializer
        return OrderSerializer

class OrderItemViewSet(viewsets.ModelViewSet):
    queryset = OrderItem.objects.all().select_related('order', 'product')
    serializer_class = OrderItemSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [CustomJWTAuthentication,]

# Create your views here.
























# class OrderListCreateView(generics.ListCreateAPIView):
#     queryset = Order.objects.all()
#     serializer_class = OrderSerializer

# class OrderRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Order.objects.all()
#     serializer_class = OrderSerializer

# class OrderItemListCreateView(generics.ListCreateAPIView):
#     queryset = OrderItem.objects.all()
#     serializer_class = OrderItemSerializer

# class OrderItemRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
#     queryset = OrderItem.objects.all()
#     serializer_class = OrderItemSerializer

























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
    
# class CouponViewSet(viewsets.ViewSet):
#     permission_classes = [permissions.IsAdminUser]
#     authentication_classes = [CustomJWTAuthentication]
#     queryset = Coupon.objects.all()
#     serializer_class = CouponSerializer