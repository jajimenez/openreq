"""OpenReq - User - Tests."""

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework.status import (
    HTTP_200_OK, HTTP_401_UNAUTHORIZED, HTTP_405_METHOD_NOT_ALLOWED
)


ME_URL = reverse("user:me")


class PublicUserApiTests(TestCase):
    """User API unauthenticated tests."""

    def setUp(self):
        """Initialize each test."""
        self.client = APIClient()

    def test_get_current_user_unauthenticated(self):
        """Test getting the current user without authentication."""
        res = self.client.get(ME_URL)
        self.assertEqual(res.status_code, HTTP_401_UNAUTHORIZED)


class PrivateUserApiTests(TestCase):
    """User API authenticated tests."""

    def setUp(self):
        """Initialize each test."""
        self.user = get_user_model().objects.create_user(
            username="test_user", password="test_password", first_name="Test",
            last_name="User", email="test@example.com"
        )

        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_get_current_user(self):
        """Test getting the current user with valid credentials."""
        res = self.client.get(ME_URL)
        self.assertEqual(res.status_code, HTTP_200_OK)

        self.assertEqual(
            res.data, {
                "username": self.user.username,
                "first_name": self.user.first_name,
                "last_name": self.user.last_name,
                "email": self.user.email
            }
        )

    def test_get_current_user_post_not_allowed(self):
        """Test getting the current user with valid credentials and the POST
        method.
        """
        res = self.client.post(ME_URL, {})
        self.assertEqual(res.status_code, HTTP_405_METHOD_NOT_ALLOWED)
