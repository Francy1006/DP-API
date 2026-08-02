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

  awk -v key="${key}" '
    index($0, key "=") == 1 { value = substr($0, length(key) + 2) }
    END {
      sub(/\r$/, "", value)
      sub(/^"/, "", value)
      sub(/"$/, "", value)
      printf "%s", value
    }
  ' "${ENV_FILE}"
}

DOPPLER_PROJECT="$(get_env DOPPLER_PROJECT)"
AI_ASSISTANT_URL="$(get_env AI_ASSISTANT_URL)"
SBM_SUITE_ROOT="$(get_env SBM_SUITE_ROOT)"
CONTEXT_PROJECT_NAME="dp-api"

[[ -n "${DOPPLER_PROJECT}" ]] || {
  echo "ERROR: Falta DOPPLER_PROJECT"
  exit 1
}

[[ -n "${AI_ASSISTANT_URL}" ]] || {
  echo "ERROR: Falta AI_ASSISTANT_URL"
  exit 1
}

[[ -n "${SBM_SUITE_ROOT}" ]] || {
  echo "ERROR: Falta SBM_SUITE_ROOT"
  exit 1
}

[[ -d "${SBM_SUITE_ROOT}" ]] || {
  echo "ERROR: No existe ${SBM_SUITE_ROOT}"
  exit 1
}

CONTEXT_ROOT="${SBM_SUITE_ROOT}/context"
INPUT_DIR="${CONTEXT_ROOT}/input"
BACKUP_DIR="${CONTEXT_ROOT}/backup"
UPGRADE_ZIP="${INPUT_DIR}/context-upgrade.zip"
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
    "${AI_ASSISTANT_URL%/}/contexts/upgrade" \
    --header "Content-Type: application/json" \
    --data-binary "$(
      PROJECT_NAME="${CONTEXT_PROJECT_NAME}" \
      python3 <<'PY'
import json
import os

print(json.dumps({
    "project_name": os.environ["PROJECT_NAME"],
    "workflow": "context-upgrade"
}))
PY
    )"
)"

cat "${RESPONSE_FILE}"
echo

if [[ "${HTTP_STATUS}" -lt 200 || "${HTTP_STATUS}" -ge 300 ]]; then
  echo "ERROR: Context upgrade respondió HTTP ${HTTP_STATUS}"
  exit 1
fi

python3 - "${RESPONSE_FILE}" <<'PY'
import json
import sys
from pathlib import Path

response_path = Path(sys.argv[1])
payload = json.loads(response_path.read_text(encoding="utf-8"))

if payload.get("workflow") != "context-upgrade":
    raise SystemExit(
        "ERROR: La respuesta no corresponde a context-upgrade"
    )

if payload.get("project_name") != "dp-api":
    raise SystemExit(
        "ERROR: La respuesta no corresponde al proyecto dp-api"
    )

if "errors" not in payload:
    raise SystemExit("ERROR: La respuesta no contiene errors")

errors = payload["errors"]

if not isinstance(errors, list) or errors:
    raise SystemExit(f"ERROR: El upgrade informó errores: {errors}")

if payload.get("input_cleaned") is not True:
    raise SystemExit(
        "ERROR: El ZIP de entrada no fue limpiado"
    )

updated_files = payload.get("updated_files")

if (
    not isinstance(updated_files, list)
    or not updated_files
    or not all(isinstance(path, str) and path for path in updated_files)
):
    raise SystemExit(
        "ERROR: La respuesta no contiene archivos actualizados"
    )

backup_directory = payload.get("backup_directory")

if not isinstance(backup_directory, str) or not backup_directory:
    raise SystemExit(
        "ERROR: La respuesta no contiene backup_directory"
    )

if not backup_directory.startswith("/suite/context/backup/"):
    raise SystemExit(
        "ERROR: backup_directory no pertenece a /suite/context/backup"
    )

print("Archivos actualizados:")
for updated_file in updated_files:
    print(f"- {updated_file}")

print(f"Backup generado: {backup_directory}")
PY

[[ ! -e "${UPGRADE_ZIP}" ]] || {
  echo "ERROR: El ZIP de entrada no fue eliminado"
  exit 1
}

echo "Contextos actualizados correctamente."
