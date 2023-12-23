# OpenReq

## Introduction

OpenReq is a REST API for managing project incidents. The API is written in
Python and based on the Django framework.

## Development

The `.devcontainer` directory contains configuration to develop the project in
Visual Studio Code with Docker and a *dev container*. See
[how to share your Git credentials with the *dev container*](https://code.visualstudio.com/remote/advancedcontainers/sharing-git-credentials).

You can run the following Django commands from the `src` directory.

### Apply the migrations

```bash
python manage.py migrate
```

### Run the API

```bash
python manage.py runserver
```

### Run the unit tests

```bash
python manage.py test
```

## Management

Once the API is running, you can browse the following URLs:

- Administration: `/admin`
- API documentation: `/api/docs`

You can run the following Django commands from the `src` directory.

### Train the incident classification model

```bash
python manage.py train_classification_model
```
