from django.contrib.auth import get_user_model
from django.test import TestCase

from core.models import Tag, Incident


class ModelTests(TestCase):
    """Test the Core models."""

    def test_create_user(self):
        """Test creating a user."""
        # Create user
        username = "example_user"
        password = "example_password"

        model = get_user_model()
        user = model.objects.create_user(username=username, password=password)

        # Check database object
        self.assertEqual(user.username, username)
        self.assertTrue(user.check_password(password))

    def test_create_tag(self):
        """Test creating a tag."""
        # Create tag
        name = "example"
        tag = Tag.objects.create(name=name)

        # Check database object
        self.assertEqual(tag.name, name)

    def test_create_incident(self):
        """Test creating an incident."""
        # Create user
        username = "example_user"
        password = "example_password"

        model = get_user_model()
        user = model.objects.create_user(username=username, password=password)

        # Create tags
        name1 = "Tag 1"
        name2 = "Tag 2"

        tags = [Tag.objects.create(name=name1), Tag.objects.create(name=name2)]

        # Create incident
        sub = "Incident"
        desc = "Description"

        inc = Incident.objects.create(
            opened_by=user, subject=sub, description=desc
        )

        inc.tags.set(tags)

        # Check database object
        self.assertEqual(inc.opened_by.username, username)
        self.assertTrue(inc.opened_by.check_password(password))
        self.assertEqual(inc.subject, sub)
        self.assertEqual(inc.description, desc)
        self.assertEqual(inc.tags.count(), len(tags))
        self.assertEqual(inc.tags.get(id=tags[0].id).name, name1)
        self.assertEqual(inc.tags.get(id=tags[1].id).name, name2)
        self.assertIsNone(inc.assigned_to)
        self.assertFalse(inc.closed)
