"""Authentication API tests."""

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status


AUTH_URL = reverse("api-auth")


class AuthenticationApiTests(TestCase):
    """Authentication API tests."""

    def setUp(self):
        """Initialize each test."""
        self.client = APIClient()

    def test_create_token_valid_credentials(self):
        """Test creating a token for valid credentials."""
        # Create user
        username = "test_user"
        password = "test_password"

        model = get_user_model()
        model.objects.create_user(username=username, password=password)

        # Make request
        data = {"username": username, "password": password}
        res = self.client.post(AUTH_URL, data)

        # Check response
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn("token", res.data)

    def test_create_token_no_username(self):
        """Test creating a token without the username."""
        # Make request
        data = {"password": "test_password"}
        res = self.client.post(AUTH_URL, data)

        # Check response
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn("token", res.data)

    def test_create_token_empty_username(self):
        """Test creating a token with an empty username."""
        # Make request
        data = {"username": "", "password": "test_password"}
        res = self.client.post(AUTH_URL, data)

        # Check response
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn("token", res.data)

    def test_create_token_no_password(self):
        """Test creating a token without the password."""
        # Make request
        data = {"username": "test_user"}
        res = self.client.post(AUTH_URL, data)

        # Check response
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn("token", res.data)

    def test_create_token_empty_password(self):
        """Test creating a token with an empty password."""
        # Make request
        data = {"username": "test_user", "password": ""}
        res = self.client.post(AUTH_URL, data)

        # Check response
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn("token", res.data)

    def test_create_token_invalid_credentials(self):
        """Test creating a token for invalid credentials."""
        # Create user
        username = "test_user"
        password = "valid_password"

        model = get_user_model()
        model.objects.create_user(username=username, password=password)

        # Make request
        data = {"username": username, "password": "invalid_password"}
        res = self.client.post(AUTH_URL, data)

        # Check response
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn("token", res.data)
