# Context and Documentation lifecycle

> **Project:** DP-API
>
> **Purpose:** Describe how DP-API uses the canonical suite-wide workflows.

## Ownership

The Context and Documentation lifecycle is owned and managed exclusively from:

```text
SBM-SUITE/context
```

DP-API has no local wrappers or implementations for these workflows.

Project Registry, canonical project paths, lifecycle validation, Git and QA
evidence, HTTP payloads, archive handling, backups, Context updates and
Documentation reconciliation remain global responsibilities.

## Canonical commands

Run the canonical commands from the root of `SBM-SUITE/context`:

```bash
./scripts/context-deploy.sh dp-api ...
./scripts/context-upgrade.sh
./scripts/documentation-deploy.sh
./scripts/documentation-upgrade.sh
```

Context upgrade obtains `project_name` from its reviewed package manifest.
Documentation deploy and upgrade accept no project argument; reconciliation
remains global and multi-project.

## Project Tree

DP-API has no local `project-tree.sh` or compatibility launcher. The single
canonical implementation is used directly:

```bash
./scripts/project-tree.sh
```

Its generated suite-wide tree is:

```text
project-tree.txt
```

## Usage

Use the current argument contract published by the global scripts. Examples:

```bash
# From SBM-SUITE/context
./scripts/context-deploy.sh dp-api \
  planning-activation \
  '[{"objective_id":"DP-MATERIAL-001","objective":"Implementar Material","status":"active","priority":3,"target_date":"N/A","branch":"FEATURE-material-integration"}]' \
  "Implementar Material"

./scripts/context-upgrade.sh
./scripts/documentation-deploy.sh
./scripts/documentation-upgrade.sh
```

Context and Documentation deploy/upgrade commands can modify shared exchange
state or call external services. They are validated by the global Context
implementation rather than by DP-API.
