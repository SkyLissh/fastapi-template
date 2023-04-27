FROM python:3.11.2-slim as python-base

ENV POETRY_VERSION=1.4.0 \
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
  VENV_PATH="/opt/pysetup/.venv" \
  # Dockerize version
  DOCKERIZE_VERSION="v0.6.1" \
  # Tini for Docker
  TINI_VERSION="v0.19.0"


ENV PATH="$POETRY_HOME/bin:$VENV_PATH/bin:$PATH"


# === Builder Image ===
FROM python-base as builder
# System packages
RUN apt update && apt upgrade -y && apt install --no-install-recommends -y \
  build-essential \
  curl \
  wget

# Poetry installation
RUN curl -sSL "https://install.python-poetry.org" | python -

WORKDIR $PYSETUP_PATH
COPY ./poetry.lock ./pyproject.toml ./

RUN poetry install --no-dev

# Dockerize Installation
RUN wget "https://github.com/jwilder/dockerize/releases/download/${DOCKERIZE_VERSION}/dockerize-linux-amd64-${DOCKERIZE_VERSION}.tar.gz" \
  && tar -C /usr/local/bin -xzf "dockerize-linux-amd64-${DOCKERIZE_VERSION}.tar.gz" \
  && rm "dockerize-linux-amd64-${DOCKERIZE_VERSION}.tar.gz" \
  && dockerize --version

# Tini Installation
RUN wget -O /usr/local/bin/tini "https://github.com/krallin/tini/releases/download/${TINI_VERSION}/tini" \
  && chmod +x /usr/local/bin/tini \
  && tini --version


# === Base Image ===
FROM python-base as base

COPY --from=builder $PYSETUP_PATH $PYSETUP_PATH

COPY --from=builder /usr/local/bin/dockerize /usr/local/bin/dockerize
COPY --from=builder /usr/local/bin/tini /usr/local/bin/tini

COPY ./scripts/entrypoint.sh /docker-entrypoint.sh
RUN chmod +x /docker-entrypoint.sh


# === Development Image ===
FROM base as development

COPY --from=builder $POETRY_HOME $POETRY_HOME

WORKDIR $PYSETUP_PATH
RUN poetry install

WORKDIR /{{ cookiecutter.project_slug }}

ENTRYPOINT [ "tini", "--", "/docker-entrypoint.sh" ]


# === Production Image ===
FROM base as production

WORKDIR /{{ cookiecutter.project_slug }}

# Setup Permissions
RUN groupadd -r fastapi && useradd -d /fastapi -r -g fastapi fastapi \
  && chown fastapi:fastapi -R /{{ cookiecutter.project_slug }}

COPY --chown=fastapi:fastapi . /{{ cookiecutter.project_slug }}/

USER fastapi

ENTRYPOINT [ "tini", "--", "/docker-entrypoint.sh" ]

CMD [ "sh", "./scripts/start-prod.sh" ]
