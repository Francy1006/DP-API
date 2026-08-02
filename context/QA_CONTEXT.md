# QA_CONTEXT.md

> **Last updated:** 2026-07-30
>
> **Purpose**
>
> Project-specific QA context for `DP-API`. It defines technical QA details, quality gates, environments, test structure, test inventory, fixtures, coverage, SonarQube, validated evidence, defects, exceptions and pending work.
>
> **Accuracy note**
>
> Only executed and evidenced validation may be recorded as completed. Planned commands, tests, coverage and SonarQube results must remain clearly separated from validated evidence.

## 1. Project technical details

| Attribute | Value |
|---|---|
| Project | DP-API |
| Language | Python |
| Framework | Django 4.2.x / Django REST Framework 3.14 |
| Runtime | Docker Compose / container `dp-core` |
| Test framework | pytest / pytest-django |
| Coverage tool | pytest-cov / coverage.py |
| Static analysis tool | SonarQube Community Build |
| SonarQube project key | `DP-API` |
| QA execution command | `./scripts/qa-check.sh` |

Additional runtime details:

| Attribute | Value |
|---|---|
| Compose service | `api` |
| Internal port | `8000` |
| Host port | `8081` |
| Shared network | `sbm-network` |
| Coverage artifact | `coverage.xml` |
| Database ownership | PostgreSQL and Flyway through SBM-DB |

## 2. Project QA scope

DP-API QA protects:

- public REST contracts;
- client-facing domain behavior;
- Hexagonal Architecture boundaries;
- layered CRUD behavior;
- unmanaged ORM mappings;
- logical deletion;
- audit and confirmation behavior;
- entity versioning;
- Price creation and versioning;
- provider and relationship integrity;
- authentication and authorization;
- tenant and brand isolation;
- compatibility with SBM-MANAGER;
- compatibility with future SBM-AI-ASSISTANT Tools;
- context and documentation synchronization when project behavior changes.

Current project QA priority:

```text
Define and implement the complete evidence-based QA procedure for DP-API.
```

## 3. Required quality gates

| Gate | Requirement | Blocking | Evidence |
|---|---|---:|---|
| Focused tests | Affected domain tests pass | 1 | pytest output |
| Complete suite | Full configured suite passes | 1 | pytest output |
| Django system check | `manage.py check` returns 0 issues | 1 | command output |
| Coverage | Configured minimum threshold is met | 1 | terminal and `coverage.xml` |
| SonarQube | Quality Gate passes | 1 | scanner and server result |
| API contract | Methods, paths, bodies, responses and errors validated | 1 | API tests |
| Database compatibility | ORM matches PostgreSQL, Flyway and DBML | 1 | comparison evidence |
| Security | Authentication, authorization and tenant isolation validated | 1 | security tests |
| Regression | Previously corrected defects remain protected | 1 | regression tests |
| Documentation | Context and README updates are synchronized | 1 | Git diff / context package |

A gate may be bypassed only through an explicit accepted exception.

## 4. Test environments

| Environment | Purpose | Database | Restrictions |
|---|---|---|---|
| Local development | Focused implementation validation | Approved local PostgreSQL or isolated mocks | No final QA unless authorized |
| Container test | Authoritative project test runtime | Dedicated or isolated test database | Must match container dependencies |
| Integration | API/database and cross-project validation | Flyway-initialized PostgreSQL | No shared persistent mutations |
| SonarQube local | Static analysis and Quality Gate | Independent SonarQube PostgreSQL | No business database access |
| Production | Operational runtime only | Production PostgreSQL | No destructive QA |

Docker is the authoritative project runtime.

Host Python execution is not authoritative when dependencies or environment variables differ from the container.

## 5. Test structure

Canonical ownership:

```text
Product  → products/tests/
Material → material/tests/
Service  → service/tests/
Catalog  → catalog/tests/
Ticket   → ticket/tests/
Provider → providers/tests/
Pricing  → pricing/tests/
```

Recommended structure for business-critical domains:

```text
tests/
├── __init__.py
├── conftest.py
├── factories.py
├── test_models.py
├── test_domain.py
├── test_policies.py
├── test_serializers.py
├── test_use_cases.py
├── test_repositories.py
├── test_views.py
├── test_api.py
└── test_regression.py
```

