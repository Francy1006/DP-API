#!/usr/bin/env bash
set -euo pipefail

DP_API_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SBM_SUITE_ROOT="$(cd "${DP_API_ROOT}/.." && pwd)"
ENV_FILE="${DP_API_ROOT}/.env.dev"

[[ -f "${ENV_FILE}" ]] || {
  echo "ERROR: No existe ${ENV_FILE}"
  exit 1
}

get_env() {
  local key="$1"
  local value

  value="$(
    grep -E "^${key}=" "${ENV_FILE}" \
      | tail -n 1 \
      | cut -d '=' -f2- \
      | sed 's/^"//; s/"$//'
  )"

  printf '%s' "${value}"
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

DOCUMENTATION_ROOT="${SBM_SUITE_ROOT}/context/documentation"
INPUT_DIR="${DOCUMENTATION_ROOT}/input"
BACKUP_DIR="${DOCUMENTATION_ROOT}/backup"
UPGRADE_ZIP="${INPUT_DIR}/documentation-upgrade.zip"
RESPONSE_FILE="$(mktemp)"

trap 'rm -f "${RESPONSE_FILE}"' EXIT

mkdir -p "${INPUT_DIR}" "${BACKUP_DIR}"

[[ -f "${UPGRADE_ZIP}" ]] || {
  echo "ERROR: No existe ${UPGRADE_ZIP}"
  exit 1
}

ZIP_COUNT="$(
  find "${INPUT_DIR}" \
    -maxdepth 1 \
    -type f \
    -name '*.zip' \
    | wc -l \
    | tr -d ' '
)"

[[ "${ZIP_COUNT}" == "1" ]] || {
  echo "ERROR: Debe existir exactamente un ZIP en ${INPUT_DIR}"
  exit 1
}

HTTP_STATUS="$(
  curl --silent --show-error \
    --output "${RESPONSE_FILE}" \
    --write-out "%{http_code}" \
    --request POST \
    "${AI_ASSISTANT_URL%/}/documentation/upgrade" \
    --header "Content-Type: application/json" \
    --data-binary "$(
      PROJECT_NAME="${PROJECT_NAME}" \
      python3 <<'PY'
import json
import os

print(json.dumps({
    "project_name": os.environ["PROJECT_NAME"],
    "workflow": "documentation-upgrade"
}))
PY
    )"
)"

cat "${RESPONSE_FILE}"
echo

if [[ "${HTTP_STATUS}" -lt 200 || "${HTTP_STATUS}" -ge 300 ]]; then
  echo "ERROR: Documentation upgrade respondió HTTP ${HTTP_STATUS}"
  exit 1
fi

python3 - "${RESPONSE_FILE}" <<'PY'
import json
import sys
from pathlib import Path

response_path = Path(sys.argv[1])
payload = json.loads(response_path.read_text(encoding="utf-8"))

if payload.get("workflow") != "documentation-upgrade":
    raise SystemExit(
        "ERROR: La respuesta no corresponde a documentation-upgrade"
    )

if payload.get("project_name") is None:
    raise SystemExit(
        "ERROR: La respuesta no contiene project_name"
    )

if not payload.get("input_cleaned"):
    raise SystemExit(
        "ERROR: El ZIP de entrada no fue limpiado"
    )

updated_files = payload.get("updated_files")

if not isinstance(updated_files, list) or not updated_files:
    raise SystemExit(
        "ERROR: La respuesta no contiene archivos actualizados"
    )

backup_directory = payload.get("backup_directory")

if not isinstance(backup_directory, str) or not backup_directory:
    raise SystemExit(
        "ERROR: La respuesta no contiene backup_directory"
    )
PY

[[ ! -e "${UPGRADE_ZIP}" ]] || {
  echo "ERROR: El ZIP de entrada no fue eliminado"
  exit 1
}

echo "Documentación actualizada correctamente."
