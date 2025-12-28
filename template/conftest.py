import pytest
from rest_framework.test import APIClient

pytest_plugins = [
    "tests.fixtures",
]


@pytest.fixture
def api_client():
    """Fixture to provide an authenticated API client for testing."""
    return APIClient(enforce_csrf_checks=True)
