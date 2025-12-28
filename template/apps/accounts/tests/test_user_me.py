import pytest
from django.conf import settings
from django.contrib.auth import get_user_model
from django.test.utils import override_settings
from django.urls import reverse
from rest_framework import status

from tests.common import login_user

User = get_user_model()


@pytest.mark.django_db
def test_get_current_user(api_client, user):
    login_user(api_client, user)

    response = api_client.get(reverse("user-me"))

    assert response.status_code == status.HTTP_200_OK
    assert set(response.data.keys()) == {User.USERNAME_FIELD, User._meta.pk.name, *User.REQUIRED_FIELDS}


@pytest.mark.django_db
@override_settings(DJOSER=dict(settings.DJOSER, **{"SEND_ACTIVATION_EMAIL": False}))
def test_patch_email_change_with_send_activation_email_false(api_client, user):
    """Verify that email is not changed during patch update.

    Email is unchanged because it's used as the login field.
    """
    login_user(api_client, user)
    assert user.is_active
    original_email = user.email

    data = {"email": "new-email.0@example.com"}
    response = api_client.patch(reverse("user-me"), data=data, format="json")

    assert response.status_code == status.HTTP_200_OK
    user.refresh_from_db()
    assert user.email == original_email
    assert user.is_active


@pytest.mark.django_db
@override_settings(DJOSER=dict(settings.DJOSER, **{"SEND_ACTIVATION_EMAIL": True}))
def test_patch_email_change_with_send_activation_email_true(api_client, user):
    """Verify that email is not changed during patch update.

    Email is unchanged because it's used as the login field.
    """
    login_user(api_client, user)
    assert user.is_active
    original_email = user.email

    data = {"email": "new-email.1@example.com"}
    response = api_client.patch(reverse("user-me"), data=data, format="json")

    assert response.status_code == status.HTTP_200_OK
    user.refresh_from_db()
    assert user.email == original_email
    assert user.is_active


@pytest.mark.django_db
@pytest.mark.parametrize("field_name,target_value", [("first_name", "NewFirstName"), ("last_name", "NewLastName")])
def test_patch_success(api_client, user, field_name, target_value):
    login_user(api_client, user)

    response = api_client.patch(reverse("user-me"), data={field_name: target_value}, format="json")

    assert response.status_code == status.HTTP_200_OK
    user.refresh_from_db()
    assert getattr(user, field_name) == target_value


@pytest.mark.django_db
def test_put_success(api_client, user):
    login_user(api_client, user)

    data = {
        "first_name": "NewFirstName",
        "last_name": "NewLastName",
    }
    response = api_client.put(reverse("user-me"), data=data, format="json")

    assert response.status_code == status.HTTP_200_OK
    user.refresh_from_db()
    for field_name, value in data.items():
        assert getattr(user, field_name) == value
