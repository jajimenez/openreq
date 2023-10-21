from django.contrib.auth import get_user_model
from django.test import TestCase

from core.models import Category, Incident


class ModelTests(TestCase):
    """Test the Core models."""

    def test_create_user(self):
        """Test creating a user."""
        # Create user
        username = "example_user"
        password = "example_password"

        model = get_user_model()
        u = model.objects.create_user(username=username, password=password)

        # Check database object
        self.assertEqual(u.username, username)
        self.assertTrue(u.check_password(password))

    def test_create_category(self):
        """Test creating a category."""
        # Create category
        name = "example"
        c = Category.objects.create(name=name)

        # Check database object
        self.assertEqual(c.name, name)

    def test_create_incident(self):
        """Test creating an incident."""
        # Create user
        username = "example_user"
        password = "example_password"

        model = get_user_model()
        user = model.objects.create_user(username=username, password=password)

        # Create category
        name = "Category"
        c = Category.objects.create(name=name)

        # Create incident
        sub = "Incident"
        desc = "Description"

        i = Incident.objects.create(
            category=c, opened_by=user, subject=sub, description=desc
        )

        # Check database object
        self.assertEqual(i.opened_by.username, username)
        self.assertTrue(i.opened_by.check_password(password))
        self.assertEqual(i.category.name, name)
        self.assertEqual(i.subject, sub)
        self.assertEqual(i.description, desc)
        self.assertIsNone(i.assigned_to)
        self.assertFalse(i.closed)
