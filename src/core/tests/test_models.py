from django.contrib.auth import get_user_model
from django.test import TestCase


class ModelTests(TestCase):
    """Test the Core models."""

    def test_create_user_successful(self):
        """Test creating a user successfully."""

        username = "example_user"
        password = "example_password"

        model = get_user_model()
        user = model.objects.create_user(username=username, password=password)

        self.assertEqual(user.username, username)
        self.assertTrue(user.check_password(password))
