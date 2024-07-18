from django.shortcuts import render ,redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from rest_framework import filters ,viewsets , permissions

from account.authentications import CustomJWTAuthentication
from rest_framework.response import Response
from order.models import Order , Coupon
from order.serializers import OrderSerializer , CouponSerializer , CreateOrderSerializer,UpdateOrderSerializer
# Create your views here.

class ConformationTemplateView(TemplateView):
    template_name = 'conformorder.html'
    def dispatch(self, request, *args, **kwargs):
        # print(request.user)
        if request.COOKIES.get('username') != None:
            
            return super().dispatch(request, *args, **kwargs)
        else :
            return redirect(reverse_lazy('login'))


class OrderViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [CustomJWTAuthentication]
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    filterset_fields = ['payment_id']
    
    def create(self, request, *args, **kwargs):
        serializer = CreateOrderSerializer(data=request.data, context={ "request":request})
        serializer.is_valid(raise_exception=True)
        order = serializer.save()
        serializer = OrderSerializer(order)
        return Response(serializer.data)
    
    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Order.objects.all()
        return Order.objects.filter(customer=user)
    
class CouponViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAdminUser]
    authentication_classes = [CustomJWTAuthentication]
    queryset = Coupon.objects.all()
    serializer_class = CouponSerializer