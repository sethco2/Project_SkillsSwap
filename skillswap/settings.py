"""
Django settings for the Seth Grant Portfolio + Campus SkillSwap project.

Reads sensitive values from environment variables so the same code runs
locally (with sane fallbacks) and on Railway/Render (with real secrets).
"""

import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent


def _env_bool(name: str, default: bool = False) -> bool:
    return os.environ.get(name, str(default)).lower() in {"1", "true", "yes", "on"}


# --- Security --------------------------------------------------------------
SECRET_KEY = os.environ.get(
    "DJANGO_SECRET_KEY",
    "django-insecure-dev-only-change-me-in-production-1234567890",
)
DEBUG = _env_bool("DJANGO_DEBUG", default=True)

ALLOWED_HOSTS = [
    h.strip()
    for h in os.environ.get(
        "DJANGO_ALLOWED_HOSTS", "localhost,127.0.0.1,.railway.app,.onrender.com"
    ).split(",")
    if h.strip()
]

# Trust HTTPS hosts behind Railway/Render proxies for CSRF.
CSRF_TRUSTED_ORIGINS = [
    o.strip()
    for o in os.environ.get(
        "DJANGO_CSRF_TRUSTED_ORIGINS",
        "https://*.railway.app,https://*.onrender.com",
    ).split(",")
    if o.strip()
]


# --- Apps ------------------------------------------------------------------
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # Portfolio is the front door of the site.
    "portfolio",

    # Campus SkillSwap (existing class project, featured as live demo).
    "skills",
    "accounts",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    # Whitenoise serves static files in production without nginx.
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "skillswap.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "portfolio.context_processors.site_meta",
            ],
        },
    },
]

WSGI_APPLICATION = "skillswap.wsgi.application"


# --- Database --------------------------------------------------------------
# SQLite by default. Set DATABASE_URL on Railway/Render to use Postgres.
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

DATABASE_URL = os.environ.get("DATABASE_URL")
if DATABASE_URL:
    try:
        import dj_database_url

        DATABASES["default"] = dj_database_url.parse(
            DATABASE_URL, conn_max_age=600, ssl_require=not DEBUG
        )
    except ImportError:
        # dj-database-url is in requirements.txt; if it's missing, fall
        # back to SQLite rather than crashing.
        pass


# --- Auth ------------------------------------------------------------------
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]


# --- i18n ------------------------------------------------------------------
LANGUAGE_CODE = "en-us"
TIME_ZONE = "America/Chicago"
USE_I18N = True
USE_TZ = True


# --- Static & media --------------------------------------------------------
STATIC_URL = "static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"

# Whitenoise: hashed + compressed in production, plain in dev.
STORAGES = {
    "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
    "staticfiles": {
        "BACKEND": (
            "whitenoise.storage.CompressedManifestStaticFilesStorage"
            if not DEBUG
            else "django.contrib.staticfiles.storage.StaticFilesStorage"
        ),
    },
}

MEDIA_URL = "media/"
MEDIA_ROOT = BASE_DIR / "media"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# --- SkillSwap auth redirects ---------------------------------------------
LOGIN_REDIRECT_URL = "dashboard"
LOGOUT_REDIRECT_URL = "portfolio:home"
LOGIN_URL = "login"


# --- Email (contact form) --------------------------------------------------
# Defaults to console backend in dev; set EMAIL_HOST + creds in production.
EMAIL_BACKEND = os.environ.get(
    "DJANGO_EMAIL_BACKEND",
    "django.core.mail.backends.console.EmailBackend"
    if DEBUG
    else "django.core.mail.backends.smtp.EmailBackend",
)
EMAIL_HOST = os.environ.get("EMAIL_HOST", "")
EMAIL_PORT = int(os.environ.get("EMAIL_PORT", "587"))
EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER", "")
EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD", "")
EMAIL_USE_TLS = _env_bool("EMAIL_USE_TLS", default=True)
DEFAULT_FROM_EMAIL = os.environ.get(
    "DEFAULT_FROM_EMAIL", "Seth Grant Portfolio <noreply@example.com>"
)
CONTACT_EMAIL = os.environ.get("CONTACT_EMAIL", "sethgrant2003@gmail.com")


# --- Production hardening --------------------------------------------------
if not DEBUG:
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
    SECURE_SSL_REDIRECT = _env_bool("DJANGO_SSL_REDIRECT", default=True)
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_HSTS_SECONDS = 3600
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    X_FRAME_OPTIONS = "DENY"
