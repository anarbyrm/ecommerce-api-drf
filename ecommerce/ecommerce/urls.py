from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView


urlpatterns = [    
    path('admin/', admin.site.urls),           
    path('schema/', SpectacularAPIView.as_view(), name='api-schema'),
    path('', SpectacularSwaggerView.as_view(url_name='api-schema'), name='api-doc'),
    
    # project urls
    path('accounts/', include('accounts.api.urls')),
    path('products/', include('products.api.urls')),
    
]
