"""OpenReq - Incident - Tests."""

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework.status import (
    HTTP_200_OK, HTTP_201_CREATED, HTTP_401_UNAUTHORIZED, HTTP_403_FORBIDDEN,
    HTTP_404_NOT_FOUND, HTTP_405_METHOD_NOT_ALLOWED
)

from core.models import Tag, Incident
from incident.serializers import (
    ExistingIncidentSerializer, ExistingIncidentDetailSerializer
)


OPEN_INCIDENTS_URL = reverse("incident:open")
CLOSED_INCIDENTS_URL = reverse("incident:closed")
INCIDENTS_OPENED_BY_USER_URL = reverse("incident:opened-by-user")
INCIDENTS_ASSIGNED_TO_USER_URL = reverse("incident:assigned-to-user")
CREATE_INCIDENT_URL = reverse("incident:create")


def get_get_update_url(incident_id):
    """Get the Get-Update URL of an incident."""
    return reverse("incident:get-update", args=[incident_id])


class PublicIncidentApiTests(TestCase):
    """Incident API unauthenticated tests."""

    def setUp(self):
        """Initialize each test."""
        self.client = APIClient()

    def test_get_open_incidents_unauthenticated(self):
        """Test getting the open incidents without authentication."""
        res = self.client.get(OPEN_INCIDENTS_URL)
        self.assertEqual(res.status_code, HTTP_401_UNAUTHORIZED)

    def test_get_closed_incidents_unauthenticated(self):
        """Test getting the closed incidents without authentication."""
        res = self.client.get(CLOSED_INCIDENTS_URL)
        self.assertEqual(res.status_code, HTTP_401_UNAUTHORIZED)


