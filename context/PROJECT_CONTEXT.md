# PROJECT_CONTEXT.md

> **Last updated:** 2026-08-02
>
> **Purpose**
>
> Persistent technical, architectural and planning context for `DP-API`.
>
> **Accuracy note**
>
> Implemented behavior, QA results, database state and deployment status require repository or execution evidence. Active objectives, pending objectives and completed-objective history remain explicitly separated.

## 1. Executive summary

`DP-API` is the client-facing business API for Ditaly Pasta inside SBM Suite.

The evidence-based QA procedure and lifecycle-aware context workflow covered by `DP-QA-001` are implemented and closed. Current operational work remains in the pending Service, Material integration, Product endpoint retirement, security and production-hardening objectives.

## 2. Project purpose

Provide validated client-facing ERP operations for authorized Ditaly Pasta users.

Canonical boundary:

```text
Client business operation
→ DP-API

Internal platform operation
→ SBM-API

Physical database structure
→ SBM-DB / Flyway

AI-assisted operation
→ SBM-AI-ASSISTANT Tool
→ DP-API
```

`DP-API` must not provision tenants, create franchises, activate uncontracted modules or expose global platform administration.

## 3. Active objectives

| ID | Objective | Status | Priority | Target date | Branch | Documentation |
|---|---|---|---:|---|---|---|

Rules:

- this section contains only objectives currently being addressed;
- status is always `active`;
- implementation must not begin without an assigned branch;
- every objective change must synchronize with `SBM-SUITE/context/PROJECT_CONTEXT.md`;
- completed objectives are removed and appended only to `SBM-SUITE/context/COMPLETED_OBJECTIVES.md`.

## 4. Pending objectives

| ID | Objective | Status | Priority | Target date | Branch | Documentation |
|---|---|---|---:|---|---|---|
| DP-SERVICE-001 | Create the dedicated Service app after validating the current database source | pending | 4 | N/A | N/A | Service architecture and roadmap documentation |
| DP-MATERIAL-001 | Migrate and validate the SBM-MANAGER Material consumer | pending | 4 | N/A | N/A | Material integration documentation |
| DP-PRODUCT-RETIRE-001 | Retire the duplicate SBM-API Product endpoint after the remaining consumer audit | pending | 3 | N/A | N/A | Product API migration documentation |

Rules:

- this section contains only approved objectives not yet started;
- status is always `pending`;
- a branch must be assigned when an objective becomes active;
- completed objectives never remain here;
- every objective change must synchronize with `SBM-SUITE/context/PROJECT_CONTEXT.md`.

## 5. Scope and ownership

`DP-API` owns normal client-facing Ditaly Pasta operations, including:

- products;
- materials;
- services;
- catalogs;
- prices and permitted commercial configuration;
- providers;
- branches;
- agreements;
- tickets;
- client-scoped users, roles and permissions.

It does not own:

- franchise or tenant provisioning;
- subscription and plan administration;
- global platform configuration;
- internal SBM users;
- physical PostgreSQL schema changes;
- AI orchestration.

## 6. Architecture

The project uses a hybrid architecture.

Simple CRUD modules may use:

```text
URL/router
→ ViewSet
→ serializer
→ unmanaged Django model
→ PostgreSQL
```

Business-critical domains use:

```text
REST adapter
→ application use case
→ domain entity or policy
→ repository port
→ Django ORM adapter
→ Flyway-owned PostgreSQL
```

Accepted reference vertical:

```text
Product
→ products app
```

Current repository ownership:

```text
Product  → products
Material → material
Service  → products (legacy CRUD mapping)
Catalog  → products (legacy CRUD mapping)
Ticket   → ticket
```

The intended domain boundary keeps Service and Catalog independent, but their
dedicated Django apps have not been created yet.

Domains must not be merged merely to reduce duplication.

## 7. Runtime and containers

Known local runtime:

