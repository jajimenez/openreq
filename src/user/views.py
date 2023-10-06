"""User API views."""

from rest_framework.generics import RetrieveAPIView

from user.serializers import UserSerializer


class GetAuthUserView(RetrieveAPIView):
    """View for getting the authenticated user."""

    serializer_class = UserSerializer
