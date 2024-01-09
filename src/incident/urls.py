"""OpenReq - Incident - URLs."""

from django.urls import path

from incident.views import (
    GetCategoryView, GetOpenIncidentsView, GetClosedIncidentsView,
    GetOpenOpenedByUserIncidentsView, GetOpenAssignedToUserIncidentsView,
    CreateIncidentView, GetUpdateIncidentView
)


app_name = "incident"

urlpatterns = [
    path("category/<int:pk>/", GetCategoryView.as_view(), name="category"),
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
    path("incident/<int:id>/", GetUpdateIncidentView.as_view(), name="get-update")
]
