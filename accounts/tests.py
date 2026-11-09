
from django.contrib.auth.models import User
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