| Component | Value |
|---|---|
| Compose service | `api` |
| Container | `dp-core` |
| Internal port | `8000` |
| Host port | `8081` |
| Shared network | `sbm-network` |
| Development server | Django `runserver` |
| Database | Independent PostgreSQL and Flyway stack |

Known local endpoint:

```text
http://localhost:8081/admin
```

Docker remains the official development and QA runtime.

### Context workflow locations

The repository is located at `dp/DP-API` within SBM Suite and is mounted in the
assistant container at:

```text
/suite/dp/DP-API
```

DP-API does not configure or resolve the lifecycle script location. All Context,
Documentation and Project Tree commands run from the local
`SBM-SUITE/context` repository root, whose canonical scripts own their resource
resolution.

Shared context resources are owned globally:

| Resource | Host path derived from `SBM_SUITE_ROOT` | Container path |
|---|---|---|
| Prompt | `${SBM_SUITE_ROOT}/context/SYS_PROMPT.md` | `/suite/context/SYS_PROMPT.md` |
| Format | `${SBM_SUITE_ROOT}/context/FORMAT_CONTEXT.md` | `/suite/context/FORMAT_CONTEXT.md` |
| Input | `${SBM_SUITE_ROOT}/context/input` | `/suite/context/input` |
| Output | `${SBM_SUITE_ROOT}/context/output` | `/suite/context/output` |
| Backup | `${SBM_SUITE_ROOT}/context/backup` | `/suite/context/backup` |
| Tree script | `${SBM_SUITE_ROOT}/context/scripts/project-tree.sh` | `/suite/context/scripts/project-tree.sh` |
| Tree output | `${SBM_SUITE_ROOT}/context/project-tree.txt` | `/suite/context/project-tree.txt` |

DP-API has no local wrappers or implementations for Context and Documentation.
Their deploy and upgrade commands must be run from `SBM-SUITE/context`, using
the canonical scripts in its `scripts/` directory. Project Registry, canonical
mappings, lifecycle validation, Git/QA evidence, HTTP payloads, ZIP handling,
backups and multi-project Documentation reconciliation are global
responsibilities.

DP-API does not own a Project Tree script. Consumers use the single canonical
`${SBM_SUITE_ROOT}/context/scripts/project-tree.sh` implementation directly.

No live lifecycle request is part of repository-local validation because the
global commands mutate shared exchange state and depend on external services.

Workflow validation and end-to-end behavior are tested and maintained by the
global Context implementation, not duplicated in DP-API.

## 8. Configuration

Current configuration characteristics:

- `.env.dev` is loaded directly by Django settings;
- production environment loading exists but is not active;
- Compose and Django currently use overlapping environment-loading mechanisms;
- PostgreSQL search path is:

```text
ditaly_pasta,sbm_business,public
```

Required rules:

- secrets remain outside Git;
- test, local and production configuration remain separated;
- CORS must not remain permissive outside development;
- environment selection must become runtime-driven before production.

## 9. Modules

| Module | Responsibility | Architecture | Status |
|---|---|---|---|
| `users` | Business users and user types | layered | active |
| `authz` | Roles, permissions and restrictions | layered | active |
| `documentation` | Business instruction metadata | layered | active |
| `products` | Product and shared item lookups | hybrid / hexagonal Product | active |
| `material` | Canonical Material vertical | hexagonal | active |
| `products` (Service model) | Legacy Service CRUD pending extraction | conventional | active legacy |
| `products` (Catalog model) | Legacy Catalog CRUD pending extraction | conventional | active legacy |
| `providers` | Providers and lookup data | hybrid | active |
| `pricing` | Pricing and fiscal configuration | hybrid | active |
| `sales` | Future sales workflows | undefined | pending |
| `ticket` | Client operational tickets | layered | active |
| `branches` | Branches, platforms and agreements | layered | active |
| `business` | Shared business lookup concepts | layered | active |

The global `${SBM_SUITE_ROOT}/context/project-tree.txt` must be used by the
context workflow to detect meaningful structural changes without copying the
raw tree into this file.

