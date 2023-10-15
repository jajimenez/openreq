"""OpenReq - Incident - URLs."""

from django.urls import path, include

from rest_framework.routers import DefaultRouter

from incident.views import IncidentViewSet


app_name = "incident"

router = DefaultRouter()
router.register("", IncidentViewSet)

urlpatterns = [
    path("", include(router.urls))
]
