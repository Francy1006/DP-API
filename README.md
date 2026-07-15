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

    ████████████████████████████████████████████████████████████████
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
    ████████████████████████████████████████████████████████████████
```

# DP-API

Client-facing REST API for the Ditaly Pasta business domain within **SBM Suite**.

`dp-api` allows client users to configure and operate the ERP without requiring an internal SBM administrator for routine business operations.

## Role within SBM Suite

```text
Client user
→ SBM Manager / client application / AI assistant
→ DP-API
→ Ditaly Pasta business operations
```

`dp-api` owns client-facing business capabilities such as products, prices, providers, branches, catalogs and tickets.

Global platform administration remains in `sbm-api`.

```text
Client operation     → dp-api
Platform operation   → sbm-api
```

A client user may create products or modify prices, but cannot create a new franchise, activate uncontracted modules or provision a new tenant.

## Current status

- Active repository.
- Local development environment validated.
- Django REST API running with Docker.
- PostgreSQL connection using `ditaly_pasta`, `sbm_business` and `public` schemas.
- Django Jazzmin administration interface available.
- Domain migration from `sbm-api` pending.
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

## Development roadmap

1. Consolidate `Product` in `dp-api`.
2. Migrate client-facing business logic currently located in `sbm-api`.
3. Consolidate pricing and commercial configuration.
4. Consolidate providers, branches, clients, tickets and orders.
5. Update `sbm-manager` to consume only `dp-api` for client operations.
6. Add automated tests and API contract validation.
7. Harden authentication, authorization and tenant isolation.
8. Integrate `sbm-ai-assistant` through explicit REST tools.
9. Add auditability and human approval for sensitive AI actions.
10. Deploy development, staging and production environments.

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
