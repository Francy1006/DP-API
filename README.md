```text
                                                       █──▄────▄▄▄▄▄▄▄────▄───
                                                       █─▀▀▄─▄█████████▄─▄▀▀──
                                                       █─────██─▀███▀─██──────
                                                       █───▄─▀████▀████▀─▄────
                                                       █─▀█────██▀█▀██────█▀──
        ▄████▄   ▒█████   ███▄    █  ██ ██░██████ ▄▄▄  █
       ▒██▀ ▀█  ▒██▒  ██▒ ██ ▀█   █  ██ █░ ▓█   ▀▒████▄█
       ▒▓█    ▄ ▒██░  ██▒ ██  ▀█ █▒  ████░ ▒███  ▒██   █▄
       ▒▓▓▄ ▄██ ▒██   ██░ ██▒  ▐▌█▒  ██ █▄ ▒▓█  ▄░████████
       ▒ ▓███▀ ░░ ████▓▒  ██░   ▓█░  █▒ ██▄░▒████▒▓█  █▒
       ░ ░▒ ▒  ░░ ▒░▒░▒░ ░ ▒░   ▒ ▒  ▒▒ ▓▒░░ ▒░ ░▒▒   ▓▒█░
         ░  ▒     ░ ▒ ▒░ ░ ░░   ░ ▒  ░▒ ▒░ ░ ░  ░ ▒   ▒▒ ░
       ░        ░ ░ ░ ▒     ░   ░ ░ ░ ░░ ░    ░    ░   ▒
       ░ ░          ░ ░           ░ ░  ░      ░  ░     ░  ░
       ░
       ▄▄▄▄▄▄▄▄ ▄▄▄▄▄▄▄▄ ▄▄▄▄▄▄▄▄ ▄▄▄▄▄▄▄▄ ▄▄▄▄▄▄▄▄ ▄▄▄▄▄▄▄▄
      █ ▄▄▄ █ ▀▀ ▄▀ ▀▄▀ █ ▄▄▄ █ ▄▀ ▀▄▀ █ ▄▄▄ █ ▄▄▄ █ ▀▀ ▄▀ ▀▄
      █ ███ █ ▀ ▀▄█ ▄ ▀ █ ███ █ ▀▄█ ▄ ▀ █ ███ █ ███ █ ▀ ▀▄█ ▄
      █▄▄▄█ █ █▄▀ █ ▀█ █ █▄▄▄█ █▄▀ █ ▀█ █▄▄▄█ █▄▄▄█ █ █▄▀ █ ▀
      ▄▄▄▄▄▄█ ▀▄█▄▀ ▀ █▄█▄▄▄▄▄█ ▀▄█▄▀ ▀ █▄▄▄▄▄█▄▄▄▄▄█ ▀▄█▄▀ ▀

    █████████████████████████████████████████████████████████████████
    ██  ║                                                       ║  ██
    ██  ║               ░▒▓ DP - API ▓▒░                        ║  ██
    ██  ║                                                       ║  ██
    ██  ║    ┌─────────────────────────────────────────────┐    ║  ██
    ██  ║    │  > Ditaly Pasta Client-Facing ERP API       │    ║  ██
    ██  ║    │  > Products, Prices, Providers, Branches    │    ║  ██
    ██  ║    │  > Configurable business operations         │    ║  ██
    ██  ║    │  > AI-ready REST integration                │    ║  ██
    ██  ║    │  > STATUS: ACTIVE / IN DEVELOPMENT          │    ║  ██
    ██  ║    └─────────────────────────────────────────────┘    ║  ██
    ██  ║                                                       ║  ██
    ██  ║         ░▒▓ CLIENT DOMAIN ACCESS GRANTED ▓▒░          ║  ██
    ██  ║                                                       ║  ██
    ██  ╚═══════════════════════════════════════════════════════╝  ██
    ██                                                             ██
    █████████████████████████████████████████████████████████████████
```

# DP-API

Client-facing REST API for the Ditaly Pasta business domain within **SBM Suite**.

`dp-api` enables authorized client users to operate and configure the ERP through
stable REST contracts without depending on the internal `sbm-api` for routine
business operations.

## Role within SBM Suite

