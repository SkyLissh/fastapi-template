#!/usr/env/bin bash

set -o errexit
set -o nounset

export GUNICORN_CONF="./app/core/gunicorn_conf.py"

alembic upgrade head
gunicorn -c $GUNICORN_CONF -k uvicorn.workers.UvicornWorker app.main:app
