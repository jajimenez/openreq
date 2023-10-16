"""OpenReq - Incident - Serializers."""

from rest_framework.serializers import ModelSerializer

from core.models import Incident


class IncidentSerializer(ModelSerializer):
    """Summarized Incident objects serializer."""

    class Meta:
        model = Incident
        fields = ["id", "title"]
        read_only_fields = ["id"]


class IncidentDetailSerializer(IncidentSerializer):
    """Detailed Incident objects serializer."""

    class Meta(IncidentSerializer.Meta):
        fields = IncidentSerializer.Meta.fields + ["description"]
