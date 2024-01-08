"""OpenReq - Incident - Serializers."""

from rest_framework.serializers import ModelSerializer

from core.models import Category, Incident


class CategorySerializer(ModelSerializer):
    """Category objects serializer."""

    class Meta:
        """Model data."""

        model = Category
        fields = ["name"]
        read_only_fields = ["name"]


class ExistingIncidentSerializer(ModelSerializer):
    """Summarized existing Incident objects serializer."""

    class Meta:
        """Model data."""

        model = Incident

        fields = [
            "id", "opened_by", "category", "subject", "assigned_to", "closed"
        ]

        read_only_fields = ["id", "opened_by", "subject"]


class ExistingIncidentDetailSerializer(ExistingIncidentSerializer):
    """Detailed existing Incident objects serializer."""

    class Meta(ExistingIncidentSerializer.Meta):
        """Model data."""

        fields = [
            "id", "opened_by", "category", "subject", "description",
            "assigned_to", "closed"
        ]

        read_only_fields = \
            ExistingIncidentSerializer.Meta.read_only_fields + ["description"]


class NewIncidentDetailSerializer(ModelSerializer):
    """Detailed new Incident objects serializer."""

    class Meta:
        """Model data."""

        model = Incident

        fields = [
            "id", "opened_by", "category", "subject", "description",
            "assigned_to", "closed"
        ]

        read_only_fields = [
            "id", "opened_by", "category", "assigned_to", "closed"
        ]
