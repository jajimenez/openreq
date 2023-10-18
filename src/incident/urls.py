"""OpenReq - Incident - URLs."""

from django.urls import path

from incident.views import (
    GetOpenIncidentsView, GetClosedIncidentsView,
    GetOpenOpenedByUserIncidentsView, GetOpenAssignedToUserIncidentsView,
    CreateIncidentView, GetUpdateIncidentView
)


app_name = "incident"

urlpatterns = [
    path("open/", GetOpenIncidentsView.as_view(), name="open"),
    path("closed/", GetClosedIncidentsView.as_view(), name="closed"),
    path(
        "open-opened-by-user/",
        GetOpenOpenedByUserIncidentsView.as_view(),
        name="opened-by-user"
    ),
    path(
        "open-assigned-to-user/",
        GetOpenAssignedToUserIncidentsView.as_view(),
        name="assigned-to-user"
    ),
    path("incident/", CreateIncidentView.as_view(), name="create"),
    path("incident/<id>/", GetUpdateIncidentView.as_view(), name="get-update")
]
