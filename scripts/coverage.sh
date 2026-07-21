#!/bin/sh

set -e

ENV_FILE=".env.dev"

if [ ! -f "$ENV_FILE" ]; then
  echo "No existe $ENV_FILE"
  exit 1
fi

set -a
. "./$ENV_FILE"
set +a

ENV_FILE="${ENV_FILE:-.env.dev}"

docker compose --env-file "$ENV_FILE" exec api pytest products/tests/ \
  --cov=products \
  --cov-branch \
  --cov-config=.coveragerc \
  --cov-report=term-missing \
  --cov-report=xml:coverage.xml

docker cp dp-core:/usr/src/app/coverage.xml ./coverage.xml

echo "Coverage generado usando $ENV_FILE"