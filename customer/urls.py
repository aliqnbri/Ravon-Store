from django.urls import path ,re_path,include
from rest_framework.routers import DefaultRouter
from customer import views


router = DefaultRouter()
router.register(r'addresses',views.AddressAPIViewSet)
router.register(r'wishes',views.WishListAPIViewSet)
app_name = 'customer'
urlpatterns = [
    path('api/',include(router.urls)),
    path('',views.ProfileTemplateView.as_view(),name='profile'),
    path('orders',views.OrdersTemplateView.as_view(),name='orders'),
    path('addresses',views.AddressTemplateView.as_view(),name='address')

]