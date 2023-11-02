FROM mcr.microsoft.com/devcontainers/python:1-3.11-bullseye

ENV PYTHONUNBUFFERED 1

COPY requirements.txt /tmp/pip-tmp/
COPY requirements-dev.txt /tmp/pip-tmp/

# Install needed tools for compiling the Psycopg2 Python package, delete
# temporary APT files, install the project Python dependencies and download the
# language model
RUN apt-get update && \
    apt-get install -y build-essential python3-dev libpq-dev && \
    rm -rf /var/lib/apt/lists/* && \
    python -m pip --no-cache-dir install --upgrade pip && \
    pip --no-cache-dir install -r /tmp/pip-tmp/requirements.txt && \
    pip --no-cache-dir install -r /tmp/pip-tmp/requirements-dev.txt && \
    rm -rf /tmp/pip-tmp && \
    python -m spacy download en_core_web_sm
