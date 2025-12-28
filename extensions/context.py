import secrets
import string

from copier_templates_extensions import ContextHook
from typing import Any
import datetime


class ContextUpdater(ContextHook):
    update = False

    def hook(self, context: dict[str, Any]) -> dict[str, Any]:
        project_name = context.get("project_name")
        if project_name:
            project_slug = context["project_slug"] = project_name.lower().replace(" ", "-")
            context["package"] = project_slug.replace("-", "_")

        if "__year" not in context:
            context["__year"] = str(datetime.datetime.today().year)

        if "django_secret_key" not in context:
            context["django_secret_key"] = self.generate_django_secret_key()

    def generate_django_secret_key(self, length: int = 64) -> str:
        chars = string.ascii_letters + string.digits + string.punctuation
        # Django excludes quotes and backslashes to avoid config issues
        chars = chars.replace('"', '').replace("'", '').replace('\\', '')
        return ''.join(secrets.choice(chars) for _ in range(length))
