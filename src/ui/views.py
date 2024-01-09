from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.decorators.http import require_http_methods

import requests


# Views
LOGIN_VIEW = "ui:login"
HOME_VIEW = "ui:home"
INCIDENT_DETAIL_VIEW = "ui:incident"
CREATE_INCIDENT_VIEW = "ui:create"

# Templates
LOGIN_TEMPLATE = "ui/login.html"
HOME_TEMPLATE = "ui/home.html"
INCIDENT_DETAIL_TEMPLATE = "ui/incident.html"
CREATE_INCIDENT_TEMPLATE = "ui/create.html"

# OpenReq API
API_URL = "http://localhost:8000/api/"
AUTH_API_URL = f"{API_URL}auth/"
OPEN_INCIDENTS_API_URL = f"{API_URL}incident/open/"
INCIDENT_API_URL = f"{API_URL}incident/incident/"


@require_http_methods(["GET", "POST"])
def login(request: HttpRequest) -> HttpResponse:
    """Login view.

    :param request: HTTP request
    :type request: HttpRequest
    :return: HTTP response
    :rtype: HttpResponse
    """
    next_url = request.GET.get("next") or reverse(HOME_VIEW)

    # If the request method is GET, we render the login form if we don't have
    # an authentication token stored. Otherwise, we redirect the user to the
    # Next URL.
    if request.method == "GET":
        if "token" in request.session:
            return redirect(next_url)
        else:
            context = {"next_url": next_url}
            return render(request, LOGIN_TEMPLATE, context)

    # If the request method is POST, we try to authenticate the user with the
    # credentials provided. If the authentication is successful, we store the
    # authentication token and redirect them to the Next URL. Otherwise, we
    # render the login form with an error message.
    try:
        username = request.POST["username"]
        password = request.POST["password"]

        # Get authentication token
        data = {"username": username, "password": password}
        req = requests.post(AUTH_API_URL, data=data)

        if req.status_code != 200:
            raise Exception

        token = req.json()["token"]

        # Store username and token in session
        request.session["username"] = username
        request.session["token"] = token
    except Exception:
        # Return error message
        context = {"next_url": next_url, "error": "Error authenticating."}
        return render(request, LOGIN_TEMPLATE, context)

    # Redirect to the Next view
    return redirect(next_url)


@require_http_methods(["GET"])
def logout(request: HttpRequest) -> HttpResponse:
    """Logout view.

    :param request: HTTP request
    :type request: HttpRequest
    :return: HTTP response
    :rtype: HttpResponse
    """
    # Remove username and token from session
    if "username" in request.session:
        del request.session["username"]

    if "token" in request.session:
        del request.session["token"]

    # Redirect to the Home view
    return redirect(HOME_VIEW)


@require_http_methods(["GET"])
def home(request: HttpRequest) -> HttpResponse:
    """Home view.

    This view returns the incidents opened by the user.

    :param request: HTTP request
    :type request: HttpRequest
    :return: HTTP response
    :rtype: HttpResponse
    """
    # Check if we have the authentication token in the session
    if "token" not in request.session:
        # Redirect to the Login view
        home_url = reverse(HOME_VIEW)
        login_url = reverse(LOGIN_VIEW)
        login_url = f"{login_url}?next={home_url}"

        return redirect(login_url)

    context = {"username": request.session["username"]}
    token = request.session["token"]

    try:
        # Get incidents
        headers = {"AUTHORIZATION": f"Token {token}"}
        req = requests.get(OPEN_INCIDENTS_API_URL, headers=headers)

        if req.status_code != 200:
            raise Exception

        incidents = req.json()

        # Get the category name and the name of the assigned user of each
        # incident.
        for i in incidents:
            category_id = i["category"]
            assigned_to_id = i["assigned_to"]

            if category_id is not None:
                url = f"{API_URL}incident/category/{category_id}/"
                req = requests.get(url, headers=headers)

                if req.status_code != 200:
                    raise Exception

                i["category"] = req.json()["name"]

            if assigned_to_id is not None:
                url = f"{API_URL}user/user/{assigned_to_id}/"
                req = requests.get(url, headers=headers)

                if req.status_code != 200:
                    raise Exception

                i["assigned_to"] = req.json()["username"]

        context["incidents"] = incidents
    except Exception:
        context["error"] = "Error getting the incidents."

    return render(request, HOME_TEMPLATE, context=context)


@require_http_methods(["GET"])
def incident(request: HttpRequest, id: int) -> HttpResponse:
    """Incident detail view.

    This view returns the incidents opened by the user.

    :param request: HTTP request
    :type request: HttpRequest
    :param id: Incident ID
    :type id: int
    :return: HTTP response
    :rtype: HttpResponse
    """
    # Check if we have the authentication token in the session
    if "token" not in request.session:
        # Redirect to the Login view
        incident_url = reverse(INCIDENT_DETAIL_VIEW)
        login_url = reverse(LOGIN_VIEW)
        login_url = f"{login_url}?next={incident_url}"

        return redirect(login_url)

    context = {"username": request.session["username"]}
    token = request.session["token"]

    try:
        # Get incident
        url = f"{INCIDENT_API_URL}{id}/"
        headers = {"AUTHORIZATION": f"Token {token}"}
        req = requests.get(url, headers=headers)

        if req.status_code != 200:
            raise Exception

        incident = req.json()

        # Get the category name and the name of the assigned user of the
        # incident.
        category_id = incident["category"]
        assigned_to_id = incident["assigned_to"]

        if category_id is not None:
            url = f"{API_URL}incident/category/{category_id}/"
            req = requests.get(url, headers=headers)

            if req.status_code != 200:
                raise Exception

            incident["category"] = req.json()["name"]

        if assigned_to_id is not None:
            url = f"{API_URL}user/user/{assigned_to_id}/"
            req = requests.get(url, headers=headers)

            if req.status_code != 200:
                raise Exception

            incident["assigned_to"] = req.json()["username"]

        context["incident"] = incident
    except Exception:
        context["error"] = "Error getting the incident."

    return render(request, INCIDENT_DETAIL_TEMPLATE, context=context)


@require_http_methods(["GET", "POST"])
def create(request: HttpRequest) -> HttpResponse:
    """Create view.

    This view creates a new incident.

    :param request: HTTP request
    :type request: HttpRequest
    :return: HTTP response
    :rtype: HttpResponse
    """
    # Check if we have the authentication token in the session
    if "token" not in request.session:
        # Redirect to the Login view
        create_url = reverse(CREATE_INCIDENT_VIEW)
        login_url = reverse(LOGIN_VIEW)
        login_url = f"{login_url}?next={create_url}"

        return redirect(login_url)

    context = {"username": request.session["username"]}

    # If the request method is GET, we render the create form
    if request.method == "GET":
        return render(request, "ui/create.html", context=context)

    # If the request method is POST, we try to create the incident
    token = request.session["token"]

    try:
        # Create incident
        headers = {"AUTHORIZATION": f"Token {token}"}

        data = {
            "subject": request.POST.get("subject"),
            "description": request.POST.get("description")
        }

        req = requests.post(INCIDENT_API_URL, headers=headers, data=data)

        if req.status_code != 201:
            raise Exception
    except Exception:
        context["error"] = "Error creating the incident."
        return render(request, CREATE_INCIDENT_TEMPLATE, context=context)

    # Redirect to the Home view
    return redirect(HOME_VIEW)
