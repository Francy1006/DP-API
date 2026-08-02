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
OUTPUT_DIR="${CONTEXT_ROOT}/output"
PROMPT_TEMPLATE="${CONTEXT_ROOT}/SYS_PROMPT.md"
FORMAT_CONTEXT_FILE="${CONTEXT_ROOT}/FORMAT_CONTEXT.md"
QA_RESULTS_FILE="${DP_API_ROOT}/context/qa-results.md"
PROJECT_TREE_SCRIPT="${CONTEXT_ROOT}/project-tree.sh"
PROJECT_TREE_FILE="${CONTEXT_ROOT}/project-tree.txt"
RESPONSE_FILE="${OUTPUT_DIR}/context-export-response.json"

[[ -f "${PROMPT_TEMPLATE}" ]] || {
  echo "ERROR: No existe ${PROMPT_TEMPLATE}"
  exit 1
}

[[ -f "${FORMAT_CONTEXT_FILE}" ]] || {
  echo "ERROR: No existe ${FORMAT_CONTEXT_FILE}"
  exit 1
}

mkdir -p "${INPUT_DIR}" "${OUTPUT_DIR}"

find "${INPUT_DIR}" -mindepth 1 ! -name ".gitkeep" -delete
find "${OUTPUT_DIR}" -mindepth 1 ! -name ".gitkeep" -delete

sed "s/{{PROJECT_NAME}}/${CONTEXT_PROJECT_NAME}/g" \
  "${PROMPT_TEMPLATE}" > "${OUTPUT_DIR}/SYS_PROMPT.md"

[[ -f "${PROJECT_TREE_SCRIPT}" ]] || {
  echo "ERROR: No existe ${PROJECT_TREE_SCRIPT}"
  exit 1
}

[[ -x "${PROJECT_TREE_SCRIPT}" ]] || {
  echo "ERROR: ${PROJECT_TREE_SCRIPT} no es ejecutable"
  exit 1
}

"${PROJECT_TREE_SCRIPT}"

[[ -f "${PROJECT_TREE_FILE}" ]] || {
  echo "ERROR: No existe ${PROJECT_TREE_FILE}"
  echo "Ejecuta ${PROJECT_TREE_SCRIPT} antes de context-deploy."
  exit 1
}

cd "${DP_API_ROOT}"

GIT_DIFF="$(
  {
    git diff --no-ext-diff -- . \
      ':(exclude).env' ':(exclude).env.*' ':(exclude)**/.env' ':(exclude)**/.env.*'
    git diff --cached --no-ext-diff -- . \
      ':(exclude).env' ':(exclude).env.*' ':(exclude)**/.env' ':(exclude)**/.env.*'
  } 2>/dev/null
)"

CHANGED_FILES="$(
  {
    git diff --name-only -- . \
      ':(exclude).env' ':(exclude).env.*' ':(exclude)**/.env' ':(exclude)**/.env.*'
    git diff --cached --name-only -- . \
      ':(exclude).env' ':(exclude).env.*' ':(exclude)**/.env' ':(exclude)**/.env.*'
    git ls-files --others --exclude-standard
  } 2>/dev/null \
    | awk '!/(^|\/)\.env($|\.)/' \
    | sort -u
)"

if [[ -n "${CHANGED_FILES}" ]]; then
  CHANGED_FILES_INLINE="$(
    printf '%s\n' "${CHANGED_FILES}" \
      | awk 'NF' \
      | paste -sd ',' - \
      | sed 's/,/, /g'
  )"

  CHANGE_SUMMARY="Current ${CONTEXT_PROJECT_NAME} changes affect: ${CHANGED_FILES_INLINE}."
else
  CHANGE_SUMMARY="No uncommitted changes detected in ${CONTEXT_PROJECT_NAME}."
fi

if [[ -f "${QA_RESULTS_FILE}" ]]; then
  QA_RESULTS="$(cat "${QA_RESULTS_FILE}")"
else
  QA_RESULTS="No QA results file was supplied for this context deployment."
fi

PAYLOAD="$(
  PROJECT_NAME="${CONTEXT_PROJECT_NAME}" \
  CHANGE_SUMMARY="${CHANGE_SUMMARY}" \
  CHANGED_FILES="${CHANGED_FILES}" \
  GIT_DIFF="${GIT_DIFF}" \
  QA_RESULTS="${QA_RESULTS}" \
  python3 <<'PY'
import json
import os

changed_files = [
    line.strip()
    for line in os.environ["CHANGED_FILES"].splitlines()
    if line.strip()
]

print(json.dumps({
    "project_name": os.environ["PROJECT_NAME"],
    "workflow": "context-deploy",
    "project_root": "/suite/dp/DP-API",
    "source_context_root": "/suite",
    "format_context_path": "/suite/context/FORMAT_CONTEXT.md",
    "output_directory": "/suite/context/output",
    "change_summary": os.environ["CHANGE_SUMMARY"],
    "changed_files": changed_files,
    "git_diff": os.environ["GIT_DIFF"],
    "qa_results": os.environ["QA_RESULTS"]
}))
PY
)"

curl --fail --silent --show-error \
  -X POST "${AI_ASSISTANT_URL%/}/contexts/export" \
  -H "Content-Type: application/json" \
  --data-binary "${PAYLOAD}" \
  --output "${RESPONSE_FILE}"

python3 - "${RESPONSE_FILE}" <<'PY'
import json
import sys
from pathlib import Path

response_path = Path(sys.argv[1])
payload = json.loads(response_path.read_text(encoding="utf-8"))

if payload.get("status") != "completed":
    raise SystemExit(
        "ERROR: La exportación no terminó con status=completed"
    )

if payload.get("workflow") != "context-deploy":
    raise SystemExit(
        "ERROR: La respuesta no corresponde a context-deploy"
    )

if payload.get("project_name") != "dp-api":
    raise SystemExit(
        "ERROR: La respuesta no corresponde al proyecto dp-api"
    )

if "errors" not in payload:
    raise SystemExit("ERROR: La respuesta no contiene errors")

errors = payload["errors"]
if not isinstance(errors, list) or errors:
    raise SystemExit(f"ERROR: La exportación informó errores: {errors}")

print("Exportación de contexto completada.")
print("Workflow: context-deploy")
print("Proyecto: dp-api")
PY

echo
echo "Generado en: ${OUTPUT_DIR}"
echo "Respuesta: ${RESPONSE_FILE}"
