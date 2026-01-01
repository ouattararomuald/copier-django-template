import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status

from tests.common import login_user

User = get_user_model()


@pytest.mark.django_db
def test_user_can_get_own_detail(api_client, user):
    """Test that users can access their own detail."""
    login_user(api_client, user)

    response = api_client.get(reverse("user-detail", args=[user.pk]))
    assert response.status_code == status.HTTP_200_OK

    user_profile = response.json()

    assert set(user_profile.keys()) == {User.USERNAME_FIELD, User._meta.pk.name, *User.REQUIRED_FIELDS}

    assert user_profile["id"] == user.pk
    assert user_profile["username"] == user.username
    assert user_profile["first_name"] == user.first_name
    assert user_profile["last_name"] == user.last_name


@pytest.mark.django_db
def test_user_cannot_get_other_user_detail(api_client, user, user_1):
    """Test that users can't access other users' data."""
    login_user(api_client, user)

    response = api_client.get(reverse("user-detail", args=[user_1.pk]))
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
def test_superuser_can_get_other_user_detail(api_client, superuser, user_1):
    """Test superuser can access other users' detail."""
    login_user(api_client, superuser)

    response = api_client.get(reverse("user-detail", args=[user_1.pk]))
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
@pytest.mark.parametrize("field_name,target_value", [("first_name", "NewFirstName"), ("last_name", "NewLastName")])
def test_user_can_patch_update_own_detail(api_client, user, field_name, target_value):
    login_user(api_client, user)

    response = api_client.patch(
        reverse("user-detail", args=[user.pk]),
        data={field_name: target_value},
        format="json",
    )

    assert response.status_code == status.HTTP_200_OK
    user.refresh_from_db()
    assert getattr(user, field_name) == target_value


@pytest.mark.django_db
def test_user_can_put_update_own_detail(api_client, user):
    login_user(api_client, user)

    data = {
        "first_name": "NewFirstName",
        "last_name": "NewLastName",
        "email": user.email,
    }
    response = api_client.put(
        reverse("user-detail", args=[user.pk]),
        data=data,
        format="json",
    )

    assert response.status_code == status.HTTP_200_OK
    user.refresh_from_db()
    for field_name, value in data.items():
        assert getattr(user, field_name) == value
