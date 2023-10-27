# OpenReq

## Introduction

OpenReq is a REST API for managing project incidents. The API is written in
Python and based on the Django framework.

## Development

The `.devcontainer` directory contains configuration to develop the project in
Visual Studio Code with Docker and a *dev container*. See
[how to share your Git credentials with the *dev container*](https://code.visualstudio.com/remote/advancedcontainers/sharing-git-credentials).

You can run the API locally by running this command from the `src` directory:

```bash
python manage.py runserver
```

To run the unit tests:

```bash
python manage.py test
```

## Management

Once the API is running, you can browse to the administration site in `/admin`.
To train the incident classification model, run:

```bash
python manage.py train_classification_model
```
