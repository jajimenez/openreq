"""User API URLs."""

from django.urls import path
from rest_framework.authtoken.views import ObtainAuthToken


app_name = "user"

urlpatterns = [
    path("token/", ObtainAuthToken.as_view(), name="token")
]
