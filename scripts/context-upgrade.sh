#!/usr/bin/env bash
set -euo pipefail

DP_API_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
ENV_FILE="${DP_API_ROOT}/.env.dev"

[[ -f "${ENV_FILE}" ]] || {
  echo "ERROR: No existe ${ENV_FILE}"
  exit 1
}

get_env() {
  local key="$1"

  grep -E "^${key}=" "${ENV_FILE}" \
    | tail -n 1 \
    | cut -d '=' -f2- \
    | sed 's/^"//; s/"$//'
}

PROJECT_NAME="$(get_env DOPPLER_PROJECT)"
AI_ASSISTANT_URL="$(get_env AI_ASSISTANT_URL)"

[[ -n "${PROJECT_NAME}" ]] || {
  echo "ERROR: Falta DOPPLER_PROJECT"
  exit 1
}

[[ -n "${AI_ASSISTANT_URL}" ]] || {
  echo "ERROR: Falta AI_ASSISTANT_URL"
  exit 1
}

curl --fail --silent --show-error \
  -X POST "${AI_ASSISTANT_URL}/contexts/upgrade" \
  -H "Content-Type: application/json" \
  -d "{
    \"project_name\":\"${PROJECT_NAME}\",
    \"workflow\":\"context-upgrade\"
  }"

echo
echo "Contextos actualizados correctamente."