from django.urls import path

from ui.views import home, incident, create, login, logout


app_name = "ui"

urlpatterns = [
    path("", home, name="home"),
    path("incident/<int:id>/", incident, name="incident"),
    path("create/", create, name="create"),
    path("login/", login, name="login"),
    path("logout/", logout, name="logout")
]