Rules:

- each domain owns its tests;
- do not place one domain's tests inside another app;
- avoid a repository-root `tests/` directory unless explicitly approved;
- test names use:

```text
test_<behavior>_<condition>_<expected_result>
```

## 6. Test inventory

| Test ID | Description | Logic type | Components | Risk | Last execution | Result | Evidence |
|---|---|---|---|---:|---|---|---|
| DP-PROD-001 | Product focused test suite | unit | Product domain, serializers, use cases, views | 4 | 2026-07-29 | PASS | 54 tests passed |
| DP-SUITE-001 | Complete configured pytest suite | integration | DP-API configured test scope | 4 | 2026-07-29 | PASS | 71 tests passed |
| DP-DJANGO-001 | Django system check | static-analysis | Django project configuration | 4 | 2026-07-29 | PASS | 0 issues |
| DP-COV-001 | Product pytest coverage | coverage | Product package | 3 | 2026-07-29 | PASS | 73.64% including branches |
| DP-SONAR-001 | Product SonarQube analysis | static-analysis | Product scope | 4 | 2026-07-29 | PASS | Quality Gate Passed |
| DP-API-PROD-001 | Product list and detail contract | api | `/api/products/` | 4 | 2026-07-29 | PASS | API regression suite |
| DP-API-PROD-002 | Product create contract | api | Product, Price, PostgreSQL trigger | 5 | 2026-07-29 | PASS | HTTP 201 and regression tests |
| DP-API-PROD-003 | Product PATCH and idempotency | api | Product use cases and repository | 5 | 2026-07-29 | PASS | Regression tests |
| DP-API-PROD-004 | Product logical deletion | api | Product delete action | 4 | 2026-07-29 | PASS | Regression tests |
| DP-API-PROD-005 | Disabled Product PUT and DELETE | api | Product ViewSet | 3 | 2026-07-29 | PASS | HTTP 405 tests |
| DP-PRICE-001 | Product Price versioning | integration | Product, Price, transaction behavior | 5 | 2026-07-29 | PASS | Regression tests |
| DP-MAT-001 | Material canonical app ownership | integration | `material`, `products` | 4 | N/A | pending | Final Material baseline pending |
| DP-SERVICE-001 | Service schema and contract preflight | database | SBM-DB, Flyway, DBML, Service app | 5 | N/A | blocked | Current database evidence required |
| DP-SEC-001 | Tenant isolation | security | Authentication, authorization, query scope | 5 | N/A | pending | No complete evidence |
| DP-AUTH-001 | Django user and business user mapping | security | Django auth, `users.User` | 5 | N/A | pending | Architecture unresolved |

Allowed logic types:

```text
unit
integration
api
database
security
static-analysis
coverage
deployment
```

Risk scale:

```text
0 = none
1 = very low
2 = low
3 = medium
4 = high
5 = critical
```

## 7. Test data and fixtures

Preferred:

- deterministic builders;
- reusable fixtures;
- dedicated Flyway-initialized test database;
- isolated test records;
- rolled-back transactions;
- minimal required data;
- explicit business-user and Django-user distinction.

Avoid:

- production-like hardcoded IDs;
- dependence on shared development rows;
- persistent mutation of development data;
- random values where exact behavior matters;
- credentials in fixtures;
- mocking all ORM behavior for integration-sensitive tests.

Current Product test support includes:

```text
products/tests/conftest.py
products/tests/factories.py
```

Factory Boy and Faker are not currently required for the validated Product scope.

## 8. Unit tests

Unit tests validate:

- pure domain policies;
- value calculations;
- lifecycle rules;
- invariant enforcement;
- serializer validation without persistence when practical;
- use-case behavior through ports;
- invalid state transitions;
- idempotent decisions.

Domain tests must not depend on Django or DRF.

Do not unit-test PostgreSQL trigger internals as Python logic.

## 9. Integration tests

Integration tests validate:

- ORM mappings;
- repository adapters;
- transaction behavior;
- row locking where applicable;
- legacy data compatibility;
- Product and Price coordination;
- provider relationships;
- Flyway-initialized schema compatibility;
- rollback behavior;
- consumer-to-provider integration when required.

