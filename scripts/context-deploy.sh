#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'EOF'
Uso:
  ./scripts/context-deploy.sh planning-activation <objective_id> <user_prompt>
  ./scripts/context-deploy.sh implementation-progress <objective_id> [user_prompt]
  ./scripts/context-deploy.sh implementation-closure <objective_id> [user_prompt]
EOF
}

[[ "$#" -ge 2 && "$#" -le 3 ]] || {
  usage >&2
  exit 1
}

LIFECYCLE_PHASE="$1"
OBJECTIVE_ID="$2"
USER_PROMPT="${3:-}"

case "${LIFECYCLE_PHASE}" in
  planning-activation|implementation-progress|implementation-closure)
    ;;
  *)
    echo "ERROR: Fase de ciclo de vida no válida: ${LIFECYCLE_PHASE}" >&2
    usage >&2
    exit 1
    ;;
esac

[[ -n "${OBJECTIVE_ID//[[:space:]]/}" ]] || {
  echo "ERROR: objective_id es obligatorio" >&2
  exit 1
}

[[ "${OBJECTIVE_ID}" =~ ^[A-Za-z0-9][A-Za-z0-9._-]*$ ]] || {
  echo "ERROR: objective_id contiene caracteres no permitidos" >&2
  exit 1
}

if [[ "${LIFECYCLE_PHASE}" == "planning-activation" ]]; then
  [[ "$#" -eq 3 && -n "${USER_PROMPT//[[:space:]]/}" ]] || {
    echo "ERROR: planning-activation requiere el texto literal del objetivo" >&2
    exit 1
  }
fi

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
SBM_SUITE_ROOT_RAW="$(get_env SBM_SUITE_ROOT)"
CONTEXT_PROJECT_NAME="dp-api"
EXPECTED_CANONICAL_PROJECT_PATH="/suite/dp/DP-API"

[[ -n "${DOPPLER_PROJECT}" ]] || {
  echo "ERROR: Falta DOPPLER_PROJECT"
  exit 1
}

[[ -n "${AI_ASSISTANT_URL}" ]] || {
  echo "ERROR: Falta AI_ASSISTANT_URL"
  exit 1
}

[[ -n "${SBM_SUITE_ROOT_RAW}" ]] || {
  echo "ERROR: Falta SBM_SUITE_ROOT"
  exit 1
}

