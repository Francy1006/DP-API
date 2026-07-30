# DEPLOY_CONTEXT.md

> **Project:** DP-API
>
> **Purpose:** Define the `context-deploy` workflow executed after DP-API QA to prepare, update, validate, and apply project contexts.

## 1. Scope

`context-deploy` does not deploy application infrastructure.

It updates only:

```text
DP-API/context/PROJECT_CONTEXT.md
DP-API/README.md
SBM-SUITE/PROJECT_CONTEXT.md
SBM-SUITE/context/SUITE_CONTEXT.md
SBM-SUITE/README.md
```

It must not update:

```text
QA_CONTEXT.md
BUSINESS_CONTEXT.md
DEPLOY_CONTEXT.md
SYS_PROMPT.md
```

QA context updates belong to a future `qa-context-update` workflow.

## 2. Trigger

After manually completing QA, the user executes:

```bash
./scripts/context-deploy.sh
```

The script must send:

```text
project_name=dp-api
workflow=context-deploy
```

## 3. Working folders

```text
SBM-SUITE/context/
├── SYS_PROMPT.md
├── input/
│   ├── zip/
│   └── exported/
└── output/
```

Ignore with Git:

```text
context/output/*
context/input/zip/*
context/input/exported/*
```

## 4. Initial cleanup

Before processing, clean completely:

```text
SBM-SUITE/context/output/
SBM-SUITE/context/input/zip/
SBM-SUITE/context/input/exported/
```

Do not delete the directories.

## 5. SBM-AI-ASSISTANT responsibilities

`context-deploy.sh` calls an SBM-AI-ASSISTANT FastAPI endpoint or function.

SBM-AI-ASSISTANT must:

1. discover applicable global and DP-API contexts;
2. read Markdown sources;
3. chunk and embed them;
4. index them in Qdrant;
5. create the ChatGPT input package;
6. copy and parameterize `SYS_PROMPT.md`.

Collections:

```text
sbm_contexts → suite and project contexts
sbm_docs     → Confluence documentation
```

Do not mix them.

Git Markdown files remain the source of truth. Qdrant is only the retrieval index.

## 6. Qdrant metadata

Each chunk should include:

```text
project
project_name
repository
context_type
domain
section
source_path
updated_at
version
is_active
content_hash
```

## 7. ChatGPT input package

Do not export raw vectors or embeddings.

Export the original contexts and relevant project documentation as:

```text
SBM-SUITE/context/output/context-package.zip
```

Recommended content:

```text
SBM-SUITE/PROJECT_CONTEXT.md
SBM-SUITE/README.md
SBM-SUITE/context/SUITE_CONTEXT.md
SBM-SUITE/context/BUSINESS_CONTEXT.md
SBM-SUITE/context/QA_CONTEXT.md
DP-API/context/PROJECT_CONTEXT.md
DP-API/context/QA_CONTEXT.md
DP-API/context/DEPLOY_CONTEXT.md
DP-API/README.md
manifest.json
```

Preserve all folder names and filenames.

## 8. System prompt

Template:

```text
SBM-SUITE/context/SYS_PROMPT.md
```

Generated copy:

```text
SBM-SUITE/context/output/SYS_PROMPT.md
```

Replace its project parameter with:

```text
project_name=dp-api
```

The generated prompt must instruct ChatGPT to:

1. correlate DP-API with `SUITE_CONTEXT.md` and `BUSINESS_CONTEXT.md`;
2. inspect global and DP-API QA contexts without modifying them;
3. use previously completed QA evidence;
4. update DP-API and SBM-SUITE README files;
5. update both `PROJECT_CONTEXT.md` files;
6. update `SUITE_CONTEXT.md` only when suite interaction changed;
7. preserve paths and filenames;
8. return only allowed updated files in one ZIP;
9. never modify QA, Business, Deploy, or System Prompt contexts.

## 9. Manual ChatGPT stage

The user uploads:

```text
context-package.zip
SYS_PROMPT.md
```

ChatGPT returns one ZIP containing only permitted updates.

## 10. Returned ZIP intake

The user places the ZIP in:

```text
SBM-SUITE/context/input/zip/
```

Only one candidate ZIP should exist.

Validate:

- ZIP format;
- permitted paths;
- exact filenames;
- `project_name`;
- UTF-8 Markdown;
- no Zip Slip;
- no absolute paths;
- no symbolic links;
- no duplicate paths;
- no unexpected extensions;
- acceptable file and archive size.

## 11. Asynchronous import

