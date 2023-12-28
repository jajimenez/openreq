from django.urls import path

from ui.views import home, login, logout


app_name = "ui"

urlpatterns = [
    path("", home, name="home"),
    path("login/", login, name="login"),
    path("logout/", logout, name="logout")
]
