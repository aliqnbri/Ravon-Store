from django.shortcuts import render

# Create your views here.
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from rest_framework import permissions,filters,viewsets
# from django_filters.rest_framework import DjangoFilterBackend
from account.authentications import CustomJWTAuthentication
from customer.serializers import AddressSerializer,WishListItemSerializer
from customer.models import Address
from product.models import WishListItem
# Create your views here.

class ProfileTemplateView(TemplateView):
    template_name = "profile.html"

    def dispatch(self, request, *args, **kwargs):
        if request.COOKIES.get('username') != None:
            
            return super().dispatch(request, *args, **kwargs)
        else :
            return redirect(reverse_lazy('login'))


class OrdersTemplateView(TemplateView):
    template_name = "orders.html"
    def dispatch(self, request, *args, **kwargs):
        if request.COOKIES.get('username') != None:
            
            return super().dispatch(request, *args, **kwargs)
        else :
            return redirect(reverse_lazy('login'))

class AddressTemplateView(TemplateView):
    template_name = 'address.html'
    def dispatch(self, request, *args, **kwargs):
        if request.COOKIES.get('username') != None:
            
            return super().dispatch(request, *args, **kwargs)
        else :
            return redirect(reverse_lazy('login'))

class AddressAPIViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [CustomJWTAuthentication]
    queryset = Address.objects.all()
    # filter_backends = [DjangoFilterBackend,filters.SearchFilter]
    serializer_class = AddressSerializer
    
    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Address.objects.all()
        return Address.objects.filter(customer=user)
    
class WishListAPIViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [CustomJWTAuthentication]
    queryset = WishListItem.objects.all()
    # filter_backends = [DjangoFilterBackend,filters.SearchFilter]
    serializer_class = WishListItemSerializer
    
    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return WishListItem.objects.all()
        return WishListItem.objects.filter(customer=user)