```text
Client user
→ SBM Manager / client application / approved AI channel
→ DP-API
→ validated Ditaly Pasta domain operation
→ PostgreSQL managed by Flyway
```

```text
Client operation     → dp-api
Platform operation   → sbm-api
```

`dp-api` owns client-facing business capabilities. `sbm-api` remains responsible
for franchise and tenant provisioning, contracted modules, global configuration,
internal administration, and other platform-level operations.

## Project status

- Client-facing domain boundary implemented.
- Docker-based local runtime.
- PostgreSQL integration through the shared `sbm-network`.
- Flyway-managed business schemas.
- Hybrid architecture with hexagonal verticals.
- Product and Material separated into canonical apps.
- Dedicated Material and Ticket apps; legacy Service and Catalog mappings remain in `products` pending extraction.
- Django Jazzmin administration interface.
- Automated tests, coverage reports, and SonarQube integration.
- Ready for integration with `sbm-manager` and approved AI Tools.

## Technology stack

- Python 3.11
- Django 4.2
- Django REST Framework
- PostgreSQL
- Flyway
- Django Filter
- Django CORS Headers
- Django Jazzmin
- Docker Compose
- Pytest
- pytest-django
- pytest-cov
- SonarQube Community Build

## Current app ownership

| Domain | Django app | Responsibility |
|---|---|---|
| Product | `products` | Product lifecycle, pricing orchestration, audit, confirmation and logical deletion |
| Material | `material` | Material lifecycle, pricing, legacy compatibility and REST API |
| Service | `products` (legacy) | Current Service model, serializer, ViewSet and `/api/services/`; dedicated app remains pending |
| Catalog | `products` (legacy) | Current Catalog model, serializer, ViewSet and `/api/catalogs/`; dedicated app remains pending |
| Ticket | `ticket` | Client-facing ticket lifecycle and operational workflow |
| Pricing | `pricing` | Shared prices, price configurations and fiscal calculation infrastructure |
| Providers | `providers` | Providers, banks, regions, districts and classifications |
| Branches | `branches` | Branches, platforms and agreements |
| Users | `users` | Client-scoped business users and tokens |
| Authorization | `authz` | Roles, permissions and restrictions |
| Business | `business` | Shared business classifications |
| Documentation | `documentation` | Operational instruction models |
| Sales | `sales` | Sales-domain capabilities |

New domain work should not be placed inside another app merely because both use
the same lookup tables or database schema. Service and Catalog are documented
legacy exceptions awaiting dedicated extraction.

## Architecture

DP-API uses a **hybrid architecture**.

Simple CRUD-oriented modules may use the conventional Django flow:

```text
URL/router
→ ViewSet
→ serializer
→ unmanaged Django model
→ PostgreSQL
```

Business-critical modules use Hexagonal Architecture:

```text
REST adapter / controller
→ application use case
→ domain entity, policy and repository port
→ Django ORM repository adapter
→ Flyway-owned PostgreSQL schema
```

Product and Material are implemented as hexagonal verticals. Ticket has a
dedicated Django app. Service and Catalog remain conventional CRUD resources in
`products`; they are separate domain boundaries but not yet dedicated apps.
Shared code is limited to genuine cross-domain infrastructure or stable shared
value objects.

## Database ownership

PostgreSQL and Flyway run in an independent database stack. DP-API does not own
or provision the physical schema.

```text
DP-API
→ Django/DRF application
→ unmanaged ORM mappings

SBM-DB / Flyway
→ schemas
→ tables and columns
→ constraints and indexes
→ triggers and functions
→ versioned database migrations
```

The configured PostgreSQL search path is:

```text
ditaly_pasta,sbm_business,public
```

Do not run Django schema migrations for Flyway-owned business tables:

```bash
python manage.py makemigrations
python manage.py migrate
```

Structural database changes belong to the database/Flyway project and must be
reviewed separately.

## Requirements

- Docker Desktop or Docker Engine
- Docker Compose
- Current SBM database/Flyway stack
- External Docker network `sbm-network`
- Valid local environment file
- SonarQube stack only when running static analysis

Create the shared network once when it does not exist:

```bash
docker network create sbm-network
```

## Environment configuration

