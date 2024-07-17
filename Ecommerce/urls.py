
from django.contrib import admin
from django.urls import path, include
from debug_toolbar.toolbar import debug_toolbar_urls
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('account/', include('account.urls', namespace='account')),
    path('product/', include('product.urls', namespace='product')),
    path('__debug__/', include('debug_toolbar.urls')),
] #+ debug_toolbar_urls() #+static(settings.MEDIA_URL, document_root=settingsMEDIA_ROOT)
