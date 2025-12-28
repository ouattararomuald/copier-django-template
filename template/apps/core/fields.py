from django.db import models


class LowercaseEmailField(models.EmailField):
    """Email field that lowercases it."""

    def get_prep_value(self, value):
        value = super().get_prep_value(value)
        return str(value).strip().lower()
