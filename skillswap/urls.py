"""
Project-level URL router.

The portfolio app owns the front door (/, /about/, /projects/...).
Campus SkillSwap lives at /skillswap/ and is featured as a live demo.
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),

    # Portfolio (front door).
    path("", include("portfolio.urls")),

    # Auth URLs (login, logout, password change/reset).
    path("accounts/", include("django.contrib.auth.urls")),
    path("accounts/", include("accounts.urls")),

    # Campus SkillSwap — Django class project, kept live as a demo.
    path("skillswap/", include("skills.urls")),
]

# Serve uploaded media in development.
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
