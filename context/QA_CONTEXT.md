# QA_CONTEXT.md

> **Last updated:** 2026-07-30
>
> **Purpose**
>
> Project-specific QA context for `DP-API`. It defines technical QA details, quality gates, environments, test structure, test inventory, fixtures, coverage, SonarQube, validated evidence, defects, exceptions and pending work.
>
> **Accuracy note**
>
> Only executed and evidenced validation may be recorded as completed. Objective-specific QA may be planned before development, but planned commands, tests, coverage and SonarQube checks must remain pending, without execution date or result, until the closing context upgrade.

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
Maintain the implemented QA procedure and extend validated coverage to unresolved modules, security and integration scopes.
```

Lifecycle rule:

```text
objective activation
→ define planned QA for the feature
→ develop using synchronized contexts
→ execute qa-check.sh and SonarScanner
→ closing context upgrade reconciles actual evidence and closes the objective
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

During objective activation, applicable gates may be registered as planned requirements. They must not be marked as passed, failed or executed before evidence exists.

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
| DP-SUITE-002 | DP-QA-001 configured pytest execution | integration | Configured DP-API pytest scope | 4 | 2026-08-02 | PASS | 65 tests passed; 0 failed; exit code 0 |
| DP-COV-002 | DP-QA-001 configured pytest coverage | coverage | Configured DP-API pytest scope | 3 | 2026-08-02 | PASS | TOTAL 88%; `coverage.xml` generated |
| DP-SONAR-002 | DP-QA-001 SonarScanner execution | static-analysis | 40 indexed Python files | 4 | 2026-08-02 | PASS | Exit code 0; `ANALYSIS SUCCESSFUL`; `EXECUTION SUCCESS` |
| DP-QA-WORKFLOW-001 | Complete QA evidence workflow | integration | `qa-check.sh`, coverage and SonarScanner | 4 | 2026-08-02 | PASS | `qa-results.md` records successful test and scanner execution |

Planning and closure rules:

- The first context upgrade for a feature may add proposed tests tied to the active or pending objective.
- Planned tests use `Last execution = N/A`, `Result = pending` and explicit planning evidence.
- Planned tests must not include invented counts, coverage percentages or SonarQube results.
- The closing context upgrade must reaffirm, modify or remove planned tests using actual `qa-results.md` evidence.
- A completed objective must not retain unresolved mandatory QA entries unless an accepted exception is recorded.
- Project QA changes must synchronize with `SBM-SUITE/context/QA_CONTEXT.md`.

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

Planning rule:

- A feature objective may require coverage execution and a target scope before development.
- Coverage percentages and pass/fail status are recorded only after `qa-check.sh` execution.

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

### DP-QA-001 closure evidence

| Metric | Result |
|---|---:|
| Collected tests | 65 |
| Passed | 65 |
| Failed | 0 |
| Total configured pytest coverage | 88% |
| Coverage artifact | `coverage.xml` |
| Command exit code | 0 |

This result applies to the configured pytest scope shown in `qa-results.md`. No separate approved coverage threshold is present in the supplied evidence.

## 15. SonarQube

Planning rule:

- A feature objective may require SonarQube validation before development begins.
- Quality Gate, issue counts and ratings are recorded only from actual scanner and server evidence.

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

### DP-QA-001 closure evidence

| Metric | Result |
|---|---|
| Project key | DP-API |
| Indexed Python files | 40 |
| Scanner exit code | 0 |
| Analysis upload | successful |
| Scanner execution | successful |
| Server-side Quality Gate result | Not supplied in this run |

The scanner log reports `ANALYSIS SUCCESSFUL` and `EXECUTION SUCCESS`. It does not authorize carrying the historical Quality Gate status forward as the result of this execution.

## 16. Current validated evidence

### DP-QA-001 closure evidence

Validated on:

```text
2026-08-02
```

Evidence summary:

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

Validated command:

```bash
./scripts/qa-check.sh
```

Evidence boundaries:

- the run validates the configured pytest and SonarScanner scope;
- the log does not include a server-side Quality Gate result;
- tenant isolation, object permissions, production readiness, deployment and database compatibility remain unvalidated;
- no migration or deployment execution is evidenced.

### Historical Product baseline

Validated on:

```text
2026-07-29
```

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

The historical baseline is preserved as prior evidence and is not presented as the server result of the 2026-08-02 scanner execution.

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

1. Define mandatory thresholds for every canonical domain.
2. Extend SonarQube and coverage to Material.
3. Create the Service QA baseline after implementation.
4. Add a dedicated Flyway-initialized integration database.
5. Add repository integration tests.
6. Add tenant-isolation tests.
7. Add object-level permission tests.
8. Resolve token authentication behavior.
9. Resolve Django user and business-user mapping.
10. Add CI/CD Quality Gate enforcement.
11. Add SBM-MANAGER Material integration validation.
12. Add future AI Tool authorization tests.
13. Add deployment and rollback validation.

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

This file defines DP-API QA policy, environments, planned and executed test organization, current evidence, defects, exceptions and pending work.

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
