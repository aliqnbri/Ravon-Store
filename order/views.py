

from rest_framework import filters, viewsets, permissions, status
from rest_framework.response import Response


from account.authentications import CustomJWTAuthentication
from order.models import Order
from order.serializers import OrderSerializer ,CreateOrderSerializer


# class OrderViewSet(viewsets.ModelViewSet):

    # serializer_class = OrderSerializer
    # permission_classes = [permissions.AllowAny]
    # authentication_classes = [CustomJWTAuthentication]
    # filter_backends = [filters.SearchFilter]
    # search_fields = ['customer__username', 'customer__email']
    # queryset = Order.objects.all().select_related('customer').prefetch_related('order_items')


    
    # def get_queryset(self, ):
    #     user = self.request.user
      
    #     if user.is_staff or user.is_superuser:
    #         return Order.objects.all().select_related('customer').prefetch_related('order_items')
    #     else:
    #         return Order.objects.filter(customer=user.customer_profile).select_related('customer').prefetch_related('order_items')
        

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = CreateOrderSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        order = serializer.save()
        return Response(
            {"order_id": order.id, "status": "Order created successfully"},
            status=status.HTTP_201_CREATED
        )




