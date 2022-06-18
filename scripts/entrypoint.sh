#!/usr/bin/env bash

set -o errexit
set -o nounset
set -o pipefail

readonly cmd="$*"

: "${POSTGRES_HOST:=db}"
: "${POSTGRES_PORT:=5432}"

# We need this line to make sure that this container is started
# after the one with postgres.
dockerize \
  -wait "tcp://${POSTGRES_HOST}:${POSTGRES_PORT}" \
  -timeout 90s

# It is also possible to wait for another services as well: redis, eastic, mongo, ...
>&2 echo "Postgres is up - executing command"

# Evaluating passed command (do not touch):
# shellcheck disable=SC2086
exec $cmd
