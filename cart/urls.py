from cart import views
from django.urls import path, include
from rest_framework import routers
from rest_framework.routers import DefaultRouter
router = DefaultRouter()
router.register(r'cart', views.CartViewSet, basename='cart')
router.register(r'order-items', views.OrderItemViewSet, basename='order-items')

app_name = 'cart'
urlpatterns = [
    path('', include(router.urls)),
    path('carts/',views.CartTemplateView.as_view(),name= 'cart'),
    path('checkout/',views.CheckOutTemplateView.as_view(),name="checkout")



]