The user asks the existing Slack chatbot to update SBM Suite context.

SBM-AI-ASSISTANT processes it through FastAPI or an agent Tool:

1. detect ZIP in `context/input/zip/`;
2. validate it;
3. extract it into `context/input/exported/`;
4. preserve all paths;
5. validate allowed files;
6. generate or validate `manifest.json`;
7. stage replacements;
8. replace files atomically;
9. reindex changed Markdown in Qdrant;
10. clean `context/input/exported/` after success.

Example:

```text
context/input/exported/
├── PROJECT_CONTEXT.md
├── README.md
├── context/
│   └── SUITE_CONTEXT.md
└── DP-API/
    ├── README.md
    └── context/
        └── PROJECT_CONTEXT.md
```

## 12. Manifest

Required:

```json
{
  "project_name": "dp-api",
  "workflow": "context-deploy",
  "allowed_files": [],
  "source_package": "",
  "generated_at": "",
  "content_hashes": {}
}
```

## 13. Atomic replacement

The importer must:

1. validate the complete package;
2. verify all target paths;
3. verify hashes when available;
4. stage all files;
5. replace all targets atomically;
6. reindex changed contexts;
7. report success;
8. clean `exported/`.

No extra backup is required because Git provides version history.

On failure, retain original contexts and do not report success.

## 14. Protected files

Reject any modification to:

```text
SBM-SUITE/context/BUSINESS_CONTEXT.md
SBM-SUITE/context/QA_CONTEXT.md
SBM-SUITE/context/SYS_PROMPT.md
DP-API/context/QA_CONTEXT.md
DP-API/context/DEPLOY_CONTEXT.md
```

Reject files belonging to another project except permitted global SBM-SUITE files.

## 15. README rules

README updates must describe the completed project and may include:

- current architecture;
- canonical app ownership;
- configuration;
- usage;
- runtime;
- endpoints;
- accepted QA state.

## 16. Project context rules

Update DP-API `PROJECT_CONTEXT.md` with:

- completed implementation;
- architecture changes;
- validated QA results;
- current objective;
- pending risks;
- database and migration impact.

Update SBM-SUITE `PROJECT_CONTEXT.md` with:

- suite progress;
- affected project;
- cross-project consequences;
- next global objective.

Update `SUITE_CONTEXT.md` only when architecture, ownership, integrations, containers, shared data flow, Qdrant, or AI-assistant interaction changed.

## 17. Script requirements

Create:

```text
DP-API/scripts/context-deploy.sh
```

It must:

1. use `set -euo pipefail`;
2. resolve paths safely;
3. set `project_name=dp-api`;
4. clean working folders;
5. call SBM-AI-ASSISTANT;
6. wait for export completion;
7. parameterize `SYS_PROMPT.md`;
8. verify ZIP and prompt outputs;
9. print exact output paths;
10. fail immediately on error.

It must not:

- execute QA;
- execute migrations;
- modify PostgreSQL;
- update contexts directly;
- commit or push;
- replace contexts before ChatGPT returns the reviewed ZIP.

## 18. SBM-AI-ASSISTANT interface

Input:

```text
project_name
workflow
source_context_root
output_directory
```

Output:

```text
status
job_id
context_zip_path
system_prompt_path
indexed_source_count
chunk_count
collection_name
errors
```

The process may be asynchronous.

## 19. Logging

Record:

```text
workflow
project_name
job_id
source files
generated package
chunk count
Qdrant collection
imported files
content hashes
start time
finish time
status
error
```

Never log secrets.

## 20. Success criteria

Success requires:

- QA completed previously;
- contexts indexed;
- ChatGPT package generated;
- parameterized prompt generated;
- returned ZIP validated;
- allowed files replaced atomically;
- changed contexts reindexed;
- `exported/` cleaned;
- no protected file modified.

## 21. Stable rules

1. Command: `./scripts/context-deploy.sh`.
2. Project: `dp-api`.
3. SBM-AI-ASSISTANT owns embeddings and ingestion.
4. Qdrant collection: `sbm_contexts`.
5. Confluence remains in `sbm_docs`.
6. ChatGPT receives Markdown, not raw vectors.
7. Preserve paths and filenames.
8. Clean prior artifacts first.
9. Update only Project Context, Suite Context, and README files.
10. Never update QA Context in this workflow.
11. Never update Business Context automatically.
12. Never update Deploy Context automatically.
13. Validate ZIP and manifest.
14. Replace atomically.
15. Git provides history.
16. Clean `exported/` only after success.