Repository tests require a database initialized from the current Flyway schema.

## 10. API tests

Each endpoint test must validate:

- HTTP method;
- path;
- authentication;
- authorization;
- request fields;
- response fields;
- status codes;
- pagination;
- filters;
- search;
- ordering;
- read-only fields;
- hidden internal fields;
- error schema;
- logical deletion;
- idempotency;
- disabled methods.

Current Product contract:

```text
GET    /api/products/
POST   /api/products/
GET    /api/products/{id}/
PATCH  /api/products/{id}/
HEAD   /api/products/
HEAD   /api/products/{id}/
POST   /api/products/{id}/delete/
PUT    /api/products/{id}/      → HTTP 405
DELETE /api/products/{id}/      → HTTP 405
```

## 11. Database tests

Mandatory comparison:

```text
live PostgreSQL
↔ Flyway
↔ DBML
↔ Django model
↔ repository adapter
↔ serializer
↔ public REST contract
```

Forbidden without separate authorization:

```bash
python manage.py makemigrations
python manage.py migrate
```

Also forbidden:

- Django business-schema migration files;
- Flyway changes;
- DBML changes;
- trigger changes;
- constraint changes;
- index changes;
- persistent test mutation of shared data.

Service implementation and QA remain blocked until the current database source is verified.

## 12. Security tests

Required scenarios:

- unauthenticated request;
- invalid credentials;
- expired credentials;
- unauthorized role;
- missing permission;
- wrong tenant;
- cross-tenant read;
- cross-tenant write;
- invalid business-user reference;
- object-level restriction;
- client access to internal platform operations;
- audit actor spoofing;
- secret leakage;
- permissive production CORS;
- AI Tool using unrestricted credentials.

Current unresolved risks:

- Django auth and business users coexist;
- token endpoint and global authentication classes may differ;
- tenant isolation is not fully evidenced;
- object-level permission enforcement is not fully evidenced;
- business audit users may still be client-supplied.

## 13. Static analysis

Static-analysis rules:

- run after coverage generation;
- do not hide application code to improve metrics;
- test files may be omitted from application coverage;
- each new domain requires an explicit scope and baseline;
- scanner credentials remain outside Git.

Current SonarQube configuration:

```text
Project key: DP-API
Branch: main
sonar.sources=products
sonar.tests=products/tests
sonar.python.version=3.11
sonar.python.coverage.reportPaths=coverage.xml
```

Current scanner scripts:

```text
scripts/sonar-scan.sh
scripts/qa-check.sh
```

## 14. Coverage

Current validated Product coverage:

| Metric | Result |
|---|---:|
| Pytest coverage including branches | 73.64% |
| Line coverage | 78.44% |
| Branch coverage | 33.19% |
| SonarQube overall coverage | 88.4% |

Coverage artifact:

```text
coverage.xml
```

Rules:

- regenerate coverage before SonarQube;
- do not exclude untested domain, repository, serializer, model, view or use-case code;
- do not compare pytest-cov and SonarQube percentages as identical metrics;
- future module thresholds require explicit approval.

## 15. SonarQube

Latest validated Product scope:

| Metric | Result |
|---|---|
| Quality Gate | Passed |
| Security rating | A |
| Security open issues | 0 |
| Reliability rating | A |
| Reliability open issues | 0 |
| Maintainability rating | A |
| Maintainability open issues | 0 |
| Accepted issues | 1 |
| Security hotspots | 0 |
| Duplicated lines | 2.7% |
| Overall coverage | 88.4% |

Accepted issue:

```text
Catalog.obs null=True
```

Reason:

The unmanaged Django mapping must match the nullable Flyway/PostgreSQL column.

The finding is accepted design alignment, not a False Positive.

## 16. Current validated evidence

Validated on:

```text
2026-07-29
```

Evidence summary:

```text
Product tests                    54 passed
Complete suite                   71 passed
Django system check              0 issues
Coverage including branches      73.64%
Line coverage                    78.44%
Branch coverage                  33.19%
SonarQube overall coverage       88.4%
Security rating                  A
Reliability rating               A
Maintainability rating           A
Open Security issues             0
Open Reliability issues          0
Open Maintainability issues      0
Security hotspots                0
Duplicated lines                 2.7%
Quality Gate                     Passed
```

