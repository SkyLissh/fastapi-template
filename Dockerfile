FROM python:3.9-slim as python-base

ENV POETRY_VERSION=1.1.13 \
  POETRY_NO_INTERACTION=1 \
  POETRY_HOME="/opt/poetry" \
  # Make poetry create virtualenvs in the project root
  POETRY_VIRTUALENVS_IN_PROJECT=true \
  # PIP
  PIP_NO_CACHE_DIR=off \
  PIP_DISABIBLE_PIP_VERSION_CHECK=on \
  PIP_DEFAULT_TIMEOUT=100 \
  # PATHS
  PYSETUP_PATH="/opt/pysetup" \
  VENV_PATH="/opt/pysetup/.venv"


ENV PATH="$POETRY_HOME/bin:$VENV_PATH/bin:$PATH"

FROM python-base as builder
# System packages
RUN apt update && apt upgrade -y && apt install --no-install-recommends -y \
  build-essential \
  curl \
  libpq-dev

# Poetry installation
RUN curl -sSL "https://install.python-poetry.org" | python -

WORKDIR $PYSETUP_PATH
COPY ./poetry.lock ./pyproject.toml ./

RUN poetry install --no-dev

# Development image
FROM python-base as development

WORKDIR $PYSETUP_PATH

COPY --from=builder $POETRY_HOME $POETRY_HOME
COPY --from=builder $PYSETUP_PATH $PYSETUP_PATH

RUN poetry install

WORKDIR /app

# Production image
FROM python-base as production

# RUN mkdir $PYSETUP_PATH
COPY --from=builder $PYSETUP_PATH $PYSETUP_PATH
COPY . /app

WORKDIR /app