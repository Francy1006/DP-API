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

CONTEXT_ROOT="${SBM_SUITE_ROOT}/context"
INPUT_DIR="${CONTEXT_ROOT}/input"
OUTPUT_DIR="${CONTEXT_ROOT}/output"
PROMPT_TEMPLATE="${CONTEXT_ROOT}/SYS_PROMPT.md"
FORMAT_CONTEXT_FILE="${CONTEXT_ROOT}/FORMAT_CONTEXT.md"
QA_RESULTS_FILE="${DP_API_ROOT}/context/qa-results.md"

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

sed "s/{{PROJECT_NAME}}/${PROJECT_NAME}/g" \
  "${PROMPT_TEMPLATE}" > "${OUTPUT_DIR}/SYS_PROMPT.md"

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
  QA_RESULTS="No QA results file was supplied for this context deployment."
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
    "workflow": "context-deploy",
    "project_root": "/suite/DP-API",
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
  -X POST "${AI_ASSISTANT_URL}/contexts/export" \
  -H "Content-Type: application/json" \
  --data-binary "${PAYLOAD}"

echo
echo "Generado en: ${OUTPUT_DIR}"
