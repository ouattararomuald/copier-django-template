import random
from pathlib import Path

import pytest


@pytest.fixture(scope="session")
def root_path() -> str:
    return str(Path(__file__).parent.parent)


@pytest.fixture(scope="session")
def answers() -> dict[str, str]:
    return {
        "project_name": "test-project",
        "project_version": "0.1.0",
        "project_description": "A django project",
        "project_url": "https://github.com/ouattararomuald/test-project",
        "author_name": "Romuald",
        "django_version": "5.2",
        "database_engine": "postgres",
        "postgres_version": 17,
        "python_version": "3.12",
        "use_django_toolbar": True,
        "use_django_extensions": True,
        "use_drf_spectacular": True,
    }


def pytest_collection_modifyitems(items: list[pytest.Item]) -> None:
    """Randomise the order of tests to avoid flakiness."""
    random.shuffle(items)
