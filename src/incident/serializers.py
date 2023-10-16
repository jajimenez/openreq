"""OpenReq - Incident - Serializers."""

from rest_framework.serializers import ModelSerializer

from core.models import Incident


class IncidentSerializer(ModelSerializer):
    """Summarized Incident objects serializer."""

    class Meta:
        """Model data."""

        model = Incident
        fields = ["id", "subject"]
        read_only_fields = ["id"]


class IncidentDetailSerializer(IncidentSerializer):
    """Detailed Incident objects serializer."""

    class Meta(IncidentSerializer.Meta):
        """Model data."""

        fields = IncidentSerializer.Meta.fields + ["description"]
