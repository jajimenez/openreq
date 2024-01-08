"""OpenReq - User - URLs."""

from django.urls import path

from user.views import GetUserView, GetAuthUserView


app_name = "user"

urlpatterns = [
    path("user/<int:pk>/", GetUserView.as_view(), name="user"),
    path("me/", GetAuthUserView.as_view(), name="me")
]
