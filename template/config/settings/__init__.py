from django.conf import settings

from config.logging import configure_logging

configure_logging(debug=settings.DEBUG)
