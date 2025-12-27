from rest_framework_simplejwt.tokens import RefreshToken


def get_token_for_user(user):
    """generate JWT tokens for a user."""
    refresh = RefreshToken.for_user(user)
    return {
        "refresh": str(refresh),
        "access": str(refresh.access_token),
    }


def login_user(client, user):
    token = get_token_for_user(user=user)

    client.credentials(HTTP_AUTHORIZATION=f"Bearer {token['access']}")
