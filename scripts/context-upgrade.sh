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
BACKUP_DIR="${CONTEXT_ROOT}/backup"
UPGRADE_ZIP="${INPUT_DIR}/context-upgrade.zip"
RESPONSE_FILE="${CONTEXT_ROOT}/output/context-upgrade-response.json"
CONTRACT_RESPONSE_FILE="$(mktemp)"
PREFLIGHT_FILE="$(mktemp)"

trap 'rm -f "${CONTRACT_RESPONSE_FILE}" "${PREFLIGHT_FILE}"' EXIT

[[ -d "${INPUT_DIR}" ]] || {
  echo "ERROR: No existe ${INPUT_DIR}"
  exit 1
}

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
  "${UPGRADE_ZIP}" \
  "${PREFLIGHT_FILE}" \
  "${EXPECTED_CANONICAL_PROJECT_PATH}" \
  "${CONTEXT_ROOT}/COMPLETED_OBJECTIVES.md" <<'PY'
import hashlib
import json
import re
import stat
import sys
import zipfile
from pathlib import Path, PurePosixPath

contract_path = Path(sys.argv[1])
upgrade_zip = Path(sys.argv[2])
preflight_path = Path(sys.argv[3])
expected_canonical_project_path = sys.argv[4]
completed_objectives_path = Path(sys.argv[5])


def load_json(path, label):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise SystemExit(f"ERROR: {label} inválido: {exc}") from exc


contract = load_json(contract_path, "Contrato de contexto")
contract_version = contract.get("contract_version")
if not isinstance(contract_version, str) or not contract_version.strip():
    raise SystemExit("ERROR: El contrato no contiene contract_version válido")

contract_patch_paths = contract.get("supported_patch_paths")
if (
    not isinstance(contract_patch_paths, list)
    or not all(isinstance(path, str) and path for path in contract_patch_paths)
):
    raise SystemExit("ERROR: El contrato no contiene supported_patch_paths válidos")

lifecycle_phases = contract.get("lifecycle_phases")
if (
    not isinstance(lifecycle_phases, list)
    or not all(isinstance(phase, str) and phase for phase in lifecycle_phases)
):
    raise SystemExit("ERROR: El contrato no contiene lifecycle_phases válidas")

canonical_projects = contract.get("canonical_projects")
if not isinstance(canonical_projects, dict):
    raise SystemExit("ERROR: El contrato no contiene canonical_projects válido")

canonical_project_path = canonical_projects.get("dp-api")
if canonical_project_path != expected_canonical_project_path:
    raise SystemExit(
        "ERROR: canonical_projects['dp-api'] no corresponde a /suite/dp/DP-API"
    )

contract_supported = set(contract_patch_paths)
expected_target_files = {
    "patches/global-project-context.json": "SBM-SUITE/context/PROJECT_CONTEXT.md",
    "patches/completed-objectives.json": "SBM-SUITE/context/COMPLETED_OBJECTIVES.md",
    "patches/suite-context.json": "SBM-SUITE/context/SUITE_CONTEXT.md",
    "patches/business-context.json": "SBM-SUITE/context/BUSINESS_CONTEXT.md",
    "patches/global-qa-context.json": "SBM-SUITE/context/QA_CONTEXT.md",
    "patches/security-context.json": "SBM-SUITE/context/SECURITY_CONTEXT.md",
    "patches/data-context.json": "SBM-SUITE/context/DATA_CONTEXT.md",
    "patches/decisions-context.json": "SBM-SUITE/context/DECISIONS_CONTEXT.md",
    "patches/project-context.json": "SBM-SUITE/dp/DP-API/context/PROJECT_CONTEXT.md",
    "patches/project-qa-context.json": "SBM-SUITE/dp/DP-API/context/QA_CONTEXT.md",
    "patches/project-deploy-context.json": "SBM-SUITE/dp/DP-API/context/DEPLOY_CONTEXT.md",
    "patches/global-readme.json": "SBM-SUITE/context/README.md",
    "patches/project-readme.json": "SBM-SUITE/dp/DP-API/README.md",
}

missing_target_mappings = sorted(contract_supported - set(expected_target_files))
if missing_target_mappings:
    raise SystemExit(
        "ERROR: Faltan mapeos target_file para patches soportados: "
        + ", ".join(missing_target_mappings)
    )

try:
    archive = zipfile.ZipFile(upgrade_zip)
except (OSError, zipfile.BadZipFile) as exc:
    raise SystemExit(f"ERROR: ZIP de upgrade inválido: {exc}") from exc

