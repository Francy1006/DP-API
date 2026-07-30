# QA_CONTEXT.md

> **Last updated:** 2026-07-29
>
> **Project:** DP-API
>
> **Purpose**
>
> This document defines the QA rules, execution boundaries, test organization,
> coverage expectations, SonarQube workflow, and acceptance criteria specific to
> `DP-API`.
>
> It must be read together with:
>
> ```text
> ../../PROJECT_CONTEXT.md
> ../../context/SUITE_CONTEXT.md
> ../../context/BUSINESS_CONTEXT.md
> ../../context/QA_CONTEXT.md
> ./PROJECT_CONTEXT.md
> ./DEPLOY_CONTEXT.md
> ```
>
> The suite-level QA context governs transversal behavior. This file governs
> repository-local QA.

---

## 1. QA responsibility

DP-API QA validates the client-facing API boundary for Ditaly Pasta.

It must protect:

- public REST contracts;
- domain behavior;
- Hexagonal Architecture boundaries;
- unmanaged ORM mappings;
- audit and confirmation behavior;
- logical deletion;
- entity versioning;
- Price creation and versioning;
- provider and relationship integrity;
- authentication and authorization behavior;
- compatibility with SBM Manager and future AI Tools.

---

## 2. Runtime

Docker is the official QA runtime.

Primary Compose service:

```text
api
```

Primary container:

```text
dp-core
```

Validated local API port:

```text
8081
```

Do not treat host Python execution as authoritative when the container runtime
uses different dependencies or environment variables.

---

## 3. Context reading rule

Before QA work, read:

```text
SBM-SUITE/PROJECT_CONTEXT.md
SBM-SUITE/context/SUITE_CONTEXT.md
SBM-SUITE/context/BUSINESS_CONTEXT.md
SBM-SUITE/context/QA_CONTEXT.md
DP-API/context/PROJECT_CONTEXT.md
DP-API/context/QA_CONTEXT.md
DP-API/context/DEPLOY_CONTEXT.md
```

For database-sensitive tests, also inspect the current:

```text
SBM-DB repository
Flyway scripts
DBML
PostgreSQL schema
triggers
functions
constraints
indexes
reference data
```

If the database source is missing, contradictory, or stale, stop and request it.

---

## 4. QA stage separation

### 4.1 Development stage

During implementation, run only focused validation:

```text
focused domain tests
focused serializer tests
focused use-case tests
focused ViewSet/API tests
python manage.py check
targeted import checks
targeted endpoint smoke tests
```

Do not execute:

```bash
./scripts/qa-check.sh
```

during development unless the user explicitly authorizes it.

Do not run the final SonarQube workflow during active implementation unless
explicitly requested.

### 4.2 Final project QA

The user executes the final project QA manually after implementation review.

Final QA may include:

```bash
./scripts/coverage.sh
./scripts/sonar-scan.sh
./scripts/qa-check.sh
```

### 4.3 Transversal QA

After local acceptance, use the global QA context for flows involving:

```text
SBM-MANAGER
SBM-API
SBM-DB
SBM-AI-ASSISTANT
```

---

## 5. Test organization

Each canonical domain owns its tests.

```text
products/tests/
material/tests/
service/tests/
catalog/tests/
ticket/tests/
providers/tests/
pricing/tests/
```

Do not place tests for one domain inside another app merely because the entities
share lookups or Price infrastructure.

Canonical ownership:

```text
Product  → products
Material → material
Service  → service
Catalog  → catalog
Ticket   → ticket
```

Avoid a repository-root `tests/` hierarchy unless a future transversal test
strategy explicitly requires it.

---

## 6. Recommended test layers

Each business-critical vertical should include:

