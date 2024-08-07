from django.urls import path, include
from rest_framework import routers
from order import views

from rest_framework.routers import DefaultRouter

app_name = 'order'

router = DefaultRouter()
router.register(r'orders', views.OrderViewSet, basename='order')
router.register(r'order-items', views.OrderItemViewSet, basename='orderitem')

urlpatterns = [
    path('', include(router.urls)),
]
#     path('orders/', views.OrderListCreateView.as_view(), name='order_list'),
#     path('orders/<int:pk>/', views.OrderRetrieveUpdateDestroyView.as_view(), name='order_detail'),
#     path('orders/<int:order_pk>/items/', views.OrderItemListCreateView.as_view(), name='order_item_list'),
#     path('orders/<int:order_pk>/items/<int:pk>/', views.OrderItemRetrieveUpdateDestroyView.as_view(), name='order_item_detail'),
# ]