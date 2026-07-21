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

`dp-api` allows client users to configure and operate the ERP without requiring an internal SBM administrator for routine business operations.

## Role within SBM Suite

```text
Client user
→ SBM Manager / client application
→ DP-API
→ Ditaly Pasta business operations
```

`dp-api` is the decoupled API boundary for Ditaly Pasta client operations. `sbm-manager` and other client applications consume `dp-api` for products, prices, providers, branches, catalogs, tickets and other brand-owned capabilities.

`sbm-api` is a separate internal API reserved for critical platform processes and global administration. Client applications do not use it for normal Ditaly Pasta operations.

```text
Client operation     → dp-api
Platform operation   → sbm-api
```

A client user may create products or modify prices, but cannot create a new franchise, activate uncontracted modules or provision a new tenant.

The two APIs are independently deployable and have distinct responsibilities. Physical database schema location does not merge their API ownership boundaries.

## Current status

- Active repository.
- Local development environment validated.
- Django REST API running with Docker.
- PostgreSQL connection using `ditaly_pasta`, `sbm_business` and `public` schemas.
- Django Jazzmin administration interface available.
- Client-facing domain boundary decoupled from the internal `sbm-api`.
- Designed as the Ditaly Pasta API consumed by `sbm-manager`.
- AI integration planned through `sbm-ai-assistant`.
- Production deployment planned.

## Technology stack

- Python
- Django 4.2
- Django REST Framework
- PostgreSQL
- Django Filter
- Django CORS Headers
- Django Jazzmin
- Docker Compose
- Pytest
- Flyway-managed business schemas

## Main modules

| Module | Responsibility |
|---|---|
| `products` | Products, materials, services, catalogs and item configuration |
| `pricing` | Prices and fiscal price configuration |
| `providers` | Providers, banks, regions, districts and provider classifications |
| `branches` | Branches, platforms and agreements |
| `ticket` | Client-facing ticket operations |
| `users` | Client-scoped users and user tokens |
| `authz` | Roles, permissions and restrictions |
| `business` | Shared business classifications |
| `documentation` | Operational documentation models |
| `sales` | Sales-related domain capabilities under development |

## Architecture

The platform currently uses a **hybrid architecture**, selected per business
domain:

- **Layered Architecture** is retained for CRUD-oriented and simple domains,
  using the established ViewSet, serializer, model, and PostgreSQL flow.
- **Hexagonal Architecture** is introduced incrementally for business-critical
  domains with complex rules, workflows, audit requirements, or external
  integrations. Controllers delegate to application use cases, use cases
  depend on domain ports, and Django ORM acts as a persistence adapter.

PostgreSQL remains the source of truth, Flyway owns schema evolution, and
Django business models remain unmanaged where configured. Architecture changes
do not alter the public REST contract or the ownership boundary between
`dp-api` and `sbm-api`.

```text
Frontend / AI channel
        ↓
      DP-API
        ↓
Django REST Framework
        ↓
PostgreSQL
├── ditaly_pasta
├── sbm_business
└── public
```

The physical database schema does not define API ownership by itself. Ownership is determined by the domain rule and by who is authorized to execute the operation.

## Hexagonal Modules

- Product
- Provider
- Material
- Service
- Catalog
- Pricing
- Orders
- Inventory
- Ticket
- Franchise Provisioning
- AI Integration
- Workflow Automation

Product is the first vertical migration and the reference implementation for
the platform's hexagonal modules.

## API boundaries

### DP-API responsibilities

- Products
- Materials
- Services
- Prices
- Providers
- Branches
- Catalogs
- Tickets
- Client users and permissions
- Operational configuration
- Future AI-assisted client operations

### SBM-API responsibilities

- Franchise and tenant creation
- Contracted module activation
- Platform-level administration
- Global configuration
- Subscription and service management
- Schema provisioning
- Internal SBM operations

## Local development

### Requirements

- Docker
- Docker Compose
- PostgreSQL available through the configured Docker network
- Existing external Docker network:

```bash
 docker network create sbm-network
```

Run the command only when the network does not already exist.

### Environment

Create or configure the environment file used by Docker Compose.

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
```

Do not commit real credentials.

### Start the API

When the environment file is named `.env` and is located beside `docker-compose.yml`:

```bash
docker compose up -d --build
```

When using another environment file:

```bash
docker compose --env-file .env.dev up -d --build
```

### Validate containers

```bash
docker ps
```

### View logs

```bash
docker compose logs -f api
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

`dp-api` and `sbm-api` can run in parallel because they use separate containers and different host ports:

