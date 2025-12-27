import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status

from tests.assertions import email_assertions
from tests.common import login_user

User = get_user_model()


@pytest.mark.django_db
def test_user_set_password(api_client, user, raw_password: str):
    login_user(api_client, user)

    data = {
        "current_password": raw_password,
        "new_password": "newPa$$w0rd",
    }

    email_assertions.assert_emails_in_mailbox(0)
    response = api_client.post(reverse("user-set-password"), data, format="json")

    assert response.status_code == status.HTTP_204_NO_CONTENT
    email_assertions.assert_emails_in_mailbox(1)


@pytest.mark.django_db
def test_user_reset_password_should_send_email_with_reset_link_to_user(api_client, user, raw_password: str):
    login_user(api_client, user)

    data = {"email": user.email}

    email_assertions.assert_emails_in_mailbox(0)
    response = api_client.post(reverse("user-reset-password"), data, format="json")

    assert response.status_code == status.HTTP_204_NO_CONTENT
    email_assertions.assert_emails_in_mailbox(1)
