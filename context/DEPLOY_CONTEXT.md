# Context and Documentation lifecycle

> **Project:** DP-API
>
> **Purpose:** Describe DP-API's compatibility entry points for the canonical
> suite-wide workflows.

## Ownership

The only implementations of the Context and Documentation lifecycle live in:

```text
${SBM_SUITE_ROOT}/context/scripts/
```

DP-API retains these local commands only for compatibility:

```text
scripts/context-deploy.sh
scripts/context-upgrade.sh
scripts/documentation-deploy.sh
scripts/documentation-upgrade.sh
```

Each wrapper resolves `SBM_SUITE_ROOT` from the exported environment or the
project-local `.env.dev`, locates the corresponding global script and replaces
its own process with that script using `exec`. All user arguments are forwarded
literally.

Project Registry, canonical project paths, lifecycle validation, Git and QA
evidence, HTTP payloads, archive handling, backups, Context updates and
Documentation reconciliation remain global responsibilities.

## Delegation contract

| Local command | Canonical invocation |
|---|---|
| `scripts/context-deploy.sh ...` | `${SBM_SUITE_ROOT}/context/scripts/context-deploy.sh dp-api ...` |
| `scripts/context-upgrade.sh ...` | `${SBM_SUITE_ROOT}/context/scripts/context-upgrade.sh ...` |
| `scripts/documentation-deploy.sh ...` | `${SBM_SUITE_ROOT}/context/scripts/documentation-deploy.sh dp-api ...` |
| `scripts/documentation-upgrade.sh ...` | `${SBM_SUITE_ROOT}/context/scripts/documentation-upgrade.sh ...` |

The upgrade workflows obtain `project_name` from their reviewed package
manifest. The Documentation deploy identifies `dp-api` only as the originating
project; reconciliation remains global and multi-project.

## Project Tree

DP-API has no local `project-tree.sh` or compatibility launcher. The single
canonical implementation is used directly:

```text
${SBM_SUITE_ROOT}/context/project-tree.sh
```

Its generated suite-wide tree is:

```text
${SBM_SUITE_ROOT}/context/project-tree.txt
```

## Usage

Use the current argument contract published by the global scripts. Examples:

```bash
./scripts/context-deploy.sh \
  planning-activation \
  '[{"objective_id":"DP-MATERIAL-001","objective":"Implementar Material","status":"active","priority":3,"target_date":"N/A","branch":"FEATURE-material-integration"}]' \
  "Implementar Material"

./scripts/context-upgrade.sh
./scripts/documentation-deploy.sh
./scripts/documentation-upgrade.sh
```

Context and Documentation deploy/upgrade commands can modify shared exchange
state or call external services. Repository-local validation therefore checks
wrapper syntax and delegation statically rather than executing live workflows.