Relevant reusable components currently present in the repository include:

- workflow and QA scripts under `scripts/` plus the container bootstrap in `core/entrypoint.sh`;
- Product, Material and Provider application use cases and repository adapters;
- Product and Material price-calculation application modules;
- shared pricing domain policies and `pricing/infrastructure/transactions.py`;
- unmanaged ORM mappings in each app's `models.py`;
- domain repository ports, DTOs, commands, clocks and presentation adapters inside the hexagonal verticals.

There is no generic `services/` package. Reusable business services are kept
inside the owning vertical rather than generalized across domains prematurely.

## 10. Data model ownership

PostgreSQL, Flyway and DBML are authoritative for business schemas.

Relevant schemas:

```text
ditaly_pasta
sbm_business
public
```

Rules:

- Django models remain unmanaged for Flyway-owned tables.
- Do not run `makemigrations` or `migrate` for business tables.
- Model changes do not imply database changes.
- Structural database changes require separate SBM-DB scope.
- Read-only schema inspection is allowed.
- Runtime, Flyway, DBML and ORM mappings must remain synchronized.

Known legacy concerns include dangling Material price identifiers and historical shared Product Price records. These must not be silently deleted or normalized.

## 11. API surface

General endpoints:

| Method | Path | Purpose |
|---|---|---|
| GET | `/` | Root |
| GET | `/api/` | API root |
| GET | `/api/health/` | Health |
| GET | `/api/info/` | Service information |
| GET/POST | `/admin/` | Django admin |
| GET/POST | `/api-auth/` | DRF session authentication |
| POST | `/api-token-auth/` | Token generation |

Validated Product contract:

| Method | Path | Status |
|---|---|---|
| GET | `/api/products/` | implemented |
| POST | `/api/products/` | implemented |
| GET | `/api/products/{id}/` | implemented |
| PATCH | `/api/products/{id}/` | implemented |
| HEAD | `/api/products/` | implemented |
| HEAD | `/api/products/{id}/` | implemented |
| POST | `/api/products/{id}/delete/` | implemented |
| PUT | `/api/products/{id}/` | disabled, HTTP 405 |
| DELETE | `/api/products/{id}/` | disabled, HTTP 405 |

Other registered resource groups include users, authorization, providers, pricing, branches, agreements, tickets, catalogs and supporting lookups.

Every endpoint must be validated individually before use by a frontend or AI Tool.

## 12. Authentication and authorization

Current global DRF configuration includes:

```text
SessionAuthentication
BasicAuthentication
IsAuthenticated
```

Known inconsistency:

```text
/api-token-auth/
```

exists, but token authentication is not confirmed as a global accepted authentication class.

Two user concepts currently coexist:

1. Django authentication users.
2. Business users in the `users` app.

Target authorization chain:

```text
identity
→ tenant or franchise
→ active modules
→ role
→ permission
→ restriction
→ requested object
→ action
```

Tenant isolation and object-level authorization remain unresolved production requirements.

## 13. Integrations

Current and planned integrations:

| Source | Target | Purpose | Status |
|---|---|---|---|
| SBM-MANAGER | DP-API | Client operations | active |
| DP-API | PostgreSQL | Business persistence | active |
| DP-API | Flyway-owned schema | Schema consumption | active |
| SBM-AI-ASSISTANT | DP-API | Explicit AI Tools | planned |
| DP-API | SBM-API | Selected cross-platform workflows | proposed |
| Context scripts | SBM-AI-ASSISTANT | Context export and upgrade | active |

Product frontend integration is accepted.

Material frontend integration remains pending.

## 14. Implemented behavior

### Product

The Product vertical is the accepted reference capability.

Implemented and validated behavior includes:

