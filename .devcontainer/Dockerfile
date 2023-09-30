FROM mcr.microsoft.com/devcontainers/python:1-3.11-bullseye

ENV PYTHONUNBUFFERED 1

COPY requirements.txt /tmp/pip-tmp/
COPY requirements-dev.txt /tmp/pip-tmp/

RUN python -m pip --no-cache-dir install --upgrade pip && \
    pip --no-cache-dir install -r /tmp/pip-tmp/requirements.txt && \
    pip --no-cache-dir install -r /tmp/pip-tmp/requirements-dev.txt && \
    rm -rf /tmp/pip-tmp
