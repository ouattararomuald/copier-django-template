from django.conf import settings
from django.contrib import admin
from django.urls import include, path, re_path


urlpatterns = [
    path("admin/", admin.site.urls),
    re_path(r"^api/auth/", include("djoser.urls")),
    re_path(r"^api/auth/", include("djoser.urls.jwt")),
]
if settings.DEBUG:
    if "debug_toolbar" in settings.INSTALLED_APPS:
        from debug_toolbar.toolbar import debug_toolbar_urls

        urlpatterns += debug_toolbar_urls()
