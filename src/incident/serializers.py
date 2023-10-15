"""OpenReq - Incident - Serializers."""

from rest_framework.serializers import ModelSerializer

from core.models import Incident


class IncidentSerializer(ModelSerializer):
    """Incident objects serializer."""

    class Meta:
        model = Incident
        fields = ["description"]
        read_only_fields = ["id"]
