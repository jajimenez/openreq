"""OpenReq - Incident - Views."""

from rest_framework.generics import (
    ListAPIView, CreateAPIView, RetrieveUpdateAPIView
)
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import (
    BasePermission, SAFE_METHODS, IsAuthenticated
)

from core.models import Incident
from incident.serializers import (
    NewIncidentDetailSerializer, ExistingIncidentSerializer,
    ExistingIncidentDetailSerializer
)


class IsStaffOrAssigned(BasePermission):
    """Permission to only allow staff users and the assigned user to update an
    incident.
    """

    def has_object_permission(self, request, view, obj):
        """Get whether a user has permissions to get or update an incident."""
        # Read permission is allowed to any request
        if request.method in SAFE_METHODS:
            return True

        # Write permission is allowed to any staff user and the assigned user
        return request.user.is_staff or request.user == obj.assigned_to


class GetOpenIncidentsView(ListAPIView):
    """Get open incidents."""

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = Incident.objects.filter(closed=False)
    serializer_class = ExistingIncidentSerializer


class GetClosedIncidentsView(ListAPIView):
    """Get closed incidents."""

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = Incident.objects.filter(closed=True)
    serializer_class = ExistingIncidentSerializer


class GetOpenOpenedByUserIncidentsView(ListAPIView):
    """Get open incidents opened by the authenticated user."""

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    serializer_class = ExistingIncidentSerializer

    def get_queryset(self):
        """Get the list of incidents."""
        return Incident.objects.filter(
            opened_by=self.request.user, closed=False
        )


class GetOpenAssignedToUserIncidentsView(ListAPIView):
    """Get open incidents assigned to the authenticated user."""

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    serializer_class = ExistingIncidentSerializer

    def get_queryset(self):
        """Get the list of incidents."""
        return Incident.objects.filter(
            assigned_to=self.request.user, closed=False
        )


class CreateIncidentView(CreateAPIView):
    """Create an incident."""

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    serializer_class = NewIncidentDetailSerializer

    def perform_create(self, serializer):
        """Create an incident."""
        return serializer.save(opened_by=self.request.user)


class GetUpdateIncidentView(RetrieveUpdateAPIView):
    """Get, fully update or partially update an incident.

    Updating an incident is only allowed to staff users and the assigned user.
    The `id` and `opened_by` fields can't be updated.
    """

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsStaffOrAssigned]

    serializer_class = ExistingIncidentDetailSerializer
    queryset = Incident.objects.all()
    lookup_field = "id"
