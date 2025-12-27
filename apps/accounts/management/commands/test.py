from django.core.management import BaseCommand

from apps.common.logging import get_logger


class Command(BaseCommand):
    help = "Clean preproduction database and set up required store groups and stores. DO NOT USE IN PRODUCTION!"

    def handle(self, *args, **options):
        logger = get_logger(__name__)

        logger.info("Starting test command")
        logger.info("user_create", id=123, name="John Doe")

        # raise Exception("Test exception")
