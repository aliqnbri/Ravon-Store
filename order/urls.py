from django.urls import path, include
from rest_framework import routers
from order.views import OrderViewSet , CouponViewSet ,ConformationTemplateView

router = routers.DefaultRouter()
router.register(r'order',OrderViewSet)
router.register(r'coupon',CouponViewSet)

app_name = 'orders'


urlpatterns =[
    path('api/',include(router.urls)),
   path('conformation',ConformationTemplateView.as_view(),name ='conform')
]