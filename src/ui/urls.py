from django.urls import path

from ui.views import home, create, login, logout


app_name = "ui"

urlpatterns = [
    path("", home, name="home"),
    path("create/", create, name="create"),
    path("login/", login, name="login"),
    path("logout/", logout, name="logout")
]
