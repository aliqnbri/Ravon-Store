from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.views.generic import TemplateView

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from cart.models import Cart

# Create your views here.

class CartTemplateView(TemplateView):
    template_name = "cart.html"


class CheckOutTemplateView(TemplateView):
    template_name = "checkout.html"
    
    def dispatch(self, request, *args, **kwargs):
        if request.COOKIES.get('access_token') != None:
            
            return super().dispatch(request, *args, **kwargs)
        else :
            return redirect(reverse_lazy('login'))
    
    
class CartAPI(APIView):
    """
    Single API to handle cart operations
    """
    def get(self, request, format=None):
        cart = Cart(request)

        return Response(
            {"data": list(cart.__iter__()), 
            "count":cart.__len__(),
            "cart_total_price": cart.get_total_price()},
            status=status.HTTP_200_OK
            )

    def post(self, request, **kwargs):
        cart = Cart(request)
        action = request.data.get('action')

        match action:
            case 'remove':
                cart.remove(request.data["product"])
            case 'clear':
                cart.clear()
            case 'add':
                product = request.data
                cart.add(
                    product=product["product"],
                    quantity=product["quantity"],
                    overide_quantity=product.get("overide_quantity", False)
                )

        return Response(
            {"message": "cart updated"},
            status=status.HTTP_202_ACCEPTED)