```text
dp-api   → localhost:8081 → container 8000
sbm-api  → localhost:8082 → container 8000
```

## Authentication

Current global DRF configuration:

- Session Authentication
- Basic Authentication
- Authenticated access required by default
- DRF token endpoint exposed

Token authentication is not yet configured globally as a default authentication class and must be reviewed before production integration.

## Database management

Business app migrations are disabled in Django because the business schemas are intended to be managed externally with Flyway.

Configured search path:

```text
ditaly_pasta,sbm_business,public
```

Do not generate or apply Django migrations for the business apps without first validating the database ownership strategy.

## QA and code quality

Docker is the official QA runtime. The Product QA flow combines automated tests,
coverage generation and SonarQube static analysis without running Django
migrations or modifying the PostgreSQL schema.

### QA scripts

The repository provides three executable scripts under `scripts/`:

```text
scripts/coverage.sh
scripts/sonar-scan.sh
scripts/qa-check.sh
```

Grant execution permission when cloning the repository or creating the scripts:

```bash
chmod +x scripts/coverage.sh
chmod +x scripts/sonar-scan.sh
chmod +x scripts/qa-check.sh
```

### Generate tests and coverage

```bash
./scripts/coverage.sh
```

This script:

1. loads the configured Compose environment file;
2. executes the Product pytest suite inside the `api` service;
3. measures line and branch coverage with `pytest-cov`;
4. generates `coverage.xml` inside `dp-core`;
5. copies `coverage.xml` to the repository root.

Coverage measures which application lines and decision branches were executed by
the tests. SonarQube reads `coverage.xml`; it does not execute pytest itself.
Always regenerate coverage before a new SonarQube analysis to avoid reporting
stale results.

### Run SonarQube analysis

The local SonarQube server must be running and the environment file must contain:

```text
SONAR_HOST_URL=http://host.docker.internal:9000
SONAR_TOKEN=<project-analysis-token>
```

Do not commit the token or any environment file containing secrets.

Run the scanner:

```bash
./scripts/sonar-scan.sh
```

The scanner reads `sonar-project.properties`, analyzes the configured Product
sources, imports `coverage.xml`, and sends the report to the local SonarQube
server. It reports reliability, maintainability, security findings, coverage,
duplications and the Quality Gate result.

### Run the complete QA flow

```bash
./scripts/qa-check.sh
```

Execution order:

```text
pytest + coverage.xml
→ SonarScanner
→ SonarQube Quality Gate
```

The script stops immediately if tests or coverage generation fail, so SonarQube
never receives a report built from a failing test run.

### Direct commands

Build the current dependencies:

```bash
docker compose --env-file .env.dev build api
```

Run the complete suite or only Product:

```bash
docker compose --env-file .env.dev run --rm --no-deps --entrypoint pytest api
docker compose --env-file .env.dev run --rm --no-deps --entrypoint pytest api products/tests/
```

Latest validated baseline:

```text
Product tests                    54 passed
Complete suite                   71 passed
Django system check              0 issues
Coverage including branches      73.64%
Line coverage                    78.44%
Branch coverage                  33.19%
SonarQube Product coverage       67.9%
SonarQube reliability rating     B (2 issues)
SonarQube maintainability rating A (21 issues)
SonarQube security rating        A (0 issues)
SonarQube duplications           12.2%
Quality Gate                     Passed
```

The pytest and SonarQube percentages use different calculations. Pytest reports
coverage for the Python package and separates line and branch coverage;
SonarQube combines executable lines and conditions according to its own metric.

## AI integration

Planned flow:

```text
Client user
→ Slack / SBM Manager / future channel
→ SBM AI Assistant
→ DP-API Tool
→ validated domain operation
→ structured response
```

The AI layer must never bypass `dp-api`, access business tables directly or reproduce domain validation rules.

## Project documentation

`PROJECT_CONTEXT.md` contains persistent technical and historical context for continuing development with an LLM.

It is intentionally separate from this README:

- `README.md`: public project overview and developer entry point.
- `PROJECT_CONTEXT.md`: detailed persistent project memory.

## Security notes

- Never commit `.env` files containing real secrets.
- Rotate any credential that has been shared outside its intended environment.
- Disable permissive CORS before production.
- Replace Django `runserver` with a production WSGI/ASGI server before deployment.
- Add explicit authorization for client, tenant and module scope.
- Audit AI-triggered write operations.

## License

Private portfolio and development project unless a separate license is added.

---

```text
Signed by CONKER
SBM Suite
```
