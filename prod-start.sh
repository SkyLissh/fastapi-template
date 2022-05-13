#!/usr/env/bin bash

set -o errexit
set -o nounset

alembic upgrade head
gunicorn --bind 0.0.0.0:5000 app.main:app -k uvicorn.workers.UvicornWorker
