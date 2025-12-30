import pytest
from django.urls import reverse
from rest_framework import status

from tests.common import get_token_for_user


@pytest.mark.django_db
def test_create_jwt_tokens(api_client, user, raw_password: str):
    data = {
        "username": user.username,
        "password": raw_password,
    }

    response = api_client.post(reverse("jwt-create"), data, format="json")

    assert response.status_code == status.HTTP_200_OK
    token = response.json()
    assert "access" in token
    assert "refresh" in token
    assert token["access"] is not None
    assert token["refresh"] is not None


@pytest.mark.django_db
def test_jwt_refresh(api_client, user):
    token = get_token_for_user(user=user)

    data = {"refresh": token["refresh"]}
    response = api_client.post(reverse("jwt-refresh"), data, format="json")
    assert response.status_code == status.HTTP_200_OK

    token = response.json()
    assert "access" in token
    assert "refresh" in token
    assert token["access"] is not None
    assert token["refresh"] is not None


@pytest.mark.django_db
def test_refresh_token_blacklist_old_refresh_token(api_client, user):
    token = get_token_for_user(user=user)

    data = {"refresh": token["refresh"]}
    response = api_client.post(reverse("jwt-refresh"), data, format="json")
    assert response.status_code == status.HTTP_200_OK

    data = {"token": token["refresh"]}
    response = api_client.post(reverse("jwt-verify"), data, format="json")
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_jwt_verify(api_client, user):
    token = get_token_for_user(user=user)
    access_token = token["access"]
    refresh_token = token["refresh"]

    data = {"token": access_token}
    response = api_client.post(reverse("jwt-verify"), data, format="json")
    assert response.status_code == status.HTTP_200_OK

    data = {"token": refresh_token}
    response = api_client.post(reverse("jwt-verify"), data, format="json")
    assert response.status_code == status.HTTP_200_OK
