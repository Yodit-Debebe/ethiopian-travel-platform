
from datetime import timedelta

from django.conf import settings
from django.contrib.auth.models import User
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from django.urls import reverse


class AuthenticationAPITests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpassword123"
        )

    def test_user_registration(self):
        data = {
            "username": "newuser",
            "email": "newuser@example.com",
            "password": "newpassword123"
        }

        response = self.client.post(
            reverse("register-api"),
            data
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )
        self.assertTrue(
            User.objects.filter(username="newuser").exists()
        )

    def test_user_login(self):
        data = {
            "username": "testuser",
            "password": "testpassword123"
        }

        response = self.client.post(
            reverse("login-api"),
            data
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
        self.assertIn("token", response.data)

    def test_user_logout(self):
        token = Token.objects.create(user=self.user)

        self.client.credentials(
            HTTP_AUTHORIZATION=f"Token {token.key}"
        )

        response = self.client.post(reverse("logout-api"))

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
        self.assertFalse(
            Token.objects.filter(user=self.user).exists()
        )

    def test_logout_with_invalid_token(self):
        self.client.credentials(
            HTTP_AUTHORIZATION="Token invalid_token_123"
        )

        response = self.client.post(reverse("logout-api"))

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED
        )

    def expire_token(self, token):
        Token.objects.filter(pk=token.pk).update(
            created=(
                timezone.now()
                - timedelta(days=settings.AUTH_TOKEN_TTL_DAYS + 1)
            )
        )

    def test_expired_token_is_rejected(self):
        token = Token.objects.create(user=self.user)
        self.expire_token(token)

        self.client.credentials(
            HTTP_AUTHORIZATION=f"Token {token.key}"
        )

        response = self.client.get(reverse("profile-api"))

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED
        )
        self.assertFalse(
            Token.objects.filter(pk=token.pk).exists()
        )

    def test_login_refreshes_expired_token(self):
        token = Token.objects.create(user=self.user)
        self.expire_token(token)

        response = self.client.post(
            reverse("login-api"),
            {
                "username": "testuser",
                "password": "testpassword123",
            }
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
        self.assertNotEqual(response.data["token"], token.key)
        self.assertTrue(
            Token.objects.filter(user=self.user).exists()
        )
