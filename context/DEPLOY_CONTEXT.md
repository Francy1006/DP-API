# DEPLOY_CONTEXT.md

> **Project:** DP-API
>
> **Last updated:** 2026-08-02
>
> **Purpose:** Document the real export and reviewed-upgrade workflows for DP-API context files. These workflows do not deploy application infrastructure.

## 1. Scope and ownership

DP-API owns the client-side orchestration scripts:

```text
dp/DP-API/scripts/context-deploy.sh
dp/DP-API/scripts/context-upgrade.sh
```

SBM-AI-ASSISTANT owns the backend endpoints that build the context package and apply a reviewed upgrade. The shared suite context owns the prompt, format, exchange directories, backup and project tree.

Neither script runs database migrations, modifies PostgreSQL, commits, pushes, or calculates the suite root from parent directories.

## 2. Required configuration

Both scripts locate DP-API from their own file location and read the project-local `.env.dev`. They read:

```text
DOPPLER_PROJECT
AI_ASSISTANT_URL
SBM_SUITE_ROOT
```

`DOPPLER_PROJECT` must be present for the local environment, while the context protocol always identifies this repository as:

```text
project_name=dp-api
```

`SBM_SUITE_ROOT` is the only allowed host source for the suite root. It must name an existing directory. Environment values, credentials and tokens must never be copied into context artifacts or logs.

## 3. Canonical paths

Host paths are derived from `${SBM_SUITE_ROOT}`:

| Purpose | Host path | Container path |
|---|---|---|
| Suite source root | `${SBM_SUITE_ROOT}` | `/suite` |
| DP-API project | `${SBM_SUITE_ROOT}/dp/DP-API` | `/suite/dp/DP-API` |
| System prompt | `${SBM_SUITE_ROOT}/context/SYS_PROMPT.md` | `/suite/context/SYS_PROMPT.md` |
| Format definition | `${SBM_SUITE_ROOT}/context/FORMAT_CONTEXT.md` | `/suite/context/FORMAT_CONTEXT.md` |
| Input | `${SBM_SUITE_ROOT}/context/input` | `/suite/context/input` |
| Output | `${SBM_SUITE_ROOT}/context/output` | `/suite/context/output` |
| Backup | `${SBM_SUITE_ROOT}/context/backup` | `/suite/context/backup` |
| Tree generator | `${SBM_SUITE_ROOT}/context/project-tree.sh` | `/suite/context/project-tree.sh` |
| Project tree | `${SBM_SUITE_ROOT}/context/project-tree.txt` | `/suite/context/project-tree.txt` |

There is one backup directory: `context/backup`. The workflows must never create or use an alternative plural directory. Project-tree artifacts are global and are not generated inside DP-API.

## 4. Context deploy workflow

The phase and objective are positional inputs and are never inferred from Git,
QA, changed files, prompts or current context state. Accepted commands are:

```bash
./scripts/context-deploy.sh planning-activation DP-MATERIAL-001 \
  "Implementar la integración Material solicitada"

./scripts/context-deploy.sh implementation-progress DP-MATERIAL-001

./scripts/context-deploy.sh implementation-closure DP-MATERIAL-001
```

`objective_id` is mandatory for every phase. `planning-activation` also requires
the literal objective text as `user_prompt`; it is optional for progress and
closure.

The script performs the following sequence:

1. validates the explicit phase, objective and phase-specific prompt arguments;
2. reads and validates the required variables from `.env.dev`;
3. requests `GET /contexts/contract` and requires HTTP 200;
4. validates `contract_version`, `lifecycle_phases`, `canonical_project_path` and `supported_patch_paths`;
5. requires global/project context support for activation and progress, and all five closing patches for closure;
6. aborts before creating or cleaning exchange outputs if the contract preflight fails;
7. validates the global prompt and format files;
8. prepares input/output and removes stale exchange artifacts while preserving `.gitkeep`;
9. generates `/suite/context/output/SYS_PROMPT.md` for `dp-api`;
10. requires and runs the global project-tree script and output;
11. captures Git diff, modified files and optional QA results, excluding `.env*` paths;
12. sends `POST /contexts/export` and validates the completed response.

The backend payload contains exactly these path semantics:

```text
project_name=dp-api
workflow=context-deploy
lifecycle_phase=<explicit phase>
objective_id=<explicit objective>
user_prompt=<literal text or null>
project_root=/suite/dp/DP-API
source_context_root=/suite
format_context_path=/suite/context/FORMAT_CONTEXT.md
output_directory=/suite/context/output
```

The payload also includes `change_summary`, `changed_files`, `git_diff` and `qa_results`. It must not contain environment files, secrets or tokens.

Expected reviewed artifacts are written under:

```text
${SBM_SUITE_ROOT}/context/output
```

The exact archive names returned by the backend remain backend-controlled and must be confirmed from its successful response.

