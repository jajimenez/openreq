"""User API URLs."""

from django.urls import path

from user.views import GetAuthUserView


app_name = "user"

urlpatterns = [
    path("me/", GetAuthUserView.as_view(), name="me")
]
