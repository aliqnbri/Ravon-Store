
from django.contrib import admin
from django.urls import path, include
from debug_toolbar.toolbar import debug_toolbar_urls
from django.conf.urls.static import static
from django.conf import settings




urlpatterns = [
    path('admin/', admin.site.urls),
    # path('',include('core.urls')),
    # path('api-auth/', include('rest_framework.urls')),
    path('', include('account.urls', namespace='account')),
    path('', include('product.urls', namespace='product')),
    path('', include('order.urls', namespace='order')),
    path('cart/', include('cart.urls', namespace='cart')),
    # path('payment/', include('payment.urls', namespace='payment')),

] 

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
    urlpatterns += [path('__debug__/', include(debug_toolbar_urls()))]
    