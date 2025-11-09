"""
Main URL Configuration
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    # Admin panel
    path('admin/', admin.site.urls),
    
    # API Documentation
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    
    # API Routes
    path('api/auth/', include('apps.authentication.urls')),
    path('api/users/', include('apps.users.urls')),
    path('api/core/', include('apps.clients.urls')),  # Core user endpoints
    path('api/core/', include('apps.reports.urls')),  # Core user reports
    path('api/core/', include('apps.messaging.urls')),  # Core user messaging
    path('api/client/', include('apps.clients.urls')),  # Client endpoints
    path('api/guest/', include('apps.sharing.urls')),  # Guest access
    path('api/subscriptions/', include('apps.subscriptions.urls')),
    path('api/billing/', include('apps.subscriptions.urls')),
    path('api/admin/', include('apps.audit.urls')),  # Admin endpoints
    path('api/analytics/', include('apps.analytics.urls')),
    path('api/notifications/', include('apps.notifications.urls')),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Custom admin site headers
admin.site.site_header = "Dashboard Admin"
admin.site.site_title = "Dashboard Admin Portal"
admin.site.index_title = "Welcome to Dashboard Administration"