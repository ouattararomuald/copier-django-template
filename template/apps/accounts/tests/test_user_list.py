import pytest
from django.conf import settings
from django.contrib.auth import get_user_model
from django.test import override_settings
from django.urls import reverse
from rest_framework import status

from tests.common import login_user

User = get_user_model()


@pytest.mark.django_db
def test_user_registration_success(api_client):
    """Test user registration endpoint."""
    data = {
        "email": "user@example.com",
        "username": "user@example.com",
        "first_name": "John",
        "last_name": "Doe",
        "password": "ComplexPa$$w0rd",
    }

    response = api_client.post(reverse("user-list"), data=data, format="json")

    assert response.status_code == status.HTTP_201_CREATED
    user_profile = response.json()

    assert set(user_profile.keys()) == {User.USERNAME_FIELD, User._meta.pk.name, *User.REQUIRED_FIELDS}
    assert user_profile["username"] == data["username"]
    assert user_profile["first_name"] == data["first_name"]
    assert user_profile["last_name"] == data["last_name"]


@pytest.mark.django_db
@pytest.mark.parametrize("missing_field", ["email", "first_name", "last_name", "password"])
def test_user_registration_fails_when_required_field_is_missing(api_client, missing_field):
    """Test user registration endpoint fails when required fields are missing."""
    data = {
        "email": "user@example.com",
        "first_name": "John",
        "last_name": "Doe",
        "password": "ComplexPa$$w0rd",
    }

    data.pop(missing_field)

    response = api_client.post(reverse("user-list"), data=data, format="json")

    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
@override_settings(DJOSER=dict(settings.DJOSER, **{"HIDE_USERS": True}))
def test_user_cannot_list_other_users(api_client, user, user_1, user_2):
    """Test user can list users."""
    login_user(api_client, user)

    response = api_client.get(reverse("user-list"))
    assert response.status_code == status.HTTP_200_OK

    assert len(response.json()) == 1


@pytest.mark.django_db
@override_settings(DJOSER=dict(settings.DJOSER, **{"HIDE_USERS": False}))
def test_user_can_list_other_users(api_client, user, user_1, user_2):
    """Test user can list users."""
    login_user(api_client, user)

    response = api_client.get(reverse("user-list"))
    assert response.status_code == status.HTTP_200_OK

    assert len(response.json()) == 3


@pytest.mark.django_db
def test_superuser_can_list_all_users(api_client, superuser, user_1, user_2):
    """Test superuser can list all users."""
    login_user(api_client, superuser)

    response = api_client.get(reverse("user-list"))
    assert response.status_code == status.HTTP_200_OK

    assert len(response.json()) == 3
