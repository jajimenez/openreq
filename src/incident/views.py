"""OpenReq - Incident - Views."""

from rest_framework.viewsets import ModelViewSet
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Incident
from incident.serializers import IncidentSerializer, IncidentDetailSerializer


class IncidentViewSet(ModelViewSet):
    """Views for managing the incidents of the user."""

    serializer_class = IncidentDetailSerializer
    queryset = Incident.objects.all()

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Get the incidents of the user."""
        return self.queryset.filter(user=self.request.user).order_by("-id")

    def get_serializer_class(self):
        """Get the serializer class."""
        if self.action == "list":
            return IncidentSerializer

        return self.serializer_class
