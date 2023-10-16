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
        for i in range(1, 4):
            Incident.objects.create(
                user=self.user,
                subject=f"Incident {i}",
                description=f"Description {i}"
            )

        res = self.client.get(INCIDENT_LIST_URL)
        self.assertEqual(res.status_code, HTTP_200_OK)

        incidents = Incident.objects.filter(user=self.user).order_by("-id")
        ser = IncidentSerializer(incidents, many=True)
        self.assertEqual(res.data, ser.data)

    def test_get_incident(self):
        """Test getting an incident."""
        i = Incident.objects.create(
            user=self.user, subject="Incident", description="Description"
        )

        url = get_incident_detail_url(i.id)
        res = self.client.get(url)
        self.assertEqual(res.status_code, HTTP_200_OK)

        ser = IncidentDetailSerializer(i)
        self.assertEqual(res.data, ser.data)

    def test_create_incident(self):
        """Test creating a incident."""
        data = {"subject": "Incident", "description": "Description"}
        res = self.client.post(INCIDENT_URL, data)

        self.assertEqual(res.status_code, HTTP_201_CREATED)
        self.assertEqual(len(res.data), 3)
        self.assertIn("id", res.data)

        incident = Incident.objects.get(id=res.data["id"])

        for k, v in data.items():
            # Check response
            self.assertIn(k, res.data)
            self.assertEqual(res.data[k], v)

            # Check database object
            self.assertEqual(getattr(incident, k), v)

        self.assertEqual(incident.user, self.user)

    def test_update_incident(self):
        """Test updating an incident."""
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

        for i in ("id", "subject", "description"):
            self.assertIn(i, res.data)

        self.assertNotIn("user", res.data)

        self.assertEqual(res.data["id"], prev_id)
        self.assertEqual(res.data["subject"], data["subject"])
        self.assertEqual(res.data["description"], data["description"])

        # Check database object
        incident.refresh_from_db()

        self.assertEqual(incident.id, prev_id)
        self.assertEqual(incident.user, self.user)
        self.assertEqual(incident.subject, data["subject"])
        self.assertEqual(incident.description, data["description"])

    def test_partial_update_incident(self):
        """Test updating an incident partially."""
        prev_sub = "Incident"
        prev_desc = "Incident description."

        incident = Incident.objects.create(
            user=self.user, subject=prev_sub, description=prev_desc
        )

        prev_id = incident.id

        # Make request
        url = get_incident_detail_url(incident.id)
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
