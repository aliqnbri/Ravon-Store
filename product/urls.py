from django.urls import path,include
from rest_framework.routers import DefaultRouter
from product import views

app_name = 'product'



router = DefaultRouter()
router.register(r'products', views.ProductViewSet, basename='products')
router.register(r'category',views.CategoryViewSet)
router.register(r'brand',views.BrandViewSet)


urlpatterns = [
     path('',views.ProductTemplateView.as_view(),name='product-list'),
    path('detail/<str:slug>',views.ProductDetailTemplateView.as_view(),name='productdetail'),

    path('api/', include(router.urls)),
]