```text
tests/
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

The exact files may vary by domain complexity.

### Models

Validate:

- field mappings;
- unmanaged status;
- relationships;
- canonical names;
- nullability assumptions;
- database-owned generated fields.

Do not unit-test PostgreSQL trigger internals as Python logic.

### Domain and policies

Validate:

- pure business rules;
- lifecycle transitions;
- Price calculations;
- invariants;
- idempotency;
- invalid state transitions.

Domain tests must not depend on Django or DRF.

### Use cases

Validate:

- orchestration;
- repository-port interactions;
- transaction intent;
- audit behavior;
- error mapping;
- idempotency;
- rollback-sensitive decisions.

### Repositories

Validate:

- ORM mapping;
- filtering;
- logical visibility;
- row locking when applicable;
- persistence of domain changes;
- compatibility with legacy records.

Repository integration tests require a database initialized with the current
Flyway schema.

### Serializers

Validate:

- writable fields;
- read-only fields;
- canonical response fields;
- relationship validation;
- hidden audit fields;
- invalid payloads;
- incompatible Price Configuration.

### Views and API

Validate:

- routes;
- HTTP methods;
- status codes;
- pagination;
- filters;
- search;
- logical delete actions;
- disabled PUT or physical DELETE where applicable;
- authentication;
- authorization;
- public error contracts.

### Regression

Protect every previously corrected defect.

---

## 7. Naming convention

Use:

```text
test_<behavior>_<condition>_<expected_result>
```

Examples:

```text
test_create_product_with_valid_data_returns_201
test_patch_material_with_same_values_does_not_increment_version
test_create_service_without_current_database_mapping_is_blocked
test_delete_product_logically_hides_record_from_list
test_put_product_returns_405
```

Names must describe observable behavior.

---

## 8. Database QA restrictions

PostgreSQL and Flyway own the physical business schema.

Forbidden:

```bash
python manage.py makemigrations
python manage.py migrate
```

Also forbidden without separate authorization:

- Django migration files;
- PostgreSQL schema changes;
- Flyway changes;
- DBML changes;
- trigger changes;
- constraint changes;
- index changes;
- seed-data changes.

Allowed:

- read-only schema inspection;
- isolated test database;
- rolled-back transactions;
- focused smoke tests against approved development data.

Do not use shared development rows as deterministic fixtures.

---

## 9. Database-sensitive domain preflight

Before testing a new or extracted domain, compare:

```text
live PostgreSQL
↔ Flyway
↔ DBML
↔ Django model
↔ repository adapter
↔ serializer
↔ public REST contract
```

For Service, this preflight is mandatory before implementation or QA planning.

Do not infer Service behavior from Product or Material.

---

## 10. Hexagonal Architecture QA

For business-critical domains, validate this dependency direction:

```text
presentation adapter
→ application use case
→ domain
→ repository port
→ infrastructure adapter
```

Prohibited dependencies:

```text
domain → Django
domain → DRF
domain → ORM
application → concrete ORM repository
```

Validate that:

- controllers do not own complex workflows;
- serializers do not own business orchestration;
- use cases depend on ports;
- repository adapters implement domain ports;
- domain rules remain framework-independent;
- no artificial Product/Material/Service shared abstraction exists.

---

## 11. Product QA baseline

Product is the accepted reference vertical.

Latest validated baseline:

```text
Product tests                    54 passed
Complete suite                   71 passed
Django system check              0 issues
SonarQube overall coverage       88.4%
Security open issues             0
Reliability open issues          0
Maintainability open issues      0
Accepted issues                  1
Duplicated lines                 2.7%
Quality Gate                     Passed
```

Accepted Product finding:

```text
Catalog.obs null=True
```

Reason:

The unmanaged Django mapping must match the nullable Flyway/PostgreSQL column.
Removing `null=True` would desynchronize the ORM and could change the REST
contract.

This is an accepted design issue, not a False Positive.

---

## 12. Product behaviors to preserve

### Read

- list and detail return the accepted contract;
- canonical `item_group` naming;
- response labels remain available;
- internal log remains hidden;
- logically deleted records remain excluded.

### Create

- HTTP 201;
- SKU generated by PostgreSQL;
- Provider validation;
- current Price created and linked;
- compatible confirmed Price Configuration;
- version starts correctly;
- audit and confirmation metadata controlled by backend.

### Update

- PATCH supported;
- PUT disabled when defined by contract;
- physical DELETE disabled;
- Provider immutable after creation;
- effective changes increment version once;
- idempotent updates do not increment;
- Price changes create a new Price version;
- shared legacy Prices remain protected;
- transaction failure rolls back safely.

### Logical deletion

Method:

```text
POST
```

Path:

```text
/api/products/{id}/delete/
```

Expected:

- physical record remains;
- inactive/deleted state is persisted;
- audit fields are populated;
- record disappears from normal queries.

---

## 13. Material QA direction

Material is owned exclusively by the `material` app.

Validate:

- no Material implementation remains in `products`;
- canonical `/api/materials/` contract;
- Material-specific domain and repository ports;
- Price behavior independent from Product;
- legacy dangling Price UUID compatibility;
- lifecycle, confirmation, audit and logical deletion;
- Material test ownership under `material/tests/`.

A dedicated Material final QA baseline will be created separately after its
complete acceptance.

---

## 14. Service QA direction

Service belongs exclusively to the future `service` app.

Before Service QA:

1. request the current SBM-DB source;
2. inspect Flyway;
3. inspect DBML;
4. inspect live PostgreSQL read-only;
5. inspect existing DP-API and SBM-API Service code;
6. confirm the public contract.

Do not create a final Service QA baseline before implementation is complete.

During development:

- focused Service tests only;
- `python manage.py check`;
- targeted import and endpoint smoke tests;
- no `qa-check.sh`;
- no final SonarQube run unless authorized.

---

## 15. Pricing QA

Validate:

- compatible record type;
- confirmed Price Configuration;
- Decimal-based calculation;
- exact monetary rounding;
- Price creation;
- Price versioning;
- current/non-current transitions;
- ownership of previous Price;
- shared legacy Price protection;
- idempotent updates;
- transaction rollback;
- audit linkage;
- frontend and AI cannot submit derived values as authoritative.

---

## 16. Provider QA

Validate:

- selector contract;
- list and detail;
- search and filters;
- creation and partial update;
- geographic relationships;
- banking relationships;
- confirmation and audit;
- provider compatibility with Product, Material and Service;
- no cross-domain ownership leakage.

---

## 17. Authentication and authorization QA

Current risks include:

- Django auth and business users coexist;
- token endpoint and global authentication classes may differ;
- business audit users may still be client-supplied;
- tenant isolation is not fully resolved.

Validate where applicable:

```text
unauthenticated
authenticated
unauthorized
wrong tenant
wrong role
missing permission
invalid business-user reference
```

Do not use superuser access as proof of a valid client workflow.

---

## 18. API contract QA

For each endpoint validate:

- HTTP method;
- path;
- authentication;
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
- logical deletion behavior;
- idempotency where applicable.

Endpoint documentation format:

```text
Method: POST

