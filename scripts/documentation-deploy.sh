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
OUTPUT_DIR="${DOCUMENTATION_ROOT}/output"
FORMAT_CONTEXT_FILE="${DOCUMENTATION_ROOT}/FORMAT_CONTEXT.md"
SYSTEM_PROMPT_FILE="${DOCUMENTATION_ROOT}/SYS_PROMPT.md"
QA_RESULTS_FILE="${DP_API_ROOT}/context/qa-results.md"
PROJECT_TREE_SCRIPT="${DP_API_ROOT}/scripts/project-tree.sh"
PROJECT_TREE_FILE="${DP_API_ROOT}/project-tree.txt"
RESPONSE_FILE="${OUTPUT_DIR}/documentation-export-response.json"

[[ -f "${FORMAT_CONTEXT_FILE}" ]] || {
  echo "ERROR: No existe ${FORMAT_CONTEXT_FILE}"
  exit 1
}

[[ -f "${SYSTEM_PROMPT_FILE}" ]] || {
  echo "ERROR: No existe ${SYSTEM_PROMPT_FILE}"
  exit 1
}

mkdir -p "${INPUT_DIR}" "${OUTPUT_DIR}"

find "${INPUT_DIR}" -mindepth 1 ! -name ".gitkeep" -delete
find "${OUTPUT_DIR}" -mindepth 1 ! -name ".gitkeep" -delete

if [[ -f "${PROJECT_TREE_SCRIPT}" ]]; then
  [[ -x "${PROJECT_TREE_SCRIPT}" ]] || {
    echo "ERROR: ${PROJECT_TREE_SCRIPT} no es ejecutable"
    exit 1
  }

  "${PROJECT_TREE_SCRIPT}"
fi

[[ -f "${PROJECT_TREE_FILE}" ]] || {
  echo "ERROR: No existe ${PROJECT_TREE_FILE}"
  echo "Ejecuta scripts/project-tree.sh antes de documentation-deploy."
  exit 1
}

cd "${DP_API_ROOT}"

GIT_DIFF="$(
  {
    git diff --no-ext-diff
    git diff --cached --no-ext-diff
  } 2>/dev/null
)"

CHANGED_FILES="$(
  {
    git diff --name-only
    git diff --cached --name-only
    git ls-files --others --exclude-standard
  } 2>/dev/null | sort -u
)"

if [[ -n "${CHANGED_FILES}" ]]; then
  CHANGED_FILES_INLINE="$(
    printf '%s\n' "${CHANGED_FILES}" \
      | awk 'NF' \
      | paste -sd ',' - \
      | sed 's/,/, /g'
  )"

  CHANGE_SUMMARY="Current ${PROJECT_NAME} changes affect: ${CHANGED_FILES_INLINE}."
else
  CHANGE_SUMMARY="No uncommitted changes detected in ${PROJECT_NAME}."
fi

if [[ -f "${QA_RESULTS_FILE}" ]]; then
  QA_RESULTS="$(cat "${QA_RESULTS_FILE}")"
else
  QA_RESULTS="No QA results file was supplied for this documentation deployment."
fi

PAYLOAD="$(
  PROJECT_NAME="${PROJECT_NAME}" \
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
    "workflow": "documentation-deploy",
    "project_root": "/suite/DP-API",
    "documentation_root": "/suite/context/documentation",
    "format_context_path": "/suite/context/documentation/FORMAT_CONTEXT.md",
    "system_prompt_path": "/suite/context/documentation/SYS_PROMPT.md",
    "output_directory": "/suite/context/documentation/output",
    "change_summary": os.environ["CHANGE_SUMMARY"],
    "changed_files": changed_files,
    "git_diff": os.environ["GIT_DIFF"],
    "qa_results": os.environ["QA_RESULTS"],
    "retrieved_context_chunks": []
}))
PY
)"

curl --fail --silent --show-error \
  --request POST \
  "${AI_ASSISTANT_URL%/}/documentation/export" \
  --header "Content-Type: application/json" \
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

if payload.get("workflow") != "documentation-deploy":
    raise SystemExit(
        "ERROR: La respuesta no corresponde a documentation-deploy"
    )

if payload.get("collection_name") != "sbm_documentation":
    raise SystemExit(
        "ERROR: La colección esperada es sbm_documentation"
    )

zip_path = payload.get("documentation_zip_path")

if not isinstance(zip_path, str) or not zip_path:
    raise SystemExit(
        "ERROR: La respuesta no contiene documentation_zip_path"
    )

print(json.dumps(payload, ensure_ascii=False, indent=2))
PY

echo
echo "Generado en: ${OUTPUT_DIR}"
echo "Respuesta: ${RESPONSE_FILE}"
