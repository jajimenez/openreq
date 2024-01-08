"""OpenReq - User - Views."""

from django.contrib.auth import get_user_model

from rest_framework.generics import RetrieveAPIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from user.serializers import UserSerializer


class GetUserView(RetrieveAPIView):
    """Get a user."""

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    serializer_class = UserSerializer
    queryset = get_user_model().objects.all()


class GetAuthUserView(RetrieveAPIView):
    """Get the authenticated user."""

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    serializer_class = UserSerializer

    def get_object(self):
        """Get the authenticated user."""
        return self.request.user