with archive:
    members = archive.infolist()
    names = [member.filename for member in members]
    if len(names) != len(set(names)):
        raise SystemExit("ERROR: El ZIP contiene rutas duplicadas")

    for member in members:
        name = member.filename
        path = PurePosixPath(name)
        mode = member.external_attr >> 16
        if (
            not name
            or "\\" in name
            or path.is_absolute()
            or ".." in path.parts
            or stat.S_ISLNK(mode)
        ):
            raise SystemExit(f"ERROR: Ruta ZIP insegura: {name!r}")

    manifest_members = [member for member in members if member.filename == "manifest.json"]
    if len(manifest_members) != 1:
        raise SystemExit("ERROR: El ZIP debe contener un único manifest.json en la raíz")

    manifest_member = manifest_members[0]
    if manifest_member.file_size > 1024 * 1024:
        raise SystemExit("ERROR: manifest.json excede 1 MiB")

    try:
        manifest = json.loads(archive.read(manifest_member).decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise SystemExit(f"ERROR: manifest.json inválido: {exc}") from exc

    physical_files = {
        member.filename
        for member in members
        if not member.is_dir()
    }
    physical_patches = {
        name
        for name in physical_files
        if name.startswith("patches/")
    }
    file_bytes = {
        member.filename: archive.read(member)
        for member in members
        if not member.is_dir()
    }
    patch_payloads = {}

    for member in members:
        if member.is_dir() or member.filename not in contract_supported:
            continue
        try:
            patch_payload = json.loads(archive.read(member).decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise SystemExit(
                f"ERROR: {member.filename} inválido: {exc}"
            ) from exc
        if not isinstance(patch_payload, dict):
            raise SystemExit(
                f"ERROR: {member.filename} debe contener un objeto JSON"
            )
        patch_payloads[member.filename] = patch_payload
        expected_target_file = expected_target_files[member.filename]
        if patch_payload.get("target_file") != expected_target_file:
            raise SystemExit(
                f"ERROR: {member.filename}.target_file debe ser "
                f"{expected_target_file}"
            )

if not isinstance(manifest, dict):
    raise SystemExit("ERROR: manifest.json debe contener un objeto JSON")

if manifest.get("project_name") != "dp-api":
    raise SystemExit("ERROR: project_name del manifest debe ser dp-api")

if manifest.get("workflow") != "context-upgrade":
    raise SystemExit("ERROR: workflow del manifest debe ser context-upgrade")

if manifest.get("output_filename") != "context-upgrade.zip":
    raise SystemExit("ERROR: output_filename del manifest debe ser context-upgrade.zip")

allowed_files = manifest.get("allowed_files")
updated_files = manifest.get("updated_files")
content_hashes = manifest.get("content_hashes")
if (
    not isinstance(allowed_files, list)
    or not all(isinstance(item, str) and item for item in allowed_files)
    or len(allowed_files) != len(set(allowed_files))
):
    raise SystemExit("ERROR: manifest.allowed_files debe ser una lista única")
if (
    not isinstance(updated_files, list)
    or not all(isinstance(item, str) and item for item in updated_files)
    or len(updated_files) != len(set(updated_files))
):
    raise SystemExit("ERROR: manifest.updated_files debe ser una lista única")
if not isinstance(content_hashes, dict):
    raise SystemExit("ERROR: manifest.content_hashes debe ser un objeto")

expected_updated_files = physical_files - {"manifest.json"}
if set(allowed_files) != physical_files:
    raise SystemExit(
        "ERROR: manifest.allowed_files debe coincidir con los archivos físicos del ZIP"
    )
if set(updated_files) != expected_updated_files:
    raise SystemExit(
        "ERROR: manifest.updated_files debe coincidir con los archivos no-manifest"
    )
if set(content_hashes) != expected_updated_files:
    raise SystemExit(
        "ERROR: manifest.content_hashes debe coincidir con manifest.updated_files"
    )
for name in sorted(expected_updated_files):
    expected_hash = content_hashes.get(name)
    if not isinstance(expected_hash, str) or len(expected_hash) != 64:
        raise SystemExit(f"ERROR: SHA-256 inválido para {name}")
    actual_hash = hashlib.sha256(file_bytes[name]).hexdigest()
    if actual_hash != expected_hash:
        raise SystemExit(f"ERROR: SHA-256 no coincide para {name}")

if manifest.get("contract_version") != contract_version:
    raise SystemExit("ERROR: contract_version del manifest no coincide con el contrato")

lifecycle_phase = manifest.get("lifecycle_phase")
if lifecycle_phase not in {
    "planning-activation",
    "implementation-progress",
    "implementation-closure",
}:
    raise SystemExit("ERROR: lifecycle_phase del manifest no es válida")

if lifecycle_phase not in lifecycle_phases:
    raise SystemExit(
        f"ERROR: El backend no publica la fase {lifecycle_phase}"
    )

objective_id = manifest.get("objective_id")
if (
    not isinstance(objective_id, str)
    or not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._-]*", objective_id)
):
    raise SystemExit("ERROR: objective_id del manifest es obligatorio o inválido")

if manifest.get("canonical_project_path") != canonical_project_path:
    raise SystemExit(
        "ERROR: canonical_project_path del manifest no corresponde a /suite/dp/DP-API"
    )

manifest_patch_paths = manifest.get("supported_patch_paths")
if (
    not isinstance(manifest_patch_paths, list)
    or not all(isinstance(path, str) and path for path in manifest_patch_paths)
):
    raise SystemExit("ERROR: El manifest no contiene supported_patch_paths válidos")

if len(manifest_patch_paths) != len(set(manifest_patch_paths)):
    raise SystemExit("ERROR: manifest.supported_patch_paths contiene duplicados")

manifest_supported = set(manifest_patch_paths)
unsupported_declared = sorted(manifest_supported - contract_supported)
if unsupported_declared:
    raise SystemExit(
        "ERROR: El manifest declara patches no soportados: "
        + ", ".join(unsupported_declared)
    )

authorized_files = contract_supported | {
    "EXECUTIVE_README.md",
    "COMMIT_MESSAGE.md",
    "manifest.json",
    "USER_PROMPT.md",
}
unauthorized_physical = sorted(physical_files - authorized_files)
if unauthorized_physical:
    raise SystemExit(
        "ERROR: El ZIP contiene archivos no autorizados: "
        + ", ".join(unauthorized_physical)
    )

execution_mode = manifest.get("execution_mode")
user_prompt_file = manifest.get("user_prompt_file")
if execution_mode == "evidence":
    if user_prompt_file is not None or "USER_PROMPT.md" in physical_files:
        raise SystemExit(
            "ERROR: evidence no permite USER_PROMPT.md"
        )
elif execution_mode == "user-guided":
    if user_prompt_file != "USER_PROMPT.md" or "USER_PROMPT.md" not in physical_files:
        raise SystemExit(
            "ERROR: user-guided requiere USER_PROMPT.md"
        )
else:
    raise SystemExit(
        "ERROR: execution_mode debe ser evidence o user-guided"
    )

unsupported_physical = sorted(
    physical_patches - contract_supported.intersection(manifest_supported)
)
if unsupported_physical:
    raise SystemExit(
        "ERROR: El ZIP contiene patches físicos no soportados: "
        + ", ".join(unsupported_physical)
    )

completed_path = "patches/completed-objectives.json"
closure_paths = {
    completed_path,
    "patches/global-project-context.json",
    "patches/project-context.json",
    "patches/global-qa-context.json",
    "patches/project-qa-context.json",
}

if lifecycle_phase in {"planning-activation", "implementation-progress"}:
    if completed_path in physical_patches:
        raise SystemExit(
            f"ERROR: {lifecycle_phase} no permite {completed_path}"
        )
else:
    missing_contract_paths = sorted(closure_paths - contract_supported)
    if missing_contract_paths:
        raise SystemExit(
            "ERROR: El contrato no soporta todos los patches de cierre: "
            + ", ".join(missing_contract_paths)
        )

    missing_physical_paths = sorted(closure_paths - physical_patches)
    if missing_physical_paths:
        raise SystemExit(
            "ERROR: El ZIP no contiene todos los patches de cierre: "
            + ", ".join(missing_physical_paths)
        )

    qa = manifest.get("qa")
    if not isinstance(qa, dict) or qa.get("status") not in {"passed", "success"}:
        raise SystemExit(
            "ERROR: implementation-closure requiere qa.status passed o success"
        )

    if not completed_objectives_path.is_file():
        raise SystemExit(
            f"ERROR: No existe {completed_objectives_path}"
        )
    try:
        completed_markdown = completed_objectives_path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as exc:
        raise SystemExit(
            f"ERROR: COMPLETED_OBJECTIVES.md no es legible: {exc}"
        ) from exc

    completed_payload = patch_payloads[completed_path]
    operations = completed_payload.get("operations")
    if not isinstance(operations, list) or len(operations) != 1:
        raise SystemExit(
            "ERROR: completed-objectives.json debe contener una operación"
        )
    operation = operations[0]
    if not isinstance(operation, dict):
        raise SystemExit(
            "ERROR: La operación de completed-objectives.json es inválida"
        )
    if operation.get("heading") != "## 1. Completed objectives by project":
        raise SystemExit(
            "ERROR: completed-objectives.json usa un heading inválido"
        )
    content = operation.get("content")
    if not isinstance(content, str) or not content.strip():
        raise SystemExit(
            "ERROR: completed-objectives.json no contiene Markdown"
        )

    def headings_outside_fences(markdown, level):
        headings = []
        fence_character = None
        for line in markdown.splitlines():
            stripped = line.strip()
            if stripped.startswith("```") or stripped.startswith("~~~"):
                marker_character = stripped[0]
                if fence_character is None:
                    fence_character = marker_character
                elif marker_character == fence_character:
                    fence_character = None
                continue
            if fence_character is None and stripped.startswith("#" * level + " "):
                if not stripped.startswith("#" * (level + 1)):
                    headings.append(stripped)
        return headings

    def lines_outside_fences(markdown):
        lines = []
        fence_character = None
        for line in markdown.splitlines():
            stripped = line.strip()
            if stripped.startswith("```") or stripped.startswith("~~~"):
                marker_character = stripped[0]
                if fence_character is None:
                    fence_character = marker_character
                elif marker_character == fence_character:
                    fence_character = None
                continue
            if fence_character is None:
                lines.append(stripped)
        return lines

    project_directory = PurePosixPath(canonical_project_path).name
    project_heading = f"### {project_directory}"
    existing_headings = headings_outside_fences(completed_markdown, 3)
    if len(existing_headings) != len(set(existing_headings)):
        raise SystemExit(
            "ERROR: COMPLETED_OBJECTIVES.md contiene headings de proyecto duplicados"
        )
    project_heading_count = existing_headings.count(project_heading)
    if project_heading_count == 0:
        if operation.get("operation") != "append_to_section":
            raise SystemExit(
                "ERROR: Un proyecto sin historial requiere append_to_section"
            )
        appended_headings = headings_outside_fences(content, 3)
        if appended_headings != [project_heading]:
            raise SystemExit(
                f"ERROR: El append debe crear exactamente {project_heading}"
            )
        outside_lines = lines_outside_fences(content)
        required_header = (
            "| Objective ID | Project | Objective | Final status | Priority | "
            "Branch | Started | Completed | Summary | Validation | Documentation | "
            "Proposed commit |"
        )
        required_separator = (
            "|---|---|---|---|---:|---|---|---|---|---|---|---|"
        )
        table_valid = any(
            line == required_header
            and index + 1 < len(outside_lines)
            and outside_lines[index + 1] == required_separator
            for index, line in enumerate(outside_lines)
        )
        if not table_valid:
            raise SystemExit(
                "ERROR: El primer grupo completado requiere la tabla canónica"
            )
    elif project_heading_count == 1:
        if operation.get("operation") != "replace_section":
            raise SystemExit(
                "ERROR: Un proyecto con historial requiere replace_section"
            )
        replacement_headings = headings_outside_fences(content, 3)
        if replacement_headings != existing_headings:
            raise SystemExit(
                "ERROR: El replace de completed objectives debe preservar todos "
                "los headings de proyecto"
            )
    else:
        raise SystemExit(
            f"ERROR: {project_heading} aparece más de una vez"
        )

preflight_path.write_text(
    json.dumps(
        {
            "contract_version": contract_version,
            "lifecycle_phase": lifecycle_phase,
            "objective_id": objective_id,
            "canonical_project_path": canonical_project_path,
        }
    ),
    encoding="utf-8",
)

print(f"Preflight de upgrade validado para {lifecycle_phase} / {objective_id}")
PY

mkdir -p "${BACKUP_DIR}" "$(dirname "${RESPONSE_FILE}")"
rm -f "${RESPONSE_FILE}"

HTTP_STATUS="$(
  curl --silent --show-error \
    --output "${RESPONSE_FILE}" \
    --write-out "%{http_code}" \
    --request POST \
    "${AI_ASSISTANT_URL%/}/contexts/upgrade" \
    --header "Content-Type: application/json" \
    --data-binary "$(
      PROJECT_NAME="${CONTEXT_PROJECT_NAME}" \
      PREFLIGHT_FILE="${PREFLIGHT_FILE}" \
      python3 <<'PY'
import json
import os
from pathlib import Path

preflight = json.loads(
    Path(os.environ["PREFLIGHT_FILE"]).read_text(encoding="utf-8")
)

print(json.dumps({
    "project_name": os.environ["PROJECT_NAME"],
    "workflow": "context-upgrade",
    "contract_version": preflight["contract_version"],
    "lifecycle_phase": preflight["lifecycle_phase"],
    "objective_id": preflight["objective_id"],
    "canonical_project_path": preflight["canonical_project_path"]
}))
PY
    )"
)"

if [[ "${HTTP_STATUS}" -lt 200 || "${HTTP_STATUS}" -ge 300 ]]; then
  echo "ERROR: Context upgrade respondió HTTP ${HTTP_STATUS}"
  if [[ -s "${RESPONSE_FILE}" ]]; then
    echo "Respuesta del backend:"
    cat "${RESPONSE_FILE}"
    echo
  fi
  echo "Respuesta guardada en: ${RESPONSE_FILE}"
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
