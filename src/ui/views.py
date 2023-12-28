from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth import (
    authenticate, login as _login, logout as _logout
)
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods

from core.models import Incident


# Views
LOGIN_VIEW = "ui:login"
HOME_VIEW = "ui:home"

# Templates
LOGIN_TEMPLATE = "ui/login.html"
HOME_TEMPLATE = "ui/home.html"


@require_http_methods(["GET"])
@login_required(login_url=LOGIN_VIEW)
def home(request: HttpRequest) -> HttpResponse:
    """Home view.

    This view returns the incidents opened by the user.

    :param request: HTTP request
    :type request: HttpRequest
    :return: HTTP response
    :rtype: HttpResponse
    """
    context = {
        "user": request.user,
        "incidents": Incident.objects.filter(opened_by=request.user)
    }

    return render(request, HOME_TEMPLATE, context=context)


@require_http_methods(["GET", "POST"])
def login(request: HttpRequest) -> HttpResponse:
    """Login view.

    :param request: HTTP request
    :type request: HttpRequest
    :return: HTTP response
    :rtype: HttpResponse
    """
    next_url = request.GET.get("next") or reverse(HOME_VIEW)

    # If the request method is GET, we render the login form if the user is not
    # authenticated. Otherwise, we redirect the user to the Next URL.
    if request.method == "GET":
        if request.user.is_authenticated:
            return redirect(next_url)
        else:
            context = {"next_url": next_url}
            return render(request, LOGIN_TEMPLATE, context)

    # If the request method is POST, we try to authenticate the user with the
    # credentials provided. If the authentication is successful, we log in the
    # user and redirect them to the Next URL. Otherwise, we render the login
    # form with an error message.
    username = request.POST.get("username")
    password = request.POST.get("password")

    # Check credentials
    user = authenticate(request, username=username, password=password)

    if user is not None:
        # Log in user
        _login(request, user)

        # Redirect to the Home view
        return redirect(next_url)
    else:
        # Return error message
        context = {
            "next_url": next_url,
            "error": "Invalid username or password"
        }

        return render(request, LOGIN_TEMPLATE, context)


@require_http_methods(["GET"])
def logout(request: HttpRequest) -> HttpResponse:
    """Logout view.

    :param request: HTTP request
    :type request: HttpRequest
    :return: HTTP response
    :rtype: HttpResponse
    """
    # Log out current user
    _logout(request)

    # Redirect to the Home view
    return redirect(HOME_VIEW)
