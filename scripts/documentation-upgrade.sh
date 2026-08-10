#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
ENV_FILE="${PROJECT_ROOT}/.env.dev"

if [[ -z "${SBM_SUITE_ROOT:-}" && -f "${ENV_FILE}" ]]; then
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
fi

[[ -n "${SBM_SUITE_ROOT:-}" ]] || {
  echo "ERROR: Falta SBM_SUITE_ROOT" >&2
  exit 1
}

if [[ "${SBM_SUITE_ROOT}" != /* ]]; then
  SBM_SUITE_ROOT="${PROJECT_ROOT}/${SBM_SUITE_ROOT}"
fi
SBM_SUITE_ROOT="$(cd "${SBM_SUITE_ROOT}" && pwd)"
GLOBAL_SCRIPT="${SBM_SUITE_ROOT}/context/scripts/documentation-upgrade.sh"

[[ -x "${GLOBAL_SCRIPT}" ]] || {
  echo "ERROR: No existe o no es ejecutable ${GLOBAL_SCRIPT}" >&2
  exit 1
}

exec "${GLOBAL_SCRIPT}" "$@"
