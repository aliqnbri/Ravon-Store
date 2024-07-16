from django.urls import path

from product import views

app_name= 'product'

urlpatterns = [
    path('list/',views.ProductMixinView.as_view(), name='product_list'),
    path('detail/<str:slug>/',views.ProductMixinView.as_view(), name='product_detail'),
    path('update/<str:slug>/',views.ProductMixinView.as_view(), name='product_update'),
    path('destroy/<str:slug>/',views.ProductMixinView.as_view(), name='product_destroy'),
    path('create/<str:slug>/',views.ProductMixinView.as_view(), name='product_create'),
]