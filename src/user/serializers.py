"""OpenReq - User - Serializers."""

from django.contrib.auth import get_user_model

from rest_framework.serializers import ModelSerializer


class UserSerializer(ModelSerializer):
    """User objects serializer."""

    class Meta:
        model = get_user_model()
        fields = ["username", "first_name", "last_name", "email"]
        extra_fields = {"password": {"write_only": True, "min_lengh": 8}}