Create `.env.dev`, `.env.prod`, or another environment file outside version
control.

Main variables:

```text
API_PUBLIC_PORT
ALLOWED_HOSTS
CORS_ALLOWED_ORIGINS
DB_HOST
DB_NAME
DB_USER
DB_PASSWORD
DB_PORT
SECRET_KEY
DEBUG
TIME_ZONE
LANGUAGE_CODE
USE_I18N
USE_TZ
DJANGO_SUPERUSER_EMAIL
DJANGO_SUPERUSER_USERNAME
DJANGO_SUPERUSER_PASSWORD
MEDIA_ROOT
MEDIA_URL
STATIC_URL
NODE_ENV
VIRTUAL_HOST
VIRTUAL_PORT
LETSENCRYPT_HOST
LETSENCRYPT_EMAIL
SONAR_HOST_URL
SONAR_TOKEN
DOPPLER_PROJECT
AI_ASSISTANT_URL
SBM_SUITE_ROOT
```

Example local values:

```text
API_PUBLIC_PORT=8081
DB_HOST=postgres
DB_PORT=5432
DEBUG=True
TIME_ZONE=America/Santiago
SONAR_HOST_URL=http://host.docker.internal:9000
```

Never commit credentials, tokens, real hostnames, or production secrets.

## Build and start

Build the API image:

```bash
docker compose --env-file .env.dev build api
```

Start the API:

```bash
docker compose --env-file .env.dev up -d
```

Build and start in one command:

```bash
docker compose --env-file .env.dev up -d --build
```

## Runtime operations

View running containers:

```bash
docker ps
```

View API logs:

```bash
docker compose --env-file .env.dev logs -f api
```

Restart the API:

```bash
docker compose --env-file .env.dev restart api
```

Stop the project:

```bash
docker compose --env-file .env.dev down
```

Open a shell inside the API container:

```bash
docker compose --env-file .env.dev exec api sh
```

Run the Django system check:

```bash
docker compose --env-file .env.dev run --rm --no-deps --entrypoint python api manage.py check
```

## Local URLs

With `API_PUBLIC_PORT=8081`:

```text
Home:       http://localhost:8081/
API root:   http://localhost:8081/api/
Health:     http://localhost:8081/api/health/
API info:   http://localhost:8081/api/info/
Admin:      http://localhost:8081/admin/
DRF login:  http://localhost:8081/api-auth/
Token:      http://localhost:8081/api-token-auth/
```

DP-API and SBM-API run in parallel:

```text
dp-api   → localhost:8081 → container 8000
sbm-api  → localhost:8082 → container 8000
```

## Main REST resources

```text
/api/products/
/api/materials/
/api/services/
/api/catalogs/
/api/tickets/
/api/prices/
/api/price-configuration/
/api/providers/
/api/branches/
/api/users/
/api/roles/
```

Actual fields, filters and permitted methods are defined by each domain contract.

## Usage examples

Health check:

```bash
curl http://localhost:8081/api/health/
```

Authenticated Product list with Basic Authentication:

```bash
curl -u "<username>:<password>"   http://localhost:8081/api/products/
```

Authenticated Material list:

```bash
curl -u "<username>:<password>"   http://localhost:8081/api/materials/
```

Authenticated Service list:

```bash
curl -u "<username>:<password>"   http://localhost:8081/api/services/
```

Create and update payloads must follow the corresponding serializer contract.
Server-controlled fields such as generated identifiers, audit timestamps,
confirmation metadata and derived Price values must not be fabricated by
clients.

## Authentication and authorization

The API supports authenticated access through the configured DRF authentication
classes. Session and Basic Authentication are available for local operation.
The token endpoint is exposed for integrations configured to use DRF tokens.

Every production request must resolve:

```text
identity
→ tenant or franchise context
→ active contracted modules
→ role
→ permission
→ restriction
→ requested business object
```

Client applications must never use unrestricted internal platform credentials.

## Administration

Django Jazzmin is available at:

```text
http://localhost:8081/admin/
```

Administration registrations follow current repository ownership. Product,
Service and Catalog are registered from `products`, Material from `material`,
and Ticket from `ticket`.

## Reusable components