- database-generated SKU;
- immutable Provider after creation;
- server-controlled confirmation audit;
- logical deletion;
- audit log formatting;
- atomic entity-version increments;
- idempotent PATCH behavior;
- Product Price creation and versioning;
- protection of shared legacy Price records;
- canonical response labels;
- disabled PUT and physical DELETE;
- SBM-MANAGER integration.

### Material

Material is isolated in the dedicated `material` app.

Implemented behavior includes:

- canonical dedicated ownership;
- preserved `/api/materials/` contract;
- lifecycle, confirmation and audit behavior;
- logical deletion;
- entity versioning;
- Price versioning;
- compatibility with legacy dangling Price identifiers.

### Provider

The Provider vertical and selector response were repaired and locally validated.

No current objective authorizes redesigning Product or Material.

### QA and context lifecycle

Implemented workflow behavior includes:

- explicit `planning-activation`, `implementation-progress` and `implementation-closure` phases;
- mandatory objective identifiers for every context export;
- contract preflight through `GET /contexts/contract` before exchange cleanup;
- bounded QA evidence written by `qa-check.sh` to `context/qa-results.md`;
- client-side ZIP manifest and physical-patch preflight before backend upgrade;
- mandatory project/global objective and QA synchronization during closure;
- single global completed-objective history grouped by project.

## 15. Validation evidence

Latest recorded Product QA evidence:

| Evidence | Result |
|---|---|
| Product tests | 54 passed |
| Complete suite | 71 passed |
| Django system check | 0 issues |
| Pytest coverage including branches | 73.64% |
| Line coverage | 78.44% |
| Branch coverage | 33.19% |
| SonarQube overall coverage | 88.4% |
| Security rating | A |
| Reliability rating | A |
| Maintainability rating | A |
| Open Security issues | 0 |
| Open Reliability issues | 0 |
| Open Maintainability issues | 0 |
| Security hotspots | 0 |
| Duplicated lines | 2.7% |
| Quality Gate | Passed |

Recorded date:

```text
2026-07-29
```

This evidence applies to the recorded Product-focused scope. It does not prove the complete new DP-API QA procedure has been implemented.

### DP-QA-001 closure evidence

Validated on:

```text
2026-08-02
```

```text
Configured pytest scope          65 passed
Failed tests                     0
Pytest exit code                 0
Total configured coverage        88%
Coverage artifact                coverage.xml
SonarScanner exit code           0
Sonar analysis                   ANALYSIS SUCCESSFUL
SonarScanner execution           EXECUTION SUCCESS
Indexed Python files             40
```

The supplied scanner log proves successful analysis execution and upload. It does not include a server-side Quality Gate result for this run. No deployment, database or migration execution is evidenced.

## 16. Database and migration impact

Current context changes do not establish a new database or migration change.

Stable rules:

- no Django migration was created for Product or Material;
- PostgreSQL structure was not altered by those application changes;
- future Service work requires current PostgreSQL, Flyway and DBML inspection;
- database changes require separate SBM-DB authorization.

## 17. Security considerations

Known risks:

- permissive CORS in development configuration;
- Basic authentication globally enabled;
- token endpoint and accepted authentication classes are inconsistent;
- two user systems coexist;
- tenant isolation is not confirmed;
- object-level authorization is not confirmed;
- audit actor fields may still be supplied through transitional business-user inputs;
- development server remains in use;
- local environment files require strict secret handling.

Future AI Tools must preserve user identity, tenant scope, API authorization and auditability.

## 18. Accepted risks and constraints

| Risk | Level | Status | Constraint |
|---|---:|---|---|
| Authentication and business-user mapping unresolved | 5 | open | Requires separate security objective |
| Tenant isolation not fully evidenced | 5 | open | Must block production acceptance |
| Service schema not yet verified | 4 | open | No Service implementation before database inspection |
| Material frontend integration pending | 3 | open | Backend remains canonical |
| Product endpoint remains duplicated in SBM-API | 3 | accepted temporarily | Retire only after consumer audit |
| Trigger concurrency strategy requires hardening | 3 | accepted temporarily | Database-owned future task |
| Development server and fixed startup delay | 3 | open | Production hardening pending |

