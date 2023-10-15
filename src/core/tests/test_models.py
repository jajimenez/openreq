from django.contrib.auth import get_user_model
from django.test import TestCase

# from core.models import Tag, Incident
from core.models import Incident


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

    # def test_create_tag(self):
    #     """Test creating a tag successfully."""
    #     name = "example"
    #     tag = Tag.objects.create(name=name)

    #     self.assertEqual(tag.name, name)

    def test_create_incident(self):
        """Test creating a tag successfully."""
        # Create user
        username = "example_user"
        password = "example_password"

        model = get_user_model()
        user = model.objects.create_user(username=username, password=password)

        # Create tags
        # name1 = "Tag 1"
        # name2 = "Tag 2"

        # tags = [Tag.objects.create(name=name1), Tag.objects.create(name=name2)]

        # Create incident
        desc = "Incident example"
        # inc = Incident.objects.create(user=user, description=desc, tags=tags)
        inc = Incident.objects.create(user=user, description=desc)

        self.assertEqual(inc.user.username, username)
        self.assertTrue(inc.user.check_password(password))
        self.assertEqual(inc.description, desc)
        # self.assertEqual(inc.tags.length, 2)
        # self.assertEqual(inc.tags[0].name, name1)
        # self.assertEqual(inc.tags[1].name, name2)
