"""
URL configuration for PK PY CMS project.
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.core.urls')),
    path('', include('apps.content.urls')),
    path('media-library/', include('apps.media_library.urls')),
    path('accounts/', include('apps.users.urls')),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
    
    # Add debug toolbar URLs
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns

# Customize admin site
admin.site.site_header = settings.SITE_NAME + ' Administration'
admin.site.site_title = settings.SITE_NAME + ' Admin'
admin.site.index_title = 'Welcome to ' + settings.SITE_NAME
