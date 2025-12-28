import pytest
from django.contrib.auth import get_user_model

User = get_user_model()


@pytest.fixture
def raw_password() -> str:
    return "Pa$$w0rd"


@pytest.fixture
def user(raw_password: str):
    """Fixture to generate a user."""
    data = {
        "email": "user.acme.0@example.com",
        "username": "user.acme.0@example.com",
        "password": raw_password,
        "first_name": "John",
        "last_name": "Doe",
    }
    return User.objects.create_user(**data)


@pytest.fixture
def user_1(raw_password: str):
    """Fixture to generate a user."""
    data = {
        "email": "user.acme.1@example.com",
        "username": "user.acme.1@example.com",
        "password": raw_password,
        "first_name": "John",
        "last_name": "Doe 1",
    }
    return User.objects.create_user(**data)


@pytest.fixture
def user_2(raw_password: str):
    """Fixture to generate a user."""
    data = {
        "email": "user.acme.2@example.com",
        "username": "user.acme.2@example.com",
        "password": raw_password,
        "first_name": "John",
        "last_name": "Doe 2",
    }
    return User.objects.create_user(**data)


@pytest.fixture
def superuser(raw_password: str):
    """Fixture to generate a superuser."""
    data = {
        "email": "superuser.acme.3@example.com",
        "username": "superuser.acme.3@example.com",
        "password": raw_password,
        "first_name": "Super John",
        "last_name": "Doe 3",
    }
    return User.objects.create_superuser(**data)
