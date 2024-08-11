

from rest_framework import filters, viewsets, permissions, status
from rest_framework.response import Response


from account.authentications import CustomJWTAuthentication
from order.models import Order
from order.serializers import OrderSerializer


class OrderViewSet(viewsets.ModelViewSet):

    serializer_class = OrderSerializer
    permission_classes = [permissions.AllowAny]
    authentication_classes = [CustomJWTAuthentication]
    filter_backends = [filters.SearchFilter]
    search_fields = ['customer__username', 'customer__email']
    queryset = Order.objects.all().select_related(
        'customer').prefetch_related('items')
    
    
    # def get_queryset(self):
    #     user = self.request.user
    #     if user.is_staff or user.is_superuser:
    #         return Order.objects.all().select_related('customer').prefetch_related('items')
    #     else:
    #         return Order.objects.filter(customer=user.customer_profile).select_related('customer').prefetch_related('items')
