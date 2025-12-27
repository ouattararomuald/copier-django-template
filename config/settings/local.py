from .base import *  # noqa: F403

DEBUG = True

# django-debug-toolbar
# ------------------------------------------------------------------------------
# https://django-debug-toolbar.readthedocs.io/en/latest/installation.html#check-for-prerequisites
INSTALLED_APPS += [
    "debug_toolbar",
]

MIDDLEWARE += [
    "debug_toolbar.middleware.DebugToolbarMiddleware",
]

INTERNAL_IPS = ["127.0.0.1"]

# django-extensions
# ------------------------------------------------------------------------------
# https://django-extensions.readthedocs.io/en/latest/#getting-started
INSTALLED_APPS += [
    "django_extensions",
]

# drf_spectacular
# ------------------------------------------------------------------------------
# https://drf-spectacular.readthedocs.io/en/latest/
INSTALLED_APPS += [
    "drf_spectacular",
]

REST_FRAMEWORK = {
    **REST_FRAMEWORK,
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
}

# By Default swagger ui is available only to admin user(s). You can change permission classes to change that
# See more configuration options at https://drf-spectacular.readthedocs.io/en/latest/settings.html#settings
SPECTACULAR_SETTINGS = {
    "TITLE": "Cookiecutter Django DRF API",
    "DESCRIPTION": "Cookiecutter Django DRF description",
    "VERSION": "0.1.0",
    "SERVE_PERMISSIONS": [],
    "SCHEMA_PATH_PREFIX": "/api/",
}
