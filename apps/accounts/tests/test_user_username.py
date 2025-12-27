import pytest
from django.conf import settings
from django.contrib.auth import get_user_model
from django.test import override_settings
from django.urls import reverse
from rest_framework import status

from tests.assertions import email_assertions
from tests.common import login_user

User = get_user_model()


@pytest.mark.django_db
def test_user_reset_username_should_send_email_with_reset_link_to_user(api_client, user):
    login_user(api_client, user)

    data = {"email": user.email}

    response = api_client.post(reverse("user-reset-username"), data, format="json")
    assert response.status_code == status.HTTP_204_NO_CONTENT
    email_assertions.assert_emails_in_mailbox(1)


@pytest.mark.django_db
@override_settings(DJOSER=dict(settings.DJOSER, **{"USERNAME_RESET_SHOW_EMAIL_NOT_FOUND": False}))
def test_user_reset_username_for_non_existing_email_success(api_client, user):
    """Ensure that reset username for non-existing email addresses works.

    We expect that the API returns a 204 No Content response and no email is sent.
    """
    login_user(api_client, user)

    data = {"email": "not.existing.email@acme.com"}

    response = api_client.post(reverse("user-reset-username"), data, format="json")
    assert response.status_code == status.HTTP_204_NO_CONTENT
    email_assertions.assert_emails_in_mailbox(0)


@pytest.mark.django_db
def test_user_set_username(api_client, user, raw_password: str):
    login_user(api_client, user)

    data = {
        "new_username": "new-username.acme",
        "current_password": raw_password,
    }

    email_assertions.assert_emails_in_mailbox(0)
    response = api_client.post(reverse("user-set-username"), data, format="json")

    assert response.status_code == status.HTTP_204_NO_CONTENT
    email_assertions.assert_emails_in_mailbox(1)
