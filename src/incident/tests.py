"""OpenReq - Incident - Tests."""

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework.status import (
    HTTP_200_OK, HTTP_201_CREATED, HTTP_401_UNAUTHORIZED
)

from core.models import Incident
from incident.serializers import IncidentSerializer, IncidentDetailSerializer


# "incident:api-root", "incident-list" and "incident:incident-detail" are
# defined in the "rest_framework.routers.DefaultRouter" class.
INCIDENT_URL = reverse("incident:api-root")
INCIDENT_LIST_URL = reverse("incident:incident-list")


def get_incident_detail_url(incident_id):
    """Get the URL of an incident."""
    return reverse("incident:incident-detail", args=[incident_id])


class PublicIncidentApiTests(TestCase):
    """Incident API unauthenticated tests."""

    def setUp(self):
        """Initialize each test."""
        self.client = APIClient()

    def test_get_incident_list_unauthenticated(self):
        """Test getting the list of incidents without authentication."""
        res = self.client.get(INCIDENT_LIST_URL)
        self.assertEqual(res.status_code, HTTP_401_UNAUTHORIZED)


class PrivateIncidentApiTests(TestCase):
    """Incident API authenticated tests."""

    def setUp(self):
        """Initialize each test."""
        self.client = APIClient()
        model = get_user_model()

        self.user = model.objects.create_user(
            username="user", password="password"
        )

        self.other_user = model.objects.create_user(
            username="other_user", password="password"
        )

        self.client.force_authenticate(self.user)

    def test_get_incident_list(self):
        """Test getting the list of incidents of the user."""
        # Create objects
        for i in range(1, 4):
            Incident.objects.create(
                user=self.user,
                subject=f"Incident {i}",
                description=f"Description {i}"
            )

        # Make request
        res = self.client.get(INCIDENT_LIST_URL)

        # Check response
        self.assertEqual(res.status_code, HTTP_200_OK)

        incidents = Incident.objects.filter(user=self.user).order_by("-id")
        ser = IncidentSerializer(incidents, many=True)
        self.assertEqual(res.data, ser.data)

    def test_get_incident(self):
        """Test getting an incident."""
        # Create object
        i = Incident.objects.create(
            user=self.user, subject="Incident", description="Description"
        )

        # Make request
        url = get_incident_detail_url(i.id)
        res = self.client.get(url)

        # Check response
        self.assertEqual(res.status_code, HTTP_200_OK)

        ser = IncidentDetailSerializer(i)
        self.assertEqual(res.data, ser.data)

    def test_create_incident(self):
        """Test creating a incident."""
        # Make request
        data = {"subject": "Incident", "description": "Description"}
        res = self.client.post(INCIDENT_URL, data)

        # Check response
        self.assertEqual(res.status_code, HTTP_201_CREATED)
        self.assertEqual(len(res.data), 3)

        self.assertIn("id", res.data)
        self.assertIsNotNone(res.data["id"])

        self.assertNotIn("user", res.data)

        for k, v in data.items():
            self.assertIn(k, res.data)
            self.assertEqual(res.data[k], v)

        # Check database object
        incident = Incident.objects.get(id=res.data["id"])
        self.assertEqual(incident.user, self.user)

        for k, v in data.items():
            self.assertEqual(getattr(incident, k), v)

    def test_full_update_incident(self):
        """Test updating an incident fully."""
        # Create incident
        prev_sub = "Incident"
        prev_desc = "Incident description."

        incident = Incident.objects.create(
            user=self.user, subject=prev_sub, description=prev_desc
        )

        prev_id = incident.id

        # Make request
        url = get_incident_detail_url(incident.id)
        data = {"subject": "New incident", "description": "New description"}
        res = self.client.put(url, data)

        # Check response
        self.assertEqual(res.status_code, HTTP_200_OK)
        self.assertEqual(len(res.data), 3)

        self.assertIn("id", res.data)
        self.assertEqual(res.data["id"], prev_id)

        self.assertNotIn("user", res.data)

        for k, v in data.items():
            self.assertIn(k, res.data)
            self.assertEqual(res.data[k], v)

        # Check database object
        incident.refresh_from_db()

        self.assertEqual(incident.id, prev_id)
        self.assertEqual(incident.user, self.user)

        for k, v in data.items():
            self.assertEqual(getattr(incident, k), v)

    def test_partial_update_incident(self):
        """Test updating an incident partially."""
        # Create incident
        prev_sub = "Incident"
        prev_desc = "Incident description."

        incident = Incident.objects.create(
            user=self.user, subject=prev_sub, description=prev_desc
        )

        prev_id = incident.id

        # Make request
        url = get_incident_detail_url(prev_id)
        data = {"subject": "New subject"}
        res = self.client.patch(url, data)

        # Check response
        self.assertEqual(res.status_code, HTTP_200_OK)
        self.assertEqual(len(res.data), 3)

        for i in ("id", "subject", "description"):
            self.assertIn(i, res.data)

        self.assertNotIn("user", res.data)

        self.assertEqual(res.data["id"], prev_id)
        self.assertEqual(res.data["subject"], data["subject"])
        self.assertEqual(res.data["description"], prev_desc)

        # Check database object
        incident.refresh_from_db()

        self.assertEqual(incident.id, prev_id)
        self.assertEqual(incident.user, self.user)
        self.assertEqual(incident.subject, data["subject"])
        self.assertEqual(incident.description, prev_desc)

    def test_update_incident_user_no_success(self):
        """Test updating the user of an incident, which is not allowed."""
        # Create incident
        incident = Incident.objects.create(
            user=self.user, subject="Incident", description="Description"
        )

        # Make request
        url = get_incident_detail_url(incident.id)
        data = {"user": self.other_user.id}
        res = self.client.patch(url, data)

        # Check response
        self.assertEqual(res.status_code, HTTP_200_OK)

        # Check database object (the user should still be "self.user")
        incident.refresh_from_db()
        self.assertEqual(incident.user, self.user)

    def test_delete_incident(self):
        """Test deleting an incident."""
        pass
