"""
Project-level URL router for SkillSwap.

This file is the "front door" — every request first hits the patterns below.
We mostly use `include()` to delegate to each app's own urls.py, which keeps
this file short and lets each app own its own routes.
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView  # quick way to render a template

urlpatterns = [
    # Django admin site (auto-generated CRUD UI for our models).
    path('admin/', admin.site.urls),

    # Landing page. Using TemplateView avoids needing a view function just
    # to render one static page. The `name='home'` is what LOGOUT_REDIRECT_URL
    # in settings.py refers to.
    path('', TemplateView.as_view(template_name='home.html'), name='home'),

    # Auth URLs (login, logout, password change/reset). Django provides these
    # for free — we just have to plug them in. They live under /accounts/...
    # by default and look for templates inside templates/registration/.
    path('accounts/', include('django.contrib.auth.urls')),

    # Our own register view (signup) lives in the accounts app.
    path('accounts/', include('accounts.urls')),

    # Skill marketplace lives at /skills/...
    path('skills/', include('skills.urls')),
]
