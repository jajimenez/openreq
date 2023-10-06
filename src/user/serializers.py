"""User API serializers."""

from django.contrib.auth import get_user_model

from rest_framework.serializers import ModelSerializer


class UserSerializer(ModelSerializer):
    """User objects serializer."""

    class Meta:
        model = get_user_model()
        fields = ["username", "name", "email"]
        extra_fields = {"password": {"write_only": True, "min_lengh": 8}}

    # def create(self, validated_data):
    #     """Create a user object encrypting its password."""
    #     return get_user_model().objects.create_user(**validated_data)