## 5. Manual review stage

The generated package and parameterized prompt are provided to the approved context-review process. The returned archive must be named exactly:

```text
context-upgrade.zip
```

Place it at:

```text
${SBM_SUITE_ROOT}/context/input/context-upgrade.zip
```

Only reviewed context and README changes belonging to the allowlist may be accepted. QA, business, deployment and prompt sources remain protected unless a separately authorized workflow explicitly includes them.

## 6. Context upgrade workflow

Apply the reviewed archive with:

```bash
./scripts/context-upgrade.sh
```

The script:

1. reads and validates `.env.dev` and `SBM_SUITE_ROOT`;
2. searches only `${SBM_SUITE_ROOT}/context/input/context-upgrade.zip`;
3. requires that this file exists and that exactly one `*.zip` exists directly in the global input directory;
4. requests `GET /contexts/contract` and requires HTTP 200;
5. inspects the root `manifest.json` with Python's ZIP reader without extracting files;
6. rejects duplicate, absolute, parent-traversal, backslash or symbolic-link members;
7. validates contract version, phase, objective, canonical path and supported patches;
8. checks every physical `patches/*` file against both contract and manifest support;
9. rejects `completed-objectives.json` during activation or progress;
10. requires all five closing patches during implementation closure;
11. creates or reuses only `${SBM_SUITE_ROOT}/context/backup` after preflight succeeds;
12. calls `POST /contexts/upgrade` with the validated manifest metadata;
13. preserves the ZIP on transport, HTTP or preflight failure;
14. validates the backend response, verifies cleanup and prints updated files and backup.

The five mandatory closing patches are:

```text
patches/completed-objectives.json
patches/global-project-context.json
patches/project-context.json
patches/global-qa-context.json
patches/project-qa-context.json
```

Activation and progress reject the completed-objectives patch but do not require
it. Client preflight never replaces the backend's authoritative validation.

The backend is responsible for validating archive type, paths, allowlist, manifest, hashes, UTF-8 content, duplicate members, symbolic links, archive limits and Zip Slip before changing any target.

## 7. Atomicity and cleanup

The backend must stage and validate the complete upgrade, create the backup, and then replace allowlisted targets atomically. A successful response is valid only when:

```text
workflow=context-upgrade
project_name=dp-api
updated_files=<non-empty list>
backup_directory=/suite/context/backup/<generated-backup>
input_cleaned=true
errors=[]
```

The input archive may be removed only after all replacements and post-update checks succeed. On failure, the original targets and `context-upgrade.zip` must remain available for diagnosis or retry.

## 8. Rollback

Rollback uses the exact timestamped backup reported by the successful upgrade response:

1. stop further context upgrades;
2. inspect the reported directory under `${SBM_SUITE_ROOT}/context/backup`;
3. compare its manifest and files with the updated targets;
4. restore only the affected allowlisted paths, preserving their relative paths;
5. rerun repository checks and context validation;
6. retain the failed upgrade evidence until the incident is resolved.

Do not use an unreported backup, a plural backup directory, or a broad recursive copy. Git history can supplement investigation but does not replace the upgrade backup or authorize destructive reset commands.

## 9. Validation performed

Repository-local validation for this workflow consists of:

```bash
bash -n scripts/context-deploy.sh
bash -n scripts/context-upgrade.sh
```

An isolated temporary harness with a fake contract/backend and synthetic ZIPs
also validates missing or invalid arguments, unavailable or incompatible
contracts, manifest/patch phase rules and one valid case for every phase. It
does not read the real `.env.dev`, clean shared outputs or call a real upgrade.

Static searches verify the absence of legacy mount paths, plural backup paths
and DP-API-local project-tree references in active context workflows. A live
endpoint call is intentionally excluded because it would affect shared context
state and invoke an external service.

Live closure-export validation:

```text
Command: ./scripts/context-deploy.sh implementation-closure DP-QA-001
Contract version: ea52d21594ed827bee97759500386658293f46b74fb0636fa3960003e47dca55
Export status: completed
Indexed sources: 15
Indexed chunks: 1107
Errors: none
```

The export completed and generated the reviewed package. This evidence does not claim that the resulting context upgrade has already been applied.

## 10. Current limitations

- End-to-end success depends on the mounted suite context and a compatible SBM-AI-ASSISTANT backend.
- The client can preserve the input on transport and HTTP failure; once a backend has accepted a request, transactionality and cleanup ordering are backend responsibilities.
- The upgrade client safely inspects manifest and member paths but does not extract or independently apply archive contents.
- `context/qa-results.md` is optional for activation and progress, but implementation closure requires a non-empty QA evidence file.
- The supplied SonarScanner log proves successful scanner execution and upload, not a server-side Quality Gate result.
- Git branch creation, commit and push remain manual.