class PrivateIncidentApiTests(TestCase):
    """Incident API authenticated tests."""

    def setUp(self):
        """Initialize each test."""
        self.client = APIClient()
        model = get_user_model()

        self.user_1 = model.objects.create_user(
            username="user_1", password="password", is_staff=True
        )

        self.user_2 = model.objects.create_user(
            username="user_2", password="password"
        )

        self.client.force_authenticate(self.user_1)

    def test_get_open_incidents(self):
        """Test getting the open incidents."""
        # Create objects
        for i in range(1, 4):
            Incident.objects.create(
                opened_by=self.user_1,
                subject=f"Incident {i}",
                description=f"Description {i}"
            )

        # Make request
        res = self.client.get(OPEN_INCIDENTS_URL)

        # Check response
        self.assertEqual(res.status_code, HTTP_200_OK)

        incidents = Incident.objects.all().order_by("id")
        ser = ExistingIncidentSerializer(incidents, many=True)
        self.assertEqual(res.data, ser.data)

    def test_get_closed_incidents(self):
        """Test getting the closed incidents."""
        # Create objects
        for i in range(1, 4):
            Incident.objects.create(
                opened_by=self.user_1,
                subject=f"Incident {i}",
                description=f"Description {i}",
                closed=True
            )

        # Make request
        res = self.client.get(CLOSED_INCIDENTS_URL)

        # Check response
        self.assertEqual(res.status_code, HTTP_200_OK)

        incidents = Incident.objects.all().order_by("id")
        ser = ExistingIncidentSerializer(incidents, many=True)
        self.assertEqual(res.data, ser.data)

    def test_get_open_incidents_opened_by_user(self):
        """Test getting the open incidents opened by the user."""
        # Create objects
        for i in range(1, 4):
            Incident.objects.create(
                opened_by=self.user_1,
                subject=f"Incident {i}",
                description=f"Description {i}"
            )

        # Make request
        res = self.client.get(INCIDENTS_OPENED_BY_USER_URL)

        # Check response
        self.assertEqual(res.status_code, HTTP_200_OK)

        incidents = \
            Incident.objects.filter(opened_by=self.user_1).order_by("id")

        ser = ExistingIncidentSerializer(incidents, many=True)
        self.assertEqual(res.data, ser.data)

    def test_get_open_incidents_assigned_to_user(self):
        """Test getting the open incidents assigned to the user."""
        # Create objects
        for i in range(1, 4):
            Incident.objects.create(
                opened_by=self.user_2,
                subject=f"Incident {i}",
                description=f"Description {i}",
                assigned_to=self.user_1
            )

        # Make request
        res = self.client.get(INCIDENTS_ASSIGNED_TO_USER_URL)

        # Check response
        self.assertEqual(res.status_code, HTTP_200_OK)

        incidents = \
            Incident.objects.filter(assigned_to=self.user_1).order_by("id")

        ser = ExistingIncidentSerializer(incidents, many=True)
        self.assertEqual(res.data, ser.data)

    def test_get_incident(self):
        """Test getting an incident."""
        # Create object
        i = Incident.objects.create(
            opened_by=self.user_1,
            subject="Incident",
            description="Description"
        )

        # Make request
        url = get_get_update_url(i.id)
        res = self.client.get(url)

        # Check response
        self.assertEqual(res.status_code, HTTP_200_OK)

        ser = ExistingIncidentDetailSerializer(i)
        self.assertEqual(res.data, ser.data)

    def test_get_non_existing_incident(self):
        """Test getting an non-existing incident."""
        # Make request
        url = get_get_update_url(1)
        res = self.client.get(url)

        # Check response
        self.assertEqual(res.status_code, HTTP_404_NOT_FOUND)

    def test_create_incident(self):
        """Test creating a incident."""
        # Make request
        data = {"subject": "Incident", "description": "Description"}
        res = self.client.post(CREATE_INCIDENT_URL, data)

        # Check response
        self.assertEqual(res.status_code, HTTP_201_CREATED)
        self.assertEqual(len(res.data), 7)

        for i in (
            "id", "opened_by", "subject", "description", "tags", "assigned_to",
            "closed"
        ):
            self.assertIn(i, res.data)

        self.assertIsNotNone(res.data["id"])
        self.assertEqual(res.data["opened_by"], self.user_1.id)
        self.assertEqual(res.data["subject"], data["subject"])
        self.assertEqual(res.data["description"], data["description"])
        self.assertEqual(len(res.data["tags"]), 0)
        self.assertIsNone(res.data["assigned_to"])
        self.assertFalse(res.data["closed"])

        # Check database object
        incident = Incident.objects.get(id=res.data["id"])

        self.assertIsNotNone(incident.id)
        self.assertEqual(incident.opened_by, self.user_1)
        self.assertEqual(incident.subject, data["subject"])
        self.assertEqual(incident.description, data["description"])
        self.assertEqual(incident.tags.count(), 0)
        self.assertIsNone(incident.assigned_to)
        self.assertFalse(incident.closed)

    def test_full_update_incident_staff(self):
        """Test updating an incident fully by a staff user."""
        # Create incident
        sub = "Incident"
        desc = "Incident description."

        incident = Incident.objects.create(
            opened_by=self.user_2, subject=sub, description=desc
        )

        _id = incident.id

        # Make request
        url = get_get_update_url(_id)
        data = {"assigned_to": self.user_1.id, "closed": True}
        res = self.client.put(url, data)

        # Check response
        self.assertEqual(res.status_code, HTTP_200_OK)
        self.assertEqual(len(res.data), 7)

        for i in (
            "id", "opened_by", "subject", "description", "tags", "assigned_to",
            "closed"
        ):
            self.assertIn(i, res.data)

        self.assertEqual(res.data["id"], _id)
        self.assertEqual(res.data["opened_by"], self.user_2.id)
        self.assertEqual(res.data["subject"], sub)
        self.assertEqual(res.data["description"], desc)
        self.assertEqual(len(res.data["tags"]), 0)
        self.assertEqual(res.data["assigned_to"], self.user_1.id)
        self.assertTrue(res.data["closed"])

        # Check database object
        incident.refresh_from_db()

        self.assertEqual(incident.id, _id)
        self.assertEqual(incident.opened_by, self.user_2)
        self.assertEqual(incident.subject, sub)
        self.assertEqual(incident.description, desc)
        self.assertEqual(incident.tags.count(), 0)
        self.assertEqual(incident.assigned_to, self.user_1)
        self.assertTrue(incident.closed)

    def test_partial_update_incident_staff(self):
        """Test updating an incident partially by a staff user."""
        # Create incident
        sub = "Incident"
        desc = "Incident description."

        incident = Incident.objects.create(
            opened_by=self.user_2, subject=sub, description=desc
        )

        _id = incident.id

        # Make request
        url = get_get_update_url(_id)
        data = {"assigned_to": self.user_1.id}
        res = self.client.patch(url, data)

        # Check response
        self.assertEqual(res.status_code, HTTP_200_OK)
        self.assertEqual(len(res.data), 7)

        for i in (
            "id", "opened_by", "subject", "description", "tags", "assigned_to",
            "closed"
        ):
            self.assertIn(i, res.data)

        self.assertEqual(res.data["id"], _id)
        self.assertEqual(res.data["opened_by"], self.user_2.id)
        self.assertEqual(res.data["subject"], sub)
        self.assertEqual(res.data["description"], desc)
        self.assertEqual(len(res.data["tags"]), 0)
        self.assertEqual(res.data["assigned_to"], self.user_1.id)
        self.assertFalse(res.data["closed"])

        # Check database object
        incident.refresh_from_db()

        self.assertEqual(incident.id, _id)
        self.assertEqual(incident.opened_by, self.user_2)
        self.assertEqual(incident.subject, sub)
        self.assertEqual(incident.description, desc)
        self.assertEqual(incident.tags.count(), 0)
        self.assertEqual(incident.assigned_to, self.user_1)
        self.assertFalse(incident.closed)

    def test_update_incident_non_staff(self):
        """Test updating an incident by a non-staff user, which is not allowed.
        """
        # Login as a non-staff user (User 2)
        self.client.force_authenticate(self.user_2)

        # Create incident
        incident = Incident.objects.create(
            opened_by=self.user_1,
            subject="Incident",
            description="Description"
        )

        # Make request
        url = get_get_update_url(incident.id)
        data = {"closed": True}
        res = self.client.patch(url, data)

        # Check response
        self.assertEqual(res.status_code, HTTP_403_FORBIDDEN)

        # Check database object ("closed" should still be False, the default
        # value).
        incident.refresh_from_db()
        self.assertEqual(incident.closed, False)

    def test_update_incident_not_allowed_fields(self):
        """Test updating the `id`, `opened_by`, `subject` and `description`
        fields of an incident, which is not allowed."""
        # Create incident
        sub = "Incident"
        desc = "Description"

        incident = Incident.objects.create(
            opened_by=self.user_1, subject=sub, description=desc
        )

        prev_id = incident.id

        # Make request
        url = get_get_update_url(incident.id)
        data = {"id": 1234}
        res = self.client.patch(url, data)

        # Check response
        self.assertEqual(res.status_code, HTTP_200_OK)

        # Check database object ("id" should still be "prev_id")
        incident.refresh_from_db()
        self.assertEqual(incident.id, prev_id)

        # Make request
        data = {"opened_by": self.user_2.id}
        res = self.client.patch(url, data)

        # Check response
        self.assertEqual(res.status_code, HTTP_200_OK)

        # Check database object ("opened_by" should still be "self.user_1")
        incident.refresh_from_db()
        self.assertEqual(incident.opened_by, self.user_1)

        # Make request
        data = {"subject": "New Incident"}
        res = self.client.patch(url, data)

        # Check response
        self.assertEqual(res.status_code, HTTP_200_OK)

        # Check database object ("subject" should still be "sub")
        incident.refresh_from_db()
        self.assertEqual(incident.subject, sub)

        # Make request
        data = {"description": "New description"}
        res = self.client.patch(url, data)

        # Check response
        self.assertEqual(res.status_code, HTTP_200_OK)

        # Check database object ("description" should still be "desc")
        incident.refresh_from_db()
        self.assertEqual(incident.description, desc)

    def test_delete_incident(self):
        """Test deleting an incident, which is not allowed.."""
        # Create object
        i = Incident.objects.create(
            opened_by=self.user_1,
            subject="Incident",
            description="Description"
        )

        # Make request
        url = get_get_update_url(i.id)
        res = self.client.delete(url)

        # Check response
        self.assertEqual(res.status_code, HTTP_405_METHOD_NOT_ALLOWED)

        # Check database object
        self.assertTrue(Incident.objects.filter(id=i.id).exists())
