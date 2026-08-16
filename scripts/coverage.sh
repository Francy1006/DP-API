#!/bin/sh

set -eu

DP_API_ROOT="$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)"
ENV_FILE="${ENV_FILE:-.env.dev}"

cd "$DP_API_ROOT"

if [ ! -f "$ENV_FILE" ]; then
  echo "No existe $ENV_FILE"
  exit 1
fi

rm -f coverage.xml

docker compose --env-file "$ENV_FILE" run \
  --rm \
  --no-deps \
  --entrypoint sh \
  -v "$DP_API_ROOT:/qa-output" \
  api \
  -lc 'pytest products/tests/ \
    --cov=products \
    --cov-branch \
    --cov-config=.coveragerc \
    --cov-report=term-missing \
    --cov-report=xml:/qa-output/coverage.xml'

if [ ! -f coverage.xml ]; then
  echo "ERROR: No se generó coverage.xml"
  exit 1
fi

echo "Coverage generado usando $ENV_FILE"
