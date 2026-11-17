"""
URL configuration for djapro project.
"""

from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static

from djapro import settings

from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView,
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('travello.urls')),
    path('accounts/', include('accounts.urls')),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path(
        'api/docs/',
        SpectacularSwaggerView.as_view(url_name='schema'),
        name='swagger-ui',
    ),
    path(
        'api/redoc/',
        SpectacularRedocView.as_view(url_name='schema'),
        name='redoc',
    ),
    path("api/bookings/", include("bookings.urls")),
    path("api/payments/", include("payments.urls")),
    path("api/reviews/", include("reviews.urls")),
    path("api/wishlist/", include("wishlist.urls")),
]

if settings.HAS_DEBUG_TOOLBAR:
    import debug_toolbar

    urlpatterns += [
        path('_debug_/', include(debug_toolbar.urls)),
    ]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )
