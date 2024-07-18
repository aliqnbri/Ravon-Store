from django.urls import path
from cart.views import CartAPI ,CartTemplateView,CheckOutTemplateView

app_name= 'cart'

urlpatterns = [
    
    path('api/', CartAPI.as_view(), name='cartapi'),
    path('',CartTemplateView.as_view(),name= 'cart'),
    path('checkout/',CheckOutTemplateView.as_view(),name="checkout")
    
]