| File name | Path | Description |
|---|---|---|
| `context-deploy.sh` | `scripts/context-deploy.sh` | Exports an explicitly selected lifecycle phase after validating `GET /contexts/contract`. |
| `context-upgrade.sh` | `scripts/context-upgrade.sh` | Safely preflights the ZIP manifest and physical patches against the published contract before `POST /contexts/upgrade`. |
| `documentation-deploy.sh` | `scripts/documentation-deploy.sh` | Exports final documentation evidence only after implementation, QA validation and context closure. |
| `documentation-upgrade.sh` | `scripts/documentation-upgrade.sh` | Applies a reviewed final-state documentation upgrade from the global documentation exchange directory. |
| `coverage.sh` | `scripts/coverage.sh` | Runs the coverage workflow and produces the report consumed by quality tooling. |
| `qa-check.sh` | `scripts/qa-check.sh` | Orchestrates the repository QA sequence. |
| `sonar-scan.sh` | `scripts/sonar-scan.sh` | Runs the configured SonarQube analysis. |
| `project-tree.sh` | `project-tree.sh` | Compatibility launcher for the suite-global `context/project-tree.sh`; it does not generate a tree inside DP-API. |
| `entrypoint.sh` | `core/entrypoint.sh` | Shared API-container startup sequence. |
| `calculate_price.py` | `products/application/calculate_price.py` | Product application service for price calculation. |
| `calculate_price.py` | `material/application/calculate_price.py` | Material application service for price calculation. |
| Product use cases | `products/application/use_cases/` | Reusable Product create, read, list, update and logical-delete application operations. |
| Material use cases | `material/application/use_cases/` | Reusable Material create, read, list, update and logical-delete application operations. |
| Provider use cases | `providers/application/use_cases/` | Reusable Provider create, read, list, update and delete application operations. |
| Product repositories | `products/infrastructure/repositories/` | Django adapters for Product and Product Price repository ports. |
| Material repositories | `material/infrastructure/repositories/` | Django adapters for Material and Material Price repository ports. |
| Provider repository | `providers/infrastructure/repositories/django_provider_repository.py` | Django adapter for the Provider repository port. |
| `transactions.py` | `pricing/infrastructure/transactions.py` | Shared transaction boundary used by pricing-aware application flows. |
| `policies.py` | `pricing/domain/policies.py` | Reusable pricing domain policies. |
| `clock.py` | `products/infrastructure/clock.py` | Product clock adapter for deterministic application workflows. |
| `clock.py` | `material/infrastructure/clock.py` | Material clock adapter for deterministic application workflows. |
| `models.py` | `products/models.py` | Product, catalog and supporting unmanaged ORM mappings. |
| `models.py` | `material/models.py` | Canonical Material unmanaged ORM mappings. |
| `models.py` | `pricing/models.py` | Shared Price and fiscal-configuration ORM mappings. |
| `models.py` | `providers/models.py` | Provider and provider-lookup ORM mappings. |
| `models.py` | `users/models.py` | Business user and user-type ORM mappings used by audit relationships. |
| `models.py` | `authz/models.py` | Role, permission and restriction ORM mappings. |

Business services stay inside their owning application vertical. There is no
generic `services/` package in this repository.

## QA and code quality

Docker is the official QA runtime.

Available scripts:

```text
scripts/coverage.sh
scripts/sonar-scan.sh
scripts/qa-check.sh
```

Grant execution permission when required:

```bash
chmod +x scripts/coverage.sh
chmod +x scripts/sonar-scan.sh
chmod +x scripts/qa-check.sh
```

Run tests, coverage and SonarScanner in sequence:

```bash
./scripts/qa-check.sh
```

The script persists bounded evidence in:

```text
context/qa-results.md
```

Latest executed closure evidence (`2026-08-02`):

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

The supplied scanner log does not include a server-side Quality Gate result for this run. Tenant isolation, object permissions, production readiness, deployment and database compatibility remain outside the validated scope.

Historical Product baseline (`2026-07-29`):

```text
Product tests                    54 passed
Complete suite                   71 passed
Django system check              0 issues
SonarQube overall coverage       88.4%
Security open issues             0
Reliability open issues          0
Maintainability open issues      0
Accepted design issues           1
Duplicated lines                 2.7%
Quality Gate                     Passed
```

