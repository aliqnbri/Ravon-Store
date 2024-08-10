from django.urls import path, include
from rest_framework import routers
from order import views

from rest_framework.routers import DefaultRouter

app_name = 'order'

router = DefaultRouter()
router.register(r'orders', views.OrderViewSet, basename='order')

urlpatterns = [
    path('', include(router.urls)),
    
]
