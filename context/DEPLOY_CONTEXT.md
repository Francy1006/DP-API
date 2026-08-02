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

Run after collecting the relevant QA evidence:

```bash
./scripts/context-deploy.sh
```

The script performs the following sequence:

1. reads and validates the required variables from `.env.dev`;
2. validates the global prompt and format files;
3. prepares the global input and output directories and removes stale exchange artifacts while preserving `.gitkeep`;
4. generates `/suite/context/output/SYS_PROMPT.md` from the global prompt for `dp-api`;
5. requires and runs the executable global `project-tree.sh`, then requires the resulting global `project-tree.txt`;
6. captures unstaged and staged Git diff, modified paths, untracked non-ignored paths and optional `context/qa-results.md`;
7. excludes `.env` and `.env.*` paths from both the diff and changed-file list;
8. sends `POST /contexts/export` to `AI_ASSISTANT_URL`;
9. requires a completed response for workflow `context-deploy`, project `dp-api`, without reported errors;
10. prints the global output and response paths.

The backend payload contains exactly these path semantics:

```text
project_name=dp-api
workflow=context-deploy
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
4. creates or reuses only `${SBM_SUITE_ROOT}/context/backup`;
5. calls `POST /contexts/upgrade` with project `dp-api` and workflow `context-upgrade`;
6. preserves the ZIP when the request fails at transport or HTTP level;
7. validates `workflow`, `project_name`, `errors`, `input_cleaned`, non-empty `updated_files` and `backup_directory` in a successful response;
8. requires the reported backup to be under `/suite/context/backup/`;
9. verifies the backend removed the input ZIP only after success;
10. prints every updated file and the generated backup path.

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

Static searches verify the absence of legacy mount paths, plural backup paths and DP-API-local project-tree references in active context workflows. A real endpoint call is not part of static validation because it would clean shared input/output directories and invoke an external service.

## 10. Current limitations

- End-to-end success depends on the mounted suite context and a compatible SBM-AI-ASSISTANT backend.
- The client can preserve the input on transport and HTTP failure; once a backend has accepted a request, transactionality and cleanup ordering are backend responsibilities.
- The scripts validate response metadata but do not independently inspect backend-created archive contents or restored files.
- `context/qa-results.md` is optional, so missing QA evidence is reported in the payload rather than synthesized.
- No repository-local automated tests currently mock the context backend; syntax and static contract checks are the available local verification.
