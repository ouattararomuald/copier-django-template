from django.apps import AppConfig
from django.conf import settings


class CommonConfig(AppConfig):
    name = "apps.common"
    verbose_name = "Common"

    def ready(self):
        """Initialize structlog when Django starts."""
        from .logging import configure_structlog

        configure_structlog(debug=settings.DEBUG)
