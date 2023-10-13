"""User API views."""

from rest_framework.generics import RetrieveAPIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from user.serializers import UserSerializer


class GetAuthUserView(RetrieveAPIView):
    """View for getting the authenticated user."""

    serializer_class = UserSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_object(self):
        """Get the authenticated user."""
        return self.request.user
