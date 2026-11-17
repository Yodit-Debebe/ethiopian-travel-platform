from datetime import timedelta

from django.conf import settings
from django.utils import timezone
from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import AuthenticationFailed


def token_is_expired(token):
    ttl_days = getattr(settings, 'AUTH_TOKEN_TTL_DAYS', 7)
    return token.created < timezone.now() - timedelta(days=ttl_days)


class ExpiringTokenAuthentication(TokenAuthentication):
    def authenticate_credentials(self, key):
        user, token = super().authenticate_credentials(key)

        if token_is_expired(token):
            token.delete()
            raise AuthenticationFailed(
                'Token has expired. Please log in again.'
            )

        return (user, token)
