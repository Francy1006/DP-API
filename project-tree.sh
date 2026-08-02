#!/usr/bin/env bash
set -euo pipefail

DP_API_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ENV_FILE="${DP_API_ROOT}/.env.dev"

[[ -f "${ENV_FILE}" ]] || {
  echo "ERROR: No existe ${ENV_FILE}"
  exit 1
}

SBM_SUITE_ROOT="$(
  awk '
    index($0, "SBM_SUITE_ROOT=") == 1 {
      value = substr($0, length("SBM_SUITE_ROOT=") + 1)
    }
    END {
      sub(/\r$/, "", value)
      sub(/^"/, "", value)
      sub(/"$/, "", value)
      printf "%s", value
    }
  ' "${ENV_FILE}"
)"

[[ -n "${SBM_SUITE_ROOT}" ]] || {
  echo "ERROR: Falta SBM_SUITE_ROOT"
  exit 1
}

[[ -d "${SBM_SUITE_ROOT}" ]] || {
  echo "ERROR: No existe ${SBM_SUITE_ROOT}"
  exit 1
}

GLOBAL_PROJECT_TREE_SCRIPT="${SBM_SUITE_ROOT}/context/project-tree.sh"

[[ -f "${GLOBAL_PROJECT_TREE_SCRIPT}" ]] || {
  echo "ERROR: No existe ${GLOBAL_PROJECT_TREE_SCRIPT}"
  exit 1
}

[[ -x "${GLOBAL_PROJECT_TREE_SCRIPT}" ]] || {
  echo "ERROR: ${GLOBAL_PROJECT_TREE_SCRIPT} no es ejecutable"
  exit 1
}

exec "${GLOBAL_PROJECT_TREE_SCRIPT}"
