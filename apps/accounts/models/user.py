from django.contrib.auth.models import AbstractUser
from django.db import models

from apps.core.fields import LowercaseEmailField


class User(AbstractUser):
    email = LowercaseEmailField(
        verbose_name="email address",
        unique=True,
        error_messages={
            "unique": "A user with that email already exists.",
        },
    )
    first_name = models.CharField("first name", max_length=150)
    last_name = models.CharField("last name", max_length=150)

    REQUIRED_FIELDS = ["first_name", "last_name"]  # noqa: RUF012
