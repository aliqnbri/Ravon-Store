from cart import views
from django.urls import path, include
from rest_framework import routers
from rest_framework.routers import DefaultRouter
router = DefaultRouter()
router.register(r'cart', views.CartViewSet, basename='cart')
app_name = 'cart'

urlpatterns = [
    path('', include(router.urls)),



]
