

# Create your views here.
from django.shortcuts import redirect ,get_object_or_404
from typing import Any
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from rest_framework import permissions,viewsets
# from django_filters.rest_framework import DjangoFilterBackend
from account.authentications import CustomJWTAuthentication
from customer.serializers import AddressSerializer,WishListItemSerializer ,CustomerProfileSerializer
from customer.models import Address , CustomerProfile
from product.models import WishListItem 
from order.models import Order
from rest_framework.response import Response
from account.utils import user_context_processor
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from account.permissions import IsAdmin , IsOwnerOrReadOnly , BaseIsAuthenticated

# Create your views here.

class AuthenticatedTemplateView(TemplateView):
    """
    A base template view class that checks for user authentication using cookies.
    Redirects to login if the user is not authenticated.
    """

    def dispatch(self, request, *args: Any, **kwargs: Any) -> Any:
        if request.COOKIES.get('access_token'):
            return super().dispatch(request, *args, **kwargs)
        return redirect(reverse_lazy('account:login'))

class BaseAPIViewSet(viewsets.ModelViewSet):
    """
    A base API viewset that sets the permission and authentication classes.
    This can be extended by other API viewsets.
    """
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [CustomJWTAuthentication]


class ProfileTemplateView(AuthenticatedTemplateView):
    template_name = "customer/profile.html"




class OrdersTemplateView(AuthenticatedTemplateView):
    template_name = "customer/orders.html"

class AddressTemplateView(AuthenticatedTemplateView):
    template_name = 'customer/address.html'


class AddressAPIViewSet(BaseAPIViewSet):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer
    
    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Address.objects.all()
        return Address.objects.filter(customer=user)
    
class WishListAPIViewSet(BaseAPIViewSet):
    queryset = WishListItem.objects.all()
    # filter_backends = [DjangoFilterBackend,filters.SearchFilter]
    serializer_class = WishListItemSerializer
    
    def get_queryset(self):
        user = self.request.user
        if user.role == user.Role.CUSTOMER:
            return WishListItem.objects.all()
        return WishListItem.objects.filter(customer=user)
    

class CustomerProfileViewSet(BaseAPIViewSet):
    serializer_class = CustomerProfileSerializer

    def get_permissions(self):
        """
        Return the appropriate permissions for each action.
        - If the action is 'list', only allow admins.
        - If the action is 'retrieve', allow the owner of the profile or admins.
        """
        if self.action == 'list':
            permission_classes = [IsAdmin]
        elif self.action == 'retrieve':
            permission_classes = [IsOwnerOrReadOnly]
        else:
            permission_classes = [BaseIsAuthenticated]  # default permission for other actions

        return [permission() for permission in permission_classes]

    def get_object(self)-> CustomerProfile:
        """Retrieve the customer profile for the logged-in user."""
        return get_object_or_404(CustomerProfile, customer=self.request.user)
    
    def get_queryset(self):
      
        return CustomerProfile.objects.all()

    def list(self, request) -> Response:
        """Retrieve the logged-in user's profile."""

        queryset = CustomerProfile.objects.all()
        profile = self.get_object()
        serializer = CustomerProfileSerializer(queryset , many=True)
        return Response(serializer.data)

    def update(self, request, *args: Any, **kwargs: Any) -> Response:
        """Update the logged-in user's profile."""
        profile = self.get_object()
        serializer = CustomerProfileSerializer(profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)
    

    # def retrieve(self, request, pk=None) -> Response:
    #     """Retrieve the logged-in user's profile."""

    #     # user = user_context_processor(request)['user']
    #     profile = self.get_object()
    #     serializer = CustomerProfileSerializer(profile)
    #     return Response(serializer.data)


    @action(detail=True, methods=['GET'])
    def addresses(self, request, pk=None) -> Response:
        """Retrieve the logged-in user's addresses."""
        profile = self.get_object()
        addresses = profile.addresses.all()
        serializer = AddressSerializer(addresses, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['PATCH'])
    def update_address(self, request, pk=None):
        """Update an address for the logged-in user."""
        profile = self.get_object()
        address = get_object_or_404(Address, pk=pk, customer_profile=profile)
        serializer = AddressSerializer(address, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    @action(detail=False, methods=['GET'])
    def orders(self, request):
        """Retrieve the logged-in user's orders - Read-only."""
        profile = self.get_object()
        orders = Order.objects.filter(customer=profile)
        order_data = [{"id": order.id, "status": order.status, "address": order.address} for order in orders]
        return Response(order_data)    