from cart import views
from django.urls import path


app_name = 'cart'


urlpatterns = [
    path('cart/', views.CartAPI.as_view()),
    path('cart-detail/', views.CartRetrieveUpdateDestroyView.as_view(), name='cart_detail'),
]

# urlpatterns = [
#     path('cart/', views.CartRetrieveUpdateDestroyView.as_view(), name='cart_detail'),
#     path('cart/add/<int:product_pk>/',
#          views.CartAddView.as_view(), name='cart_add'),
#     path('cart/remove/<int:product_pk>/',
#          views.CartRemoveView.as_view(), name='cart_remove'),
#     path('cart/clear/', views.CartClearView.as_view(), name='cart_clear'),
# ]
