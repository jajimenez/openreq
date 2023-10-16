"""OpenReq - Incident - Tests."""

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework.status import HTTP_200_OK, HTTP_401_UNAUTHORIZED

from core.models import Incident
from incident.serializers import IncidentSerializer, IncidentDetailSerializer


# "incident-list" is defined in the "rest_framework.routers.DefaultRouter"
# class.
INCIDENT_LIST_URL = reverse("incident:incident-list")


def get_incident_url(incident_id):
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
                description=f"Incident {i} detail"
            )

        res = self.client.get(INCIDENT_LIST_URL)

        incidents = Incident.objects.filter(user=self.user).order_by("-id")
        ser = IncidentSerializer(incidents, many=True)

        self.assertEqual(res.status_code, HTTP_200_OK)
        self.assertEqual(res.data, ser.data)

    def test_get_incident(self):
        """Test getting an incident."""
        i = Incident.objects.create(
            user=self.user,
            subject="Incident",
            description="Incident detail"
        )

        url = get_incident_url(i.id)
        res = self.client.get(url)
        ser = IncidentDetailSerializer(i)

        self.assertEqual(res.data, ser.data)
