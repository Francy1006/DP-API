#!/bin/sh

docker run --rm \
  --env-file .env.dev \
  -v "$(pwd):/usr/src/app" \
  -v "$(pwd)/.sonar/cache:/opt/sonar-scanner/.sonar/cache" \
  -w /usr/src/app \
  sonarsource/sonar-scanner-cli