/api/resource/
```

---

## 19. Test-data rules

Preferred:

- deterministic builders;
- reusable fixtures;
- isolated test records;
- dedicated Flyway-initialized test database;
- transaction rollback.

Avoid:

- hardcoded production-like IDs;
- dependence on existing shared rows;
- random values where exact behavior matters;
- persistent mutation of development data;
- credentials in fixtures;
- mocking all ORM behavior in integration-sensitive tests.

Use mocks only where they improve isolation.

---

## 20. Coverage

Coverage must measure application code honestly.

Do not exclude:

- untested domain modules;
- repository adapters;
- serializers;
- views;
- models;
- use cases;

merely to improve the percentage.

Test files may be omitted from application coverage.

Coverage outputs:

```text
terminal report
coverage.xml
```

SonarQube imports `coverage.xml`; it does not execute pytest.

Always regenerate coverage before a new SonarQube analysis.

---

## 21. QA scripts

Repository scripts:

```text
scripts/coverage.sh
scripts/sonar-scan.sh
scripts/qa-check.sh
```

Permissions:

```bash
chmod +x scripts/coverage.sh
chmod +x scripts/sonar-scan.sh
chmod +x scripts/qa-check.sh
```

Generate tests and coverage:

```bash
./scripts/coverage.sh
```

Run scanner:

```bash
./scripts/sonar-scan.sh
```

Run complete flow:

```bash
./scripts/qa-check.sh
```

The complete flow is reserved for final QA, not normal development.

---

## 22. Direct Docker commands

Django system check:

```bash
docker compose --env-file .env.dev run --rm --no-deps   --entrypoint python api manage.py check
```

Complete pytest suite:

```bash
docker compose --env-file .env.dev run --rm --no-deps   --entrypoint pytest api
```

Product tests:

```bash
docker compose --env-file .env.dev run --rm --no-deps   --entrypoint pytest api products/tests/
```

Material tests:

```bash
docker compose --env-file .env.dev run --rm --no-deps   --entrypoint pytest api material/tests/
```

Service tests after app creation:

```bash
docker compose --env-file .env.dev run --rm --no-deps   --entrypoint pytest api service/tests/
```

Commands must be revalidated against the current Compose configuration before
execution.

---

## 23. SonarQube

Current Product project configuration uses:

```text
Project key: DP-API
Branch: main
```

Environment:

```text
SONAR_HOST_URL
SONAR_TOKEN
```

Never commit the token.

Current Product scope:

```text
sonar.sources=products
sonar.tests=products/tests
sonar.python.coverage.reportPaths=coverage.xml
```

Each new domain must receive a separately authorized scope and baseline.

Do not combine multiple domains into one scope without an explicit decision.

---

## 24. Quality Gate

A passing Quality Gate is required for final acceptance when SonarQube applies.

A pass does not prove:

- production readiness;
- correct tenant isolation;
- correct frontend integration;
- correct database mapping;
- complete business acceptance.

These require separate validation.

---

## 25. Required evidence

Every QA report must include:

```text
scope
domain
files tested
commands executed
focused-test result
complete-suite result
Django check result
coverage result
SonarQube result
database mutation statement
migration statement
known risks
final status
```

Never claim a command was executed when it was only planned.

---

## 26. Acceptance statuses

Use:

```text
PASS
PASS WITH ACCEPTED RISK
BLOCKED
FAIL
```

Accepted risks must document:

- issue;
- impact;
- reason;
- owner;
- next action.

---

## 27. Context update rules

After local QA:

Update:

```text
DP-API/context/QA_CONTEXT.md
```

when:

- commands change;
- tests change;
- coverage changes;
- SonarQube changes;
- a finding is accepted;
- a domain baseline is completed.

Update:

```text
DP-API/context/PROJECT_CONTEXT.md
```

when:

- implementation status changes;
- ownership changes;
- architecture changes;
- active objective changes.

Update:

```text
DP-API/context/DEPLOY_CONTEXT.md
```

when:

- environment variables change;
- Docker configuration changes;
- ports change;
- startup changes;
- deployment or rollback changes.

Update global contexts when the change affects more than DP-API.

---

## 28. Stable DP-API QA rules

1. Docker is the official runtime.
2. Flyway owns business schema changes.
3. No Django migrations for Flyway-owned tables.
4. Each domain owns its tests.
5. Product remains the reference vertical.
6. Material remains independent from Product.
7. Service requires current database validation first.
8. Do not execute `qa-check.sh` during development.
9. Final QA is executed manually by the user.
10. Do not create a final domain QA context before implementation is complete.
11. Preserve public REST contracts unless separately authorized.
12. Do not hide application code from coverage.
13. Do not use superuser access as client-authorization proof.
14. Do not mutate shared persistent data.
15. Report missing sources instead of guessing.
16. Work one validated step at a time.