Validated commands:

```bash
./scripts/coverage.sh
./scripts/sonar-scan.sh
./scripts/qa-check.sh
```

Direct container commands recorded:

```bash
docker compose --env-file .env.dev run --rm --no-deps --entrypoint python api manage.py check
docker compose --env-file .env.dev run --rm --no-deps --entrypoint pytest api
docker compose --env-file .env.dev run --rm --no-deps --entrypoint pytest api products/tests/
```

This evidence applies to the configured Product-focused scope and current complete suite. It does not prove tenant isolation, production readiness or all future modules.

## 17. Known defects

| Defect ID | Description | Severity | Status | Evidence | Owner |
|---|---|---:|---|---|---|
| DP-AUTH-001 | Django auth and business-user identity mapping unresolved | 5 | open | Current architecture | DP-API |
| DP-AUTH-002 | Token endpoint and accepted authentication classes may be inconsistent | 4 | open | Current settings context | DP-API |
| DP-SEC-001 | Tenant isolation not fully evidenced | 5 | open | Missing security tests | DP-API |
| DP-SEC-002 | Object-level permissions not fully evidenced | 5 | open | Missing security tests | DP-API |
| DP-DATA-001 | Legacy Material Price identifiers may not resolve | 4 | mitigated | Compatibility behavior implemented | DP-API / SBM-DB |
| DP-DATA-002 | Shared historical Product Price rows require compatibility handling | 4 | mitigated | Regression behavior implemented | DP-API / SBM-DB |
| DP-RUNTIME-001 | Development server and fixed startup wait remain in use | 3 | open | Compose configuration | DP-API |
| DP-CORS-001 | Permissive CORS is active in development configuration | 4 | open | Settings context | DP-API |

## 18. Accepted exceptions

| Exception ID | Scope | Description | Risk | Reason | Owner | Expiration | Status |
|---|---|---|---:|---|---|---|---|
| DP-SONAR-001 | Product | `Catalog.obs null=True` remains in unmanaged ORM mapping | 2 | Required to match Flyway/PostgreSQL nullability | DP-API / SBM-DB | N/A | accepted |
| DP-API-LEGACY-001 | Product | Duplicate Product endpoint remains temporarily in SBM-API | 3 | Consumer audit and retirement are separate work | DP-API / SBM-API | N/A | accepted temporarily |
| DP-TRIGGER-001 | Product SKU | Existing trigger sequence strategy remains unchanged | 3 | Database-owned hardening task | SBM-DB | N/A | accepted temporarily |

No other exception may be inferred from missing evidence.

## 19. Pending QA work

1. Finalize the complete DP-API QA procedure.
2. Define mandatory thresholds for every domain.
3. Extend SonarQube and coverage to Material.
4. Create the Service QA baseline after implementation.
5. Add dedicated Flyway-initialized integration database.
6. Add repository integration tests.
7. Add tenant-isolation tests.
8. Add object-level permission tests.
9. Resolve token authentication behavior.
10. Resolve Django user and business-user mapping.
11. Add CI/CD Quality Gate enforcement.
12. Add SBM-MANAGER Material integration validation.
13. Add future AI Tool authorization tests.
14. Add deployment and rollback validation.
15. Standardize generated QA evidence for `context-deploy.sh`.
16. Synchronize this project QA context with the global QA context automatically.

## 20. Related documentation

Relevant documentation domains:

- DP-API;
- QA and Testing;
- Development;
- Security and DevSecOps;
- Data Architecture;
- DevOps;
- Roadmap;
- AI Engineering.

Documentation paths must use:

```text
SBM-SUITE/context/documentation/pages/<page>/<page>.md
SBM-SUITE/context/documentation/pages/<page>/subpages/<subpage>.md
```

Specific paths will be added when the documentation structure is finalized.

## 21. Document boundary

This file defines DP-API QA policy, environments, test organization, current evidence, defects, exceptions and pending work.

It does not replace:

- raw pytest output;
- `coverage.xml`;
- SonarQube reports;
- PostgreSQL inspection;
- Flyway migrations;
- DBML;
- project deployment procedures;
- global transversal QA;
- security architecture;
- implementation history;
- documentation page content.
