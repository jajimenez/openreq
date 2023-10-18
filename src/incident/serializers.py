"""OpenReq - Incident - Serializers."""

from rest_framework.serializers import ModelSerializer

from core.models import Incident


class ExistingIncidentSerializer(ModelSerializer):
    """Summarized existing Incident objects serializer."""

    class Meta:
        """Model data."""

        model = Incident

        fields = [
            "id", "opened_by", "subject", "tags", "assigned_to", "closed"
        ]

        read_only_fields = ["id", "opened_by", "subject"]


class ExistingIncidentDetailSerializer(ExistingIncidentSerializer):
    """Detailed existing Incident objects serializer."""

    class Meta(ExistingIncidentSerializer.Meta):
        """Model data."""

        fields = [
            "id", "opened_by", "subject", "description", "tags", "assigned_to",
            "closed"
        ]

        read_only_fields = \
            ExistingIncidentSerializer.Meta.read_only_fields + ["description"]


class NewIncidentDetailSerializer(ModelSerializer):
    """Detailed new Incident objects serializer."""

    class Meta:
        """Model data."""

        model = Incident

        fields = [
            "id", "opened_by", "subject", "description", "tags", "assigned_to",
            "closed"
        ]

        read_only_fields = ["id", "opened_by", "tags", "assigned_to", "closed"]