## 19. Completed work

- DP-API established as the client-facing API.
- Product vertical implemented and accepted.
- Product Price lifecycle implemented.
- Product integrated with SBM-MANAGER.
- Material extracted to its dedicated app.
- Material backend behavior validated.
- Provider vertical and selector repaired.
- Product tests standardized under `products/tests/`.
- Coverage tooling configured.
- SonarQube configured locally.
- Product Quality Gate passed.
- Context export and upgrade scripts introduced.

## 20. Pending work

1. Standardize full-project test inventory and evidence beyond the currently configured Product scope.
2. Define coverage and SonarQube thresholds for every canonical module.
3. Validate tenant isolation and object permissions.
4. Resolve Django versus business-user identity.
5. Migrate and validate the SBM-MANAGER Material consumer.
6. Validate the Service database source.
7. Create the dedicated Service app.
8. Retire the duplicate Product endpoint after consumer audit.
9. Extend QA coverage to Material and future modules.
10. Add CI/CD Quality Gate enforcement.
11. Harden production configuration, server and health checks.
12. Implement the first read-only AI Tool.

## 21. Required behavior

Before changes:

1. Read applicable global and project contexts.
2. Inspect current Git status and repository structure.
3. Identify canonical domain and API ownership.
4. Verify PostgreSQL, Flyway and DBML when database-sensitive.
5. Report missing evidence.
6. Register the objective as active or pending and assign its branch before implementation.

During changes:

- preserve user modifications;
- modify only authorized scope;
- avoid speculative refactors;
- do not run unauthorized migrations;
- do not mutate PostgreSQL structure;
- preserve public contracts unless explicitly changed;
- keep domains in their canonical apps;
- validate one step at a time;
- do not perform Git commit or push unless requested.

After changes:

- report created, modified, moved and deleted files;
- report tests and checks executed;
- report validation not executed;
- report database and migration impact;
- report security risks;
- synchronize project and global contexts;
- when completed, remove the objective from active and pending sections and append it only to `SBM-SUITE/context/COMPLETED_OBJECTIVES.md`;
- update related documentation only after implementation, QA validation and final context closure.

## 22. Historical decisions

Important accepted historical decisions:

- Client operations belong to DP-API.
- Internal platform operations belong to SBM-API.
- Flyway owns business schema changes.
- AI uses APIs and Tools, not direct database writes.
- Migrations occur one vertical capability at a time.
- Product is the reference hexagonal vertical.
- Product, Material, Service, Catalog and Ticket remain independent domain boundaries; Service and Catalog dedicated apps are still pending.
- README describes stable intended behavior.
- PROJECT_CONTEXT preserves current operational state, constraints and pending work; completed-objective history belongs only to the global completed-objectives register.
- Product-focused SonarQube scope must not hide application code.
- Material was restored after a premature shared generalization caused degraded quality metrics.
- Service implementation must stop when current database evidence is unavailable.

The previous 3,000-line context has been consolidated into the canonical sections above. Git history remains the authoritative detailed historical record.

## 23. Related documentation

Relevant documentation domains:

- DP-API;
- Development;
- Architecture;
- Roadmap;
- QA and Testing;
- Security and DevSecOps;
- Data Architecture;
- AI Engineering;
- DevOps.

Repository-relative documentation paths must be added when the documentation structure is finalized.

## 24. Document boundary

This file records current project purpose, active and pending objectives, architecture, implementation state, evidence, risks, completed work summaries and pending work. Completed-objective history is stored only in `SBM-SUITE/context/COMPLETED_OBJECTIVES.md`.

It does not replace:

- `context/QA_CONTEXT.md`;
- `context/DEPLOY_CONTEXT.md`;
- live repository inspection;
- PostgreSQL, Flyway or DBML;
- raw test or SonarQube reports;
- API reference documentation;
- deployment credentials;
- complete historical Git records.