resolve_suite_root() {
  local configured_path="$1"
  local candidate

  if [[ "${configured_path}" = /* ]]; then
    candidate="${configured_path}"
  else
    candidate="${DP_API_ROOT}/${configured_path}"
  fi

  [[ -d "${candidate}" ]] || {
    echo "ERROR: No existe SBM_SUITE_ROOT resuelto en ${candidate}" >&2
    return 1
  }

  (cd "${candidate}" && pwd)
}

SBM_SUITE_ROOT="$(resolve_suite_root "${SBM_SUITE_ROOT_RAW}")"

CONTEXT_ROOT="${SBM_SUITE_ROOT}/context"
INPUT_DIR="${CONTEXT_ROOT}/input"
OUTPUT_DIR="${CONTEXT_ROOT}/output"
PROMPT_TEMPLATE="${CONTEXT_ROOT}/SYS_PROMPT.md"
FORMAT_CONTEXT_FILE="${CONTEXT_ROOT}/FORMAT_CONTEXT.md"
QA_RESULTS_FILE="${DP_API_ROOT}/context/qa-results.md"
PROJECT_TREE_SCRIPT="${CONTEXT_ROOT}/project-tree.sh"
PROJECT_TREE_FILE="${CONTEXT_ROOT}/project-tree.txt"
SYSTEM_PROMPT_FILE="${OUTPUT_DIR}/SYS_PROMPT.md"
CONTEXT_PACKAGE_FILE="${OUTPUT_DIR}/context-package.zip"
UPLOAD_ZIP_FILE="${OUTPUT_DIR}/context-deploy-package.zip"
RESPONSE_FILE="$(mktemp)"
CONTRACT_RESPONSE_FILE="$(mktemp)"
CONTRACT_METADATA_FILE="$(mktemp)"

trap 'rm -f "${RESPONSE_FILE}" "${CONTRACT_RESPONSE_FILE}" "${CONTRACT_METADATA_FILE}"' EXIT

CONTRACT_HTTP_STATUS="$(
  curl --silent --show-error \
    --output "${CONTRACT_RESPONSE_FILE}" \
    --write-out "%{http_code}" \
    --request GET \
    "${AI_ASSISTANT_URL%/}/contexts/contract"
)"

[[ "${CONTRACT_HTTP_STATUS}" == "200" ]] || {
  echo "ERROR: /contexts/contract respondió HTTP ${CONTRACT_HTTP_STATUS}" >&2
  exit 1
}

python3 - \
  "${CONTRACT_RESPONSE_FILE}" \
  "${LIFECYCLE_PHASE}" \
  "${EXPECTED_CANONICAL_PROJECT_PATH}" \
  "${CONTRACT_METADATA_FILE}" <<'PY'
import json
import sys
from pathlib import Path

contract_path = Path(sys.argv[1])
lifecycle_phase = sys.argv[2]
expected_canonical_project_path = sys.argv[3]
metadata_path = Path(sys.argv[4])

try:
    contract = json.loads(contract_path.read_text(encoding="utf-8"))
except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
    raise SystemExit(f"ERROR: Contrato de contexto inválido: {exc}") from exc

contract_version = contract.get("contract_version")
if not isinstance(contract_version, str) or not contract_version.strip():
    raise SystemExit("ERROR: El contrato no contiene contract_version válido")

supported_patch_paths = contract.get("supported_patch_paths")
if (
    not isinstance(supported_patch_paths, list)
    or not all(isinstance(path, str) and path for path in supported_patch_paths)
):
    raise SystemExit("ERROR: El contrato no contiene supported_patch_paths válidos")

lifecycle_phases = contract.get("lifecycle_phases")
if (
    not isinstance(lifecycle_phases, list)
    or not all(isinstance(phase, str) and phase for phase in lifecycle_phases)
):
    raise SystemExit("ERROR: El contrato no contiene lifecycle_phases válidas")

if lifecycle_phase not in lifecycle_phases:
    raise SystemExit(
        f"ERROR: El backend no publica la fase {lifecycle_phase}"
    )

canonical_projects = contract.get("canonical_projects")
if not isinstance(canonical_projects, dict):
    raise SystemExit("ERROR: El contrato no contiene canonical_projects válido")

canonical_project_path = canonical_projects.get("dp-api")
if canonical_project_path != expected_canonical_project_path:
    raise SystemExit(
        "ERROR: canonical_projects['dp-api'] no corresponde a /suite/dp/DP-API"
    )

supported = set(supported_patch_paths)
context_paths = {
    "patches/global-project-context.json",
    "patches/project-context.json",
}
if not context_paths.issubset(supported):
    raise SystemExit(
        "ERROR: El contrato no permite los patches global/project context"
    )

if lifecycle_phase == "implementation-closure":
    closure_paths = {
        "patches/completed-objectives.json",
        "patches/global-project-context.json",
        "patches/project-context.json",
        "patches/global-qa-context.json",
        "patches/project-qa-context.json",
    }
    missing = sorted(closure_paths - supported)
    if missing:
        raise SystemExit(
            "ERROR: El contrato no soporta todos los patches de cierre: "
            + ", ".join(missing)
        )

metadata_path.write_text(
    json.dumps(
        {
            "canonical_project_path": canonical_project_path,
            "contract_version": contract_version,
        }
    ),
    encoding="utf-8",
)

print(f"Contrato de contexto validado: {contract_version}")
PY

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

python3 - \
  "${PROMPT_TEMPLATE}" \
  "${SYSTEM_PROMPT_FILE}" \
  "${CONTRACT_METADATA_FILE}" \
  "${CONTEXT_PROJECT_NAME}" \
  "${LIFECYCLE_PHASE}" \
  "${OBJECTIVE_ID}" <<'PY'
import json
import sys
from pathlib import Path

template_path = Path(sys.argv[1])
output_path = Path(sys.argv[2])
metadata_path = Path(sys.argv[3])
project_name = sys.argv[4]
lifecycle_phase = sys.argv[5]
objective_id = sys.argv[6]

metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
contract_version = metadata.get("contract_version")
if not isinstance(contract_version, str) or not contract_version:
    raise SystemExit("ERROR: No se pudo resolver contract_version para SYS_PROMPT.md")

rendered = template_path.read_text(encoding="utf-8")
replacements = {
    "{{PROJECT_NAME}}": project_name,
    "{{CONTRACT_VERSION}}": contract_version,
    "{{LIFECYCLE_PHASE}}": lifecycle_phase,
    "{{OBJECTIVE_ID}}": objective_id,
}
for placeholder, value in replacements.items():
    rendered = rendered.replace(placeholder, value)

unresolved = [
    placeholder
    for placeholder in replacements
    if placeholder in rendered
]
if unresolved:
    raise SystemExit(
        "ERROR: SYS_PROMPT.md conserva placeholders sin resolver: "
        + ", ".join(unresolved)
    )

output_path.write_text(rendered, encoding="utf-8")
PY

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
  QA_RESULTS=""
fi

if [[ "${LIFECYCLE_PHASE}" == "implementation-closure" ]]; then
  [[ -f "${QA_RESULTS_FILE}" ]] || {
    echo "ERROR: implementation-closure requiere ${QA_RESULTS_FILE}" >&2
    exit 1
  }

  [[ -n "${QA_RESULTS//[[:space:]]/}" ]] || {
    echo "ERROR: ${QA_RESULTS_FILE} está vacío" >&2
    exit 1
  }
fi

PAYLOAD="$(
  PROJECT_NAME="${CONTEXT_PROJECT_NAME}" \
  LIFECYCLE_PHASE="${LIFECYCLE_PHASE}" \
  OBJECTIVE_ID="${OBJECTIVE_ID}" \
  USER_PROMPT="${USER_PROMPT}" \
  HAS_USER_PROMPT="$([[ -n "${USER_PROMPT}" ]] && printf '1' || printf '0')" \
  CONTRACT_METADATA_FILE="${CONTRACT_METADATA_FILE}" \
  CHANGE_SUMMARY="${CHANGE_SUMMARY}" \
  CHANGED_FILES="${CHANGED_FILES}" \
  GIT_DIFF="${GIT_DIFF}" \
  QA_RESULTS="${QA_RESULTS}" \
  python3 <<'PY'
import json
import os
from pathlib import Path

contract_metadata = json.loads(
    Path(os.environ["CONTRACT_METADATA_FILE"]).read_text(encoding="utf-8")
)

changed_files = [
    line.strip()
    for line in os.environ["CHANGED_FILES"].splitlines()
    if line.strip()
]

print(json.dumps({
    "project_name": os.environ["PROJECT_NAME"],
    "workflow": "context-deploy",
    "lifecycle_phase": os.environ["LIFECYCLE_PHASE"],
    "objective_id": os.environ["OBJECTIVE_ID"],
    "user_prompt": (
        os.environ["USER_PROMPT"]
        if os.environ["HAS_USER_PROMPT"] == "1"
        else None
    ),
    "project_root": contract_metadata["canonical_project_path"],
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

curl --fail-with-body --silent --show-error \
  -X POST "${AI_ASSISTANT_URL%/}/contexts/export" \
  -H "Content-Type: application/json" \
  --data-binary "${PAYLOAD}" \
  --output "${RESPONSE_FILE}"

python3 - \
  "${RESPONSE_FILE}" \
  "${LIFECYCLE_PHASE}" \
  "${OBJECTIVE_ID}" \
  "${UPLOAD_ZIP_FILE}" <<'PY'
import json
import sys
from pathlib import Path
from zipfile import BadZipFile, ZipFile

response_path = Path(sys.argv[1])
expected_lifecycle_phase = sys.argv[2]
expected_objective_id = sys.argv[3]
upload_zip_path = Path(sys.argv[4])

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

if payload.get("lifecycle_phase") != expected_lifecycle_phase:
    raise SystemExit(
        "ERROR: lifecycle_phase de respuesta no coincide con la solicitud"
    )

if payload.get("objective_id") != expected_objective_id:
    raise SystemExit(
        "ERROR: objective_id de respuesta no coincide con la solicitud"
    )

if "errors" not in payload:
    raise SystemExit("ERROR: La respuesta no contiene errors")

errors = payload["errors"]
if not isinstance(errors, list) or errors:
    raise SystemExit(f"ERROR: La exportación informó errores: {errors}")

context_zip_path = payload.get("context_zip_path")
upload_response_path = payload.get("upload_zip_path")
if not isinstance(context_zip_path, str) or Path(context_zip_path).name != "context-package.zip":
    raise SystemExit("ERROR: context_zip_path inválido")
if not isinstance(upload_response_path, str) or Path(upload_response_path).name != "context-deploy-package.zip":
    raise SystemExit("ERROR: upload_zip_path inválido")
if not upload_zip_path.is_file():
    raise SystemExit(f"ERROR: No existe el paquete único {upload_zip_path}")

try:
    with ZipFile(upload_zip_path) as archive:
        names = {name for name in archive.namelist() if not name.endswith("/")}
        expected = {
            "context-export-response.json",
            "context-package.zip",
            "SYS_PROMPT.md",
        }
        if names != expected:
            raise SystemExit(
                "ERROR: El paquete único no contiene exactamente los 3 artefactos requeridos"
            )
        embedded_response = json.loads(
            archive.read("context-export-response.json").decode("utf-8")
        )
        if embedded_response != payload:
            raise SystemExit(
                "ERROR: La respuesta embebida no coincide con la respuesta del backend"
            )
except (BadZipFile, UnicodeDecodeError, json.JSONDecodeError) as exc:
    raise SystemExit(f"ERROR: Paquete único inválido: {exc}") from exc

print("Exportación de contexto completada.")
print("Workflow: context-deploy")
print("Proyecto: dp-api")
print(f"Fase: {payload['lifecycle_phase']}")
print(f"Objetivo: {payload['objective_id']}")
PY

rm -f "${CONTEXT_PACKAGE_FILE}" "${SYSTEM_PROMPT_FILE}"

[[ -f "${UPLOAD_ZIP_FILE}" ]] || {
  echo "ERROR: No existe ${UPLOAD_ZIP_FILE}" >&2
  exit 1
}

echo
echo "Paquete único para ChatGPT:"
echo "${UPLOAD_ZIP_FILE}"