Domain-specific QA baselines remain independent as each canonical app is completed.

## SonarQube configuration

Required environment variables:

```text
SONAR_HOST_URL=http://host.docker.internal:9000
SONAR_TOKEN=<project-analysis-token>
```

The token must never be committed. SonarScanner imports `coverage.xml`; it does
not execute pytest, so coverage must be regenerated before analysis.

## AI integration

Approved AI channels call DP-API through explicit Tools:

```text
Client user
→ Slack / SBM Manager / approved channel
→ SBM AI Assistant
→ DP-API Tool
→ validated domain operation
→ structured result
```

The AI layer must not access PostgreSQL directly, bypass authorization, invent
identifiers, reproduce business calculations outside the responsible API, or
turn rejected operations into successful responses.

## Security

- Keep secrets outside Git.
- Use explicit production CORS origins.
- Replace development credentials before deployment.
- Use a production WSGI/ASGI server.
- Enforce tenant-aware and object-level authorization.
- Restrict admin access.
- Rotate exposed credentials immediately.
- Record auditable user identity for write operations.
- Apply the same authorization rules to AI-triggered actions.
- Review rate limiting, secure errors and structured logging before deployment.

## Project documentation

```text
README.md
→ final-state project overview, setup, configuration and usage

context/PROJECT_CONTEXT.md
→ active and pending objectives, current implementation state, risks and
  instructions for LLM-assisted development

SBM-SUITE/context/COMPLETED_OBJECTIVES.md
→ single global history of completed objectives grouped by project
```

The README describes completed architecture and developer workflow. The project
context is the authoritative source for current operational development state.
Completed-objective history is maintained only in the global suite context.

## License

Private portfolio and development project unless a separate license is added.

---

```text
Signed by CONKER
SBM Suite
```

## Context lifecycle

The lifecycle has two context cycles and one final documentation cycle.

### Before development

Export the current project state and assigned objective with an explicit phase:

```bash
./scripts/context-deploy.sh \
  planning-activation \
  DP-MATERIAL-001 \
  "Implementar la integración Material solicitada"
```

Generated artifacts:

```text
${SBM_SUITE_ROOT}/context/output
${SBM_SUITE_ROOT}/context/output/SYS_PROMPT.md
```

After ChatGPT generates `context-upgrade.zip`, place it at:

```text
${SBM_SUITE_ROOT}/context/input/context-upgrade.zip
```

Apply the reviewed planning update:

```bash
./scripts/context-upgrade.sh
```

This first upgrade synchronizes project and global active or pending objectives,
proposes the branch name, and records planned QA when applicable. It must not
claim the feature is implemented.

### After development

Run QA and SonarQube:

```bash
./scripts/qa-check.sh
```

Export intermediate implementation evidence without inferring the phase from
Git, QA or changed files:

```bash
./scripts/context-deploy.sh \
  implementation-progress \
  DP-MATERIAL-001
```

After implementation and QA, export closing evidence explicitly:

```bash
./scripts/context-deploy.sh \
  implementation-closure \
  DP-MATERIAL-001
```

Apply the reviewed closing update:

```bash
./scripts/context-upgrade.sh
```

The closing upgrade updates actual QA evidence, removes the objective from active
and pending contexts, and appends it only to
`${SBM_SUITE_ROOT}/context/COMPLETED_OBJECTIVES.md`.

### Final documentation

Documentation is updated only after the objective is implemented, validated and
closed:

```bash
./scripts/documentation-deploy.sh
./scripts/documentation-upgrade.sh
```

The workflows validate paths, manifest metadata and hashes, create timestamped
backups under `${SBM_SUITE_ROOT}/context/backup`, apply only allowlisted files
atomically, and remove input ZIPs only after full success. Git branch creation,
commit and push remain manual.

Every context export first requires HTTP 200 from `GET /contexts/contract` and
validates the published version, lifecycle phases, canonical project path and
supported patch paths before cleaning global exchange outputs. Every upgrade
reads `manifest.json` directly from the ZIP without extracting it, checks it
against the same contract and rejects unsafe, unsupported or phase-incompatible
patches before calling the backend. This client preflight supplements and does
not replace backend validation.
