from django.urls import path,include
from rest_framework.routers import DefaultRouter
from product import views

app_name= 'product'


router = DefaultRouter()
router.register(r'products', views.ProductViewSet, basename='product')
router.register(r'categories', views.CategoryViewSet, basename='category')

urlpatterns = [
    path('', include(router.urls)),
]

# urlpatterns = [
#     path('product_list/',views.ProductMixinView.as_view(), name='product_list'),
#     path('detail/<str:slug>/',views.ProductMixinView.as_view(), name='product_detail'),
#     path('update/<str:slug>/',views.ProductMixinView.as_view(), name='product_update'),
#     path('destroy/<str:slug>/',views.ProductMixinView.as_view(), name='product_destroy'),
#     path('create/<str:slug>/',views.ProductMixinView.as_view(), name='product_create'),
#     path('categoty/<str:category_slug>/',views.ProductMixinView.as_view(), name='category_filter'),
# ]