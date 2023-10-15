"""OpenReq - Incident - Views."""

from rest_framework.viewsets import ModelViewSet
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Incident
from incident.serializers import IncidentSerializer


class IncidentViewSet(ModelViewSet):
    """Views for managing the incidents of the user."""

    serializer_class = IncidentSerializer
    queryset = Incident.objects.all()

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Get the incidents of the user."""
        return self.queryset.filter(user=self.request.user).order_by("-id")
