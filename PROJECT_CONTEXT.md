# PROJECT_CONTEXT.md

> **Last updated:** 2026-07-17
>
> **Purpose of this file**
>
> This document is persistent project memory for an LLM. It is **not** a README, onboarding guide, product brochure, installation tutorial, or complete API reference. It preserves the product, technical, architectural, historical, and migration context required to continue developing `dp-api` in a new conversation without access to the original chat.
>
> **Accuracy note**
>
> The state described here is based on direct inspection of the `DP-API` repository supplied on 2026-07-14, comparison with the supplied `SBM-API` repository, the complete `SBM-business.dbml` database model, the application running locally, and decisions explicitly validated during the conversation. The repository ZIP contained local environment files, Git metadata, and a SQLite file; secrets and credential values are intentionally omitted from this document. Some behaviors were inferred from models, serializers, views, routes, settings, Docker configuration, and existing technical documentation. Anything planned but not implemented is marked accordingly.

---

## 1. Project objective

### 1.1 What `dp-api` is

`dp-api` is the client-facing Django REST API for the Ditaly Pasta business domain inside SBM Suite.

Its purpose is to allow a **client user** of Ditaly Pasta to operate and configure the ERP without depending on an internal SBM administrator for normal business activity.

A client user may perform permitted operations such as:

- Create and maintain products.
- Create and maintain materials.
- Create and maintain services.
- Configure catalogs and menus.
- Modify prices and commercial configurations.
- Manage providers.
- Manage branches.
- Create and manage tickets.
- Manage operational users, roles, and permissions within the client scope.
- Use future AI-assisted workflows backed by this API.

### 1.2 Role inside SBM Suite

The platform boundary is:

```text
Client user
→ sbm-manager or future client application
→ dp-api
→ Ditaly Pasta business data and operations
```

For AI-assisted operations:

```text
Client user
→ Slack / sbm-manager / future channel
→ sbm-ai-assistant
→ dp-api tools
→ validated business operation or structured result
```

`dp-api` is not the global platform administration API. That responsibility belongs to `sbm-api`.

### 1.3 Core product principle

The client should be able to manage the normal operation of Ditaly Pasta independently.

The client must not require an internal SBM user for routine ERP configuration or execution.

Examples of valid client capabilities:

- Create a product.
- Modify a product price.
- Add a provider.
- Configure a branch.
- Generate a ticket.
- Update a catalog.

Examples of invalid client capabilities:

- Create a new `sbm_business.franchise`.
- Activate an uncontracted module.
- Change the commercial plan of the tenant.
- Provision a new business schema.
- Manage another brand or tenant.
- Modify global platform configuration.

### 1.4 Long-term vision

`dp-api` will become a production-grade domain API for a configurable, AI-assisted ERP.

The future architecture should allow:

- Self-service ERP configuration.
- Role-based client access.
- AI tool calling over explicit REST contracts.
- Auditable read and write operations.
- Human approval for sensitive AI-triggered actions.
- Integration with `sbm-manager` and future React applications.
- Independent deployment while sharing infrastructure with SBM Suite.

### 1.5 What this repository must not become

`dp-api` must not:

- Administer the global SBM platform.
- Create franchises or tenants.
- Control subscriptions or contracted modules.
- Provision schemas.
- Own platform-wide billing.
- Own internal SBM users.
- Implement AI orchestration or LLM prompts.
- Allow an LLM to bypass domain validations.
- Access another brand's schema without an explicit architecture decision.
- Duplicate business logic in `sbm-ai-assistant`.

---

## 2. Terminology and ownership model

### 2.1 Client user

A **client user** is a person belonging to the business using the ERP, initially Ditaly Pasta.

The client user interacts primarily with `dp-api`, directly through a frontend or indirectly through `sbm-ai-assistant`.

### 2.2 Internal SBM user

An **internal SBM user** administers the platform itself.

Typical internal operations belong to `sbm-api`, including:

- Creating a franchise or tenant.
- Activating modules.
- Managing plans and service availability.
- Suspending an account.
- Provisioning schemas.
- Managing global platform configuration.

### 2.3 API ownership rule

```text
Client operation
→ dp-api

Platform or contractual operation
→ sbm-api
```

A table being located in the shared `sbm_business` schema does not automatically mean that client-facing functionality belongs to `sbm-api`.

Ownership must be decided by **who is allowed to execute the operation and which domain owns the rule**, not only by physical schema location.

### 2.4 Important example

`Product` belongs functionally to `dp-api` because a client user can create and modify products.

`Franchise` belongs functionally to `sbm-api` because creating a franchise implies provisioning or contracting an additional platform service.

---

## 3. Current state

### 3.1 General status

The repository exists, runs locally with Docker, connects to PostgreSQL, exposes Django REST Framework endpoints, and provides a Django Jazzmin admin interface.

Local validation completed on 2026-07-14:

```text
http://localhost:8081/admin
```

The admin loaded successfully and displayed the registered modules for authentication, authorization, branches, business, pricing, products, providers, tickets, and users.

### 3.2 Current status classification

```text
Repository: active
Environment validated: local development
Deployment target: production
Migration/refactor status: pending
AI integration status: not started
```

### 3.3 Current application modules

Implemented Django apps:

1. `users`
2. `authz`
3. `documentation`
4. `products`
5. `providers`
6. `pricing`
7. `sales`
8. `ticket`
9. `branches`
10. `business`

### 3.4 Current platform components

- Django 4.2.x.
- Django REST Framework 3.14.
- PostgreSQL.
- Django Filter.
- Django CORS Headers.
- Django Jazzmin.
- Docker Compose.
- External Docker network `sbm-network`.
- Session and Basic authentication configured globally.
- DRF token endpoint exposed, but token authentication is not configured globally in `REST_FRAMEWORK`.

### 3.5 Current local container configuration

Service:

```text
api
```

Container:

```text
dp-core
```

Internal application port:

```text
8000
```

Validated public port:

```text
8081
```

The host port is configured through:

```text
API_PUBLIC_PORT
```

### 3.6 Coexistence with `sbm-api`

Validated target local mapping:

```text
sbm-api → localhost:8082 → container port 8000

dp-api  → localhost:8081 → container port 8000
```

Both APIs can use port `8000` internally because they run in separate containers. The host ports and container names must remain different.

Both services currently share:

```text
sbm-network
```

---


### 3.7 Latest validated implementation progress — 2026-07-17

The first backend portion of the `Product` vertical migration is now implemented and validated in `dp-api`.

The migration boundary remains:

```text
Ditaly Pasta client operation
→ sbm-manager
→ dp-api

Internal or critical platform operation
→ sbm-api
```

The next concrete Product backend task is to correct SKU generation in
`dp-api`. The existing implementation in the Product app of `sbm-api` will be
provided by the user and must be inspected as the behavioral reference before
making changes. This does not change the ownership boundary: Product remains a
client operation owned by `dp-api`. The broader migration of the Product
consumer in `sbm-manager` remains pending and must continue against the
canonical `dp-api` contract.

#### `products/models.py`

- `Product.group` was renamed to `Product.item_group`.
- The mapped database column remains `item_group`.
- `Product.price` was changed from a scalar field to a foreign key targeting `pricing.Price.code`.
- Main domain relationships were changed to protective deletion behavior where appropriate.
- The model remains unmanaged because Flyway owns the schema.
- The legacy PostgreSQL column `gross_price` remains database-only. Existing rows contain `0`; the commercial value exposed by the API is `Price.gross_amount` through `price_gross_amount`.

#### `products/admin.py`

All stale references to `group` were replaced with `item_group` in:

- `list_display`;
- `list_filter`;
- `fieldsets`.

Validation result:

```text
System check identified no issues (0 silenced).
```

#### `products/serializers.py`

`ProductSerializer` now exposes the validated Product contract, including:

```text
price
price_gross_amount
item_group
item_group_name
provider_name
type_name
category_name
package_description
```

Stale Product response fields such as `group`, `group_name`, and `price_description` are no longer exposed.

The internal `log` field is intentionally not exposed by Product serializers. It is an audit/tamper-detection field and must remain database-side.

#### `products/views.py`

`filterset_fields` was updated from `group` to `item_group`.

The Product endpoint intentionally supports:

```text
GET
POST
PATCH
HEAD
OPTIONS
```

Full update through `PUT` and physical deletion through HTTP `DELETE` are disabled and return HTTP 405.

Logical deletion uses:

Method:

```text
POST
```

```text
/api/products/{id}/delete/
```

Normal Product querysets exclude logically deleted rows.

Audit behavior implemented for Product:

```text
INIT: <timestamp> (USER: <user_code>);
PATCH: field='value', ... (USER: <user_code>);
DELETE: <timestamp> (USER: <user_code>);
```

Every log entry must end in `;`. PATCH automatically sets `updated_at`; logical deletion sets `is_active=False`, `is_deleted=True`, `deleted_at`, and `deleted_by`.

Product confirmation is managed entirely by the backend using the current
transitional business-user audit contract:

- A Product created without `is_confirmed`, or with `is_confirmed=false`, is
  stored with `is_confirmed=false`, `confirmed_at=NULL`, and
  `confirmed_by=NULL`.
- A Product created with `is_confirmed=true` receives `confirmed_at` from the
  server clock and `confirmed_by=created_by`.
- A PATCH with `is_confirmed=true` receives `confirmed_at` from the server
  clock and `confirmed_by=updated_by`.
- A PATCH with `is_confirmed=false` clears `confirmed_at` and `confirmed_by`.
- Repeating `is_confirmed=true` preserves an existing complete confirmation
  audit, but repairs missing audit fields on legacy/inconsistent rows.
- `confirmed_at` and `confirmed_by` are read-only request fields and cannot be
  supplied or falsified by the frontend.

Confirmation log behavior is:

```text
INIT: <timestamp> (USER: <created_by>) (confirmed);
PATCH: is_confirmed=True (USER: <updated_by>);
PATCH: is_confirmed=False (USER: <updated_by>);
```

Authorization and role checks are intentionally outside this feature because
the definitive role system and the mapping between Django authentication users
and business users are not implemented. `created_by` and `updated_by` continue
to be validated against `users.User.code`; their client-supplied nature remains
a documented transitional spoofing risk.

#### `pricing/models.py`

The old Django model referenced fields that do not match the live PostgreSQL table. Observed failures included:

```text
column price.price_fiscal_configuration does not exist
```

and:

```text
column price.record_type does not exist
```

A current data extraction from PostgreSQL confirmed the real columns of `ditaly_pasta.price` include:

```text
id
code
base_net_amount
net_amount
gross_amount
iva_amount
aditional_tax_amount
retention_amount
price_configuration
is_current
is_deleted
is_confirmed
created_at
created_by
record_item_code
price_record_type
```

The correct field is therefore:

```text
price_record_type
```

not:

```text
record_type
```

The Django mapping was aligned with those confirmed columns. The DBML documentation was identified as stale for `price_record_type` and must still be synchronized separately.

#### `pricing` consumers

`pricing/admin.py`, `pricing/serializers.py`, and `pricing/views.py` were synchronized with the final `Price` mapping. Stale Price references such as `record_type`, `price_fiscal_configuration`, and `is_active` were removed from the Price flow. References to `price_fiscal_configuration` that remain in `FiscalConfigurationDetail` are valid and belong to that separate model.

#### Current validation state

- Django system checks: passing.
- `GET /api/products/`: HTTP 200 with standard pagination.
- `GET /api/products/{id}/`: HTTP 200 for visible products.
- `GET /api/prices/`: HTTP 200.
- Product CREATE: validated with HTTP 201.
- Product PATCH: validated with HTTP 200 and automatic `updated_at`.
- Product logical delete: validated; the row remains in PostgreSQL and disappears from normal Product endpoints.
- Product create/PATCH confirmation and unconfirmation audit: validated.
- Product confirmation through the real PATCH endpoint was revalidated against
  PostgreSQL on 2026-07-17: `is_confirmed=true` automatically persists
  `confirmed_at`, `confirmed_by`, `updated_at`, and `updated_by`. A legacy row
  already marked confirmed but missing confirmation audit is repaired when the
  PATCH reaches the current `dp-api` Product endpoint.
- Product confirmation audit fields cannot be overridden by request payloads.
- Product HEAD list and detail: HTTP 200.
- Product PUT and HTTP DELETE: HTTP 405.
- No Django migration was created.
- PostgreSQL structure was not altered.
- Product-specific automated tests: 11 passing.

Audit identity is not hardcoded. At present `created_by`, `updated_by`, and `deleted_by` are validated against `users.User.code` but are supplied by the client request. This is a known spoofing risk caused by the unresolved mapping between Django authentication users and business users. It belongs to the later authentication/security phase and must not displace the immediate Product frontend migration.

## 4. Current architecture

### 4.1 Runtime flow

```text
Client / Admin / API consumer
→ Django URL router
→ DRF ViewSet
→ Serializer
→ Django unmanaged model
→ PostgreSQL
→ ditaly_pasta or sbm_business schema
```

### 4.2 Current repository structure

```text
DP-API/
├── .dockerignore
├── .env.dev
├── .env.prod
├── .gitignore
├── .vscode/
│   └── settings.json
├── authz/
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── serializers.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
├── branches/
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── serializers.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
├── business/
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── serializers.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
├── core/
│   ├── Dockerfile
│   ├── entrypoint.sh
│   ├── requirements.txt
│   ├── settings.py
│   ├── urls.py
│   ├── views.py
│   ├── asgi.py
│   └── wsgi.py
├── documentation/
├── pricing/
├── products/
├── providers/
├── sales/
├── ticket/
├── users/
├── templates/
│   └── home.html
├── TECHNICAL_DOCUMENTATION.md
├── command.md
├── db.sqlite3
├── docker-compose.yml
└── manage.py
```

### 4.3 Django settings

The active local environment is loaded directly in `core/settings.py`:

```python
environ.Env.read_env(os.path.join(BASE_DIR, '.env.dev'))
```

The production environment line exists but is commented:

```python
# environ.Env.read_env(os.path.join(BASE_DIR, '.env.prod'))
```

This is temporary and should be replaced by environment-driven selection before production.

### 4.4 Database search path

The PostgreSQL connection uses:

```text
search_path=ditaly_pasta,sbm_business,public
```

Consequences:

- Unqualified table names are resolved first in `ditaly_pasta`.
- Shared tables can be resolved from `sbm_business`.
- Django models use `db_table` names without schema qualification.
- Duplicate table names across schemas would create ambiguity and must be avoided or explicitly qualified.

### 4.5 Database migration ownership

Django migrations are disabled for all business apps:

```text
users
authz
documentation
products
providers
pricing
sales
ticket
branches
business
```

The repository states that database evolution is managed externally with Flyway.

Therefore:

- Django models are mappings to an existing database structure.
- `makemigrations` is not the source of truth for business tables.
- Database changes must be coordinated with DBML/Flyway scripts.
- Model changes without database changes can break runtime access.

---

## 5. Application responsibilities

### 5.1 `users`

Current purpose:

- Client-scoped user types.
- Client-scoped users.
- User tokens represented in business tables.

Current models:

- `UserType`
- `User`
- `UserToken`

Current endpoints:

```text
/api/user-types/
/api/users/
/api/user-tokens/
```

Architectural note:

The repository also uses Django's built-in authentication system for admin/session access. The custom `users.User` model is not configured as `AUTH_USER_MODEL`, so two user concepts currently coexist and must be clarified before production.

### 5.2 `authz`

Current purpose:

- Client-facing roles.
- Permissions.
- Restrictions.
- Role-permission associations.
- Restriction-role associations.

Current models:

- `PermissionType`
- `Permission`
- `Role`
- `RolePermissions`
- `Restriction`
- `RestrictionRoles`

Current endpoints:

```text
/api/permission-types/
/api/permissions/
/api/roles/
/api/role-permissions/
/api/restrictions/
/api/restriction-roles/
```

Target rule:

Client administrators may manage only permissions and roles within the scope allowed by their contracted modules and tenant. They must not create platform-wide capabilities.

### 5.3 `documentation`

Current purpose:

- Instruction types.
- Operational instructions referenced by packages, catalogs, or other business objects.

Current models:

- `InstructionType`
- `Instruction`

Current endpoints:

```text
/api/instruction-types/
/api/instructions/
```

This app is business documentation metadata, not the Confluence RAG pipeline. The RAG pipeline belongs to `sbm-ai-assistant`.

### 5.4 `products`

Current purpose:

- Menus.
- Item categories.
- Item types.
- Item groups.
- Package types.
- Transport types.
- Units of measure.
- Packages.
- Catalogs.
- Item configurations.
- Products.
- Materials.
- Services.

Current models:

- `Menu`
- `ItemCategory`
- `ItemType`
- `ItemGroup`
- `PackageType`
- `TransportType`
- `MeasureUnit`
- `Package`
- `Catalog`
- `ItemConfiguration`
- `ItemConfigurationDetail`
- `Product`
- `Material`
- `Service`

Current endpoints:

```text
/api/menus/
/api/item-categories/
/api/item-types/
/api/item-groups/
/api/package-types/
/api/transport-types/
/api/measure-units/
/api/packages/
/api/catalogs/
/api/item-configurations/
/api/item-configuration-details/
/api/products/
/api/materials/
/api/services/
```

This is the first migration focus because overlapping and newer product-domain implementations currently exist in `sbm-api`.

### 5.5 `providers`

Current purpose:

- Provider types and groups.
- Regions and districts.
- Banks and bank account types.
- Providers.

Current endpoints:

```text
/api/provider-types/
/api/provider-groups/
/api/regions/
/api/districts/
/api/banks/
/api/bank-account-types/
/api/providers/
```

Some referenced lookup tables may physically live in `sbm_business`, but client-facing provider operations belong to `dp-api`.

The `Provider` resource uses the Product reference pattern for Hexagonal
Architecture: REST controllers delegate to application use cases, use cases
depend on the domain repository port, and Django ORM is the persistence
adapter. Provider types, groups, regions, districts, banks, and bank account
types remain in the existing layered architecture.

The Provider vertical migration is implemented. The original selector failure
was caused by a DRF serializer mismatch: the declared fields were named
`district_name` and `region_name`, while the public field list expected
`dispatch_district_name` and `dispatch_region_name`. This caused
`GET /api/providers/` to return HTTP 500 before serializing results.

The repaired list contract returns HTTP 200 with standard pagination:

```text
count
next
previous
results
```

Selector consumers use these Provider fields:

```text
id
code
provider
type
type_name
```

The full Provider representation retains contact, company, banking, dispatch,
status, audit, and version fields. List, detail, search, POST, PATCH, and DELETE
were validated locally; write smoke tests were executed inside rolled-back
transactions.

PostgreSQL remains authoritative for Provider persistence. Relevant corrected
mappings are:

```text
provider.code          → varchar(10)
material.provider      → integer → provider.id
service.provider       → integer → provider.id
```

No Django migration was generated or executed for these mapping corrections.

### 5.6 `pricing`

Current purpose:

- Fiscal directive types.
- Fiscal directives.
- Fiscal formulas.
- Price fiscal configurations.
- Prices.
- Fiscal configuration details.

Current endpoints:

```text
/api/fiscal-directive-types/
/api/fiscal-directives/
/api/fiscal-formulas/
/api/price-fiscal-configurations/
/api/prices/
/api/fiscal-configuration-details/
```

The client may modify prices and permitted commercial configurations. Global fiscal or platform policy ownership must be reviewed table by table.

### 5.7 `ticket`

Current purpose:

- Client-created operational or support tickets.

Current model:

- `Ticket`

Current endpoint:

```text
/api/tickets/
```

Tickets initiated by a client user belong to the client-facing API. Internal SBM workflow or escalation may later interact through `sbm-api` or automation, but the client request begins in `dp-api`.

### 5.8 `branches`

Current purpose:

- Branch types.
- Branches.
- External platforms.
- Platform details by branch.
- Companies with agreements.
- Agreements.
- Agreement details.

Current models:

- `BranchType`
- `Branch`
- `Platform`
- `PlatformDetail`
- `CompanyAgreement`
- `Agreement`
- `AgreementDetail`

Current endpoints:

```text
/api/branch-types/
/api/branches/
/api/platforms/
/api/platform-details/
/api/company-agreements/
/api/agreements/
/api/agreement-details/
```

### 5.9 `business`

Current purpose:

- Generic business lookup or filtering concepts.

Current model:

- `ItemFilterClassification`

Current endpoint:

```text
/api/item-filter-classifications/
```

This app is small and its long-term boundary should be reassessed as the domain model becomes clearer.

### 5.10 `sales`

Current status:

- App exists.
- Router exists.
- No confirmed active business models or registered endpoints.

Target:

- Sales operations should be implemented only after their business contracts and ownership are defined.

---

## 6. API surface

### 6.1 General endpoints

Method: GET

```text
/
```

Method: GET

```text
/api/
```

Method: GET

```text
/api/health/
```

Method: GET

```text
/api/info/
```

Method: GET/POST depending on Django admin flow

```text
/admin/
```

### 6.2 Authentication endpoints

Method: GET/POST depending on DRF session flow

```text
/api-auth/
```

Method: POST

```text
/api-token-auth/
```

### 6.3 CRUD pattern

Most domain endpoints are registered with DRF routers and ViewSets.

Expected standard operations where permitted:

```text
GET    /api/<resource>/
POST   /api/<resource>/
GET    /api/<resource>/<id>/
PUT    /api/<resource>/<id>/
PATCH  /api/<resource>/<id>/
DELETE /api/<resource>/<id>/
```

Actual permissions, filters, lookup fields, and serializer behavior must be validated per ViewSet before exposing them to a frontend or AI Tool.

---

## 7. Authentication and authorization

### 7.1 Current global DRF authentication

Configured classes:

- `SessionAuthentication`
- `BasicAuthentication`

Configured permission:

- `IsAuthenticated`

### 7.2 Current inconsistency

The project exposes:

```text
/api-token-auth/
```

But `TokenAuthentication` is not currently included in `DEFAULT_AUTHENTICATION_CLASSES`.

This means obtaining a DRF token does not automatically guarantee that protected endpoints accept it.

### 7.3 Two user systems

Current repository contains:

1. Django built-in `auth.User` for admin/session authentication.
2. Custom business table `users.User` for domain users.

This is a major architectural decision still unresolved.

Before production, define whether:

- The custom user becomes the Django authentication user.
- Django auth remains internal and maps to domain users.
- Authentication is delegated to `sbm-api` or an identity provider.
- JWT or another token model is introduced.

### 7.4 Target authorization model

Every client request should resolve:

```text
identity
→ tenant/franchise context
→ active contracted modules
→ role
→ permission
→ restriction
→ requested business object
```

Target guarantees:

- A client user cannot act outside their tenant.
- A client user cannot activate platform services.
- A client user cannot create a franchise.
- AI-generated Tool calls execute with the same permissions as the requesting user.
- Write actions remain auditable.

---

## 8. Database ownership

### 8.1 Schemas

Current PostgreSQL schemas relevant to this project:

```text
ditaly_pasta
sbm_business
public
```

### 8.2 Domain ownership principle

Physical schema and API ownership are related but not identical.

Recommended interpretation:

```text
ditaly_pasta
→ brand-specific operational and commercial data

sbm_business
→ shared platform data, global references, and internal platform entities
```

However, a client-facing operation may read shared lookup data from `sbm_business` through `dp-api`.

### 8.3 Tables expected to be primarily owned by `dp-api`

Brand-specific or client-operational examples:

- `ditaly_pasta.catalog`
- `ditaly_pasta.item_configuration`
- `ditaly_pasta.item_configuration_detail`
- `ditaly_pasta.product`
- `ditaly_pasta.material`
- `ditaly_pasta.service`
- `ditaly_pasta.provider`
- `ditaly_pasta.price`
- `ditaly_pasta.price_configuration`
- `ditaly_pasta.price_configuration_detail`
- `ditaly_pasta.fiscal_configuration_detail`
- `ditaly_pasta.ticket`
- `ditaly_pasta.branches`
- `ditaly_pasta.platform`
- `ditaly_pasta.platform_detail`
- `ditaly_pasta.company_agreements`
- `ditaly_pasta.agreements`
- `ditaly_pasta.agreement_detail`

### 8.4 Shared tables that `dp-api` may consume

Examples:

- Menus.
- Item groups.
- Item categories.
- Item types.
- Package types.
- Transport types.
- Measure units.
- Provider types.
- Regions.
- Districts.
- Banks.
- Bank account types.
- Instruction types.
- Instructions.
- Client-scoped role and permission definitions, depending on final design.

### 8.5 Internal platform tables that clients must not create

Primary confirmed example:

- `sbm_business.franchise`

Other platform-controlled concepts should include:

- Tenant provisioning.
- Contracted modules.
- Platform subscriptions.
- Service activation.
- Global configuration.

### 8.6 Database source of truth

The complete supplied DBML is the current high-level database reference.

Before any model migration:

1. Compare the Django model.
2. Compare the DBML table.
3. Compare the actual PostgreSQL table.
4. Compare the corresponding `sbm-api` model.
5. Decide ownership.
6. Update Flyway/database migration scripts if the physical schema changes.
7. Update Django mapping.

---

## 9. Migration from `sbm-api`

### 9.1 Why migration is required

During the latest development period, functionality that should have been implemented in `dp-api` was implemented in `sbm-api` due to time constraints.

This created overlap in areas such as:

- Products.
- Materials.
- Services.
- Catalogs.
- Prices.
- Providers.
- Clients.
- Tickets.
- Orders and operational processes.

### 9.2 Migration objective

Restore the intended boundary before integrating `sbm-ai-assistant` with business Tools.

Reason:

If AI Tools are built against incorrectly owned endpoints, the following would later require rework:

- Tool contracts.
- Authentication.
- Permissions.
- Prompt/tool descriptions.
- API clients.
- Tests.
- Audit rules.

### 9.3 Migration rule

Do not copy entire apps blindly.

For each vertical capability:

```text
model
→ database table
→ serializer
→ ViewSet
→ route
→ permission
→ frontend consumer
→ tests
→ AI Tool contract
```

### 9.4 First migration slice

The first migration slice is `Product`.

Required comparison:

```text
sbm-api/catalog Product
↔ dp-api/products Product
↔ DBML product table
↔ actual PostgreSQL product table
```

The migration should establish the canonical implementation in `dp-api` before removing anything from `sbm-api`.

### 9.5 Current known `Product` concerns

The following backend differences were resolved in `dp-api`:

- Price representation and relationship.
- `group` versus `item_group` naming.
- Foreign-key delete policies.
- Product and Price mappings against live PostgreSQL.
- Read, create, partial update, HEAD, and logical-delete behavior.
- Product audit-log formatting and API concealment.

Remaining work for the Product vertical slice:

- Inspect the Product app supplied from `sbm-api` and document its current SKU
  generation algorithm, inputs, format, uniqueness rules, and concurrency
  behavior.
- Implement the canonical Product SKU generation rule in the hexagonal
  `dp-api` Product flow without coupling the domain/application layers to
  Django ORM or HTTP.
- Redirect the `sbm-manager` Product consumer from `sbm-api` to `dp-api`.
- Adapt frontend fields and actions to the canonical `dp-api` contract.
- Add regression tests.
- Resolve authenticated business-user attribution in the later security phase.
- Deprecate the equivalent `sbm-api` Product endpoint only after frontend validation.

### 9.6 Safe migration sequence

1. Identify the canonical database structure.
2. Identify the canonical business behavior.
3. Update `dp-api` model mapping.
4. Update serializer.
5. Update ViewSet and filters.
6. Update endpoint contract.
7. Validate CRUD in `dp-api`.
8. Update `sbm-manager` consumer.
9. Add regression tests.
10. Deprecate equivalent `sbm-api` endpoint.
11. Remove duplicate implementation only after all consumers migrate.

### 9.7 Migration order after `Product`

Recommended order:

1. Product.
2. Material.
3. Service.
4. Catalog and item configuration.
5. Prices and commercial configuration.
6. Providers.
7. Branches.
8. Tickets.
9. Clients, after confirming the current implementation location and schema.
10. Orders and remaining Ditaly Pasta operational workflows.

### 9.8 What remains in `sbm-api`

`sbm-api` should retain platform and internal responsibilities such as:

- Franchise/tenant creation.
- Contracted-module activation.
- Platform-level users.
- Global administration.
- Provisioning.
- Internal audit and operations.
- Shared platform services that are not client-owned.

---

## 10. Integration with `sbm-manager`

### 10.1 Current intended frontend

`sbm-manager` is the main Vue.js 3 enterprise interface.

For Ditaly Pasta client operations, the target flow is:

```text
sbm-manager
→ dp-api
```

### 10.2 Frontend migration rule

Any screen currently calling `sbm-api` for a Ditaly Pasta client operation must be redirected to the equivalent `dp-api` endpoint after the endpoint is validated.

Current Product migration state:

```text
dp-api Product backend contract → validated
dp-api Product SKU generation    → next active task; SBM-API source pending
sbm-manager Product consumer     → pending migration work
sbm-api Product endpoint         → retained until consumer migration passes
```

### 10.3 No direct client access to internal API

The primary design goal is:

```text
Client frontend
X→ sbm-api for normal operations
```

Exceptions must be explicit and justified, not accidental.

---

## 11. Integration with `sbm-ai-assistant`

### 11.1 Role of `dp-api`

`dp-api` will be the domain boundary used by AI Tools for Ditaly Pasta operations.

Examples:

```text
“Show the current price of product X”
→ sbm-ai-assistant
→ dp-api read Tool
→ Price/Product endpoint
```

```text
“Create a new product with these values”
→ sbm-ai-assistant
→ structured validation
→ approval when required
→ dp-api write Tool
→ Product endpoint
```

### 11.2 API remains authoritative

The LLM must not:

- Calculate business values outside the API when the API owns the rule.
- Write directly to PostgreSQL.
- Invent identifiers.
- Skip permission checks.
- Convert a rejected domain operation into a successful response.

### 11.3 First AI integration

Do not integrate AI until the first migrated domain endpoint is stable.

Recommended first Tool:

- Read-only product lookup, or
- Read-only current price lookup.

### 11.4 Future write Tools

Write operations require:

- Authenticated requesting user.
- Tenant context.
- Structured inputs.
- API-side validation.
- Audit trail.
- Idempotency where relevant.
- Human approval for sensitive operations.

---

## 12. Docker and environments

### 12.1 Current Compose service

```yaml
services:
  api:
    container_name: dp-core
    build: ./core
    command: sh -c "sleep 10s; python manage.py runserver 0.0.0.0:8000"
```

### 12.2 Current volume strategy

Each Django app is mounted individually into `/usr/src/app`.

This works for development but increases Compose maintenance whenever a new app is added.

Possible future simplification:

```yaml
volumes:
  - .:/usr/src/app
```

Do not change this during the domain migration unless necessary.

### 12.3 Current startup behavior

The service waits with:

```text
sleep 10s
```

This is fragile because it assumes the database becomes available within a fixed time.

Future production-grade behavior:

- Database readiness check.
- Controlled entrypoint.
- Gunicorn or another production WSGI server.
- Healthcheck.
- Restart policy.

### 12.4 Development versus production

Current command:

```text
python manage.py runserver 0.0.0.0:8000
```

Valid for development only.

Production target should use a production server and production settings.

### 12.5 Environment variable behavior

Compose variables such as:

```text
${API_PUBLIC_PORT}
```

are resolved from:

- Shell environment.
- Default `.env` next to Compose.
- Explicit Compose `--env-file`.

The `environment:` block injects resolved values into the container.

The current Django settings also read `.env.dev` from the mounted project path, creating two overlapping environment-loading mechanisms. This should be simplified later.

### 12.6 Shared network

Current network:

```text
sbm-network
```

It is external and must exist before Compose starts.

---

## 13. Development conventions

### 13.1 Hybrid architecture

The long-term architectural objective of `dp-api` is a **Hybrid Architecture**.
Architecture is selected per business domain according to its complexity, not
applied as a repository-wide rewrite:

- **Layered Architecture** remains the default for CRUD-oriented and simple
  domains whose behavior is adequately expressed by ViewSets, serializers,
  models, and database constraints.
- **Hexagonal Architecture** is used for business-critical domains with
  complex rules, workflows, audit requirements, external integrations, or a
  high expected rate of change.

The existing layered flow remains valid for simple modules:

```text
urls
→ ViewSets
→ serializers
→ models
→ PostgreSQL
```

Hexagonal domains use explicit ports and adapters:

```text
REST adapter / controller
→ application use case
→ domain entity and repository port
→ Django ORM repository adapter
→ PostgreSQL
```

`Product` is the first vertical migration and the reference implementation for
future hexagonal modules. This decision does not authorize migration of other
modules as part of Product work.

### 13.2 Responsibilities

#### Models

- Map actual database tables.
- Define relationships.
- Avoid hidden cross-domain logic.

#### Serializers

- Validate request and response contracts.
- Avoid owning complex business workflows.

#### ViewSets

- Handle HTTP/API concerns.
- Enforce authentication and permissions.
- Delegate complex behavior when service layers are introduced.

#### Database/Flyway

- Own physical schema changes.
- Remain synchronized with DBML and Django models.

### 13.3 Endpoint communication preference

When documenting an endpoint:

- State the HTTP method separately.
- Write the path as plain text.
- Do not include the method inside the endpoint block.

### 13.4 Work cadence

Development changes should be implemented and validated one step at a time.

Do not provide or execute the next migration change until the current one is validated.

### 13.5 Portfolio rule

Every refactor or feature should be evaluated against:

- Architectural necessity.
- Business value.
- Portfolio value.
- Migration risk.

Do not expand the project indefinitely with technologies that do not improve those goals.

---

## 14. Repository visual identity

The repository uses a VS Code title-bar color to distinguish it from other projects.

Color convention across the ecosystem:

```text
Red     → internal APIs
Blue    → database
Green   → frontend
Yellow  → AI
Orange  → client-facing API (`dp-api`)
Cyan    → future React public application
```

Current intended `dp-api` title-bar colors:

```json
{
  "workbench.colorTheme": "Default Dark+",
  "workbench.colorCustomizations": {
    "titleBar.activeBackground": "#D97706",
    "titleBar.activeForeground": "#ffffff",
    "titleBar.inactiveBackground": "#92400E",
    "titleBar.inactiveForeground": "#cccccc"
  }
}
```

Purpose:

- Prevent accidental modifications in the wrong Python API repository.
- Make the client-facing API visually distinct from the red internal `sbm-api`.

---

## 15. Testing

### 15.1 Current state

Every app contains a `tests.py` file, but no meaningful automated test suite was confirmed during inspection.

Dependencies include:

- `pytest`
- `pytest-django`
- `coverage`

### 15.2 Required test categories

1. Model mapping tests.
2. Serializer validation tests.
3. ViewSet permission tests.
4. CRUD API tests.
5. Tenant isolation tests.
6. Cross-schema relationship tests.
7. Regression tests against migrated `sbm-api` behavior.
8. AI Tool contract tests after integration.

### 15.3 Migration acceptance tests

For each migrated resource:

- List works.
- Retrieve works.
- Create works when permitted.
- Update works when permitted.
- Delete behavior is correct.
- Invalid foreign keys fail safely.
- A client user cannot cross tenant boundaries.
- `sbm-manager` continues to work.
- Old `sbm-api` endpoint can be deprecated safely.

---

## 16. Security

### 16.1 Current risks

- `CORS_ALLOW_ALL_ORIGINS = True` is active.
- Basic authentication is globally enabled.
- Token endpoint and accepted authentication classes are inconsistent.
- Two user systems coexist.
- Tenant isolation is not confirmed.
- No confirmed object-level permission enforcement.
- Environment files were included in the shared repository ZIP.
- Development server is used.
- Existing technical documentation contained credential examples that must not be considered safe defaults.

### 16.2 Required production controls

- Explicit allowed origins.
- Production secret management.
- Strong authentication strategy.
- Tenant-aware permissions.
- Object-level authorization.
- Audit logs.
- Rate limiting.
- Secure error handling.
- No secrets committed to Git.
- Credential rotation if any shared values were real.
- Separate internal and client administrator privileges.

### 16.3 AI security

Future AI Tools must:

- Use the requester's identity.
- Respect API authorization.
- Never use an unrestricted technical superuser token for client actions.
- Require approval for critical writes.
- Record tool name, parameters, result, user, tenant, and timestamp.

---

## 17. Technical debt

### High priority

1. Resolve the `dp-api` versus `sbm-api` domain overlap.
2. Complete the first vertical migration with `Product`.
3. Clarify the canonical database schema and Flyway migration source.
4. Resolve the two-user-system architecture.
5. Align token endpoint with accepted authentication classes.
6. Implement client/tenant isolation.
7. Remove permissive CORS for non-development environments.
8. Remove secrets and local runtime artifacts from repository packages.
9. Replace hardcoded `.env.dev` loading with environment-driven settings.
10. Add meaningful tests before removing duplicated `sbm-api` endpoints.

### Medium priority

1. Replace fixed `sleep 10s` with database readiness.
2. Replace `runserver` for production.
3. Simplify Docker volumes.
4. Add healthcheck and restart policy.
5. Normalize model field names against DBML.
6. Review `CASCADE`, `PROTECT`, and `SET_NULL` policies.
7. Review audit fields repeated across models.
8. Introduce a service layer for complex workflows.
9. Verify pagination, filtering, and ordering per endpoint.
10. Generate accurate OpenAPI documentation.

### Low priority

1. Modernize legacy technical documentation.
2. Remove decorative or obsolete project text.
3. Split large model files by domain if complexity warrants it.
4. Add frontend-oriented API documentation.
5. Add AI-specific endpoint annotations after Tool contracts exist.

---

## 18. Architectural decisions

### 18.1 Client-facing API separated from internal API

**Decision:** `dp-api` serves client users; `sbm-api` serves internal platform administration.

**Reason:** Prevent clients from directly accessing platform-level operations and establish a stable domain boundary for frontends and AI Tools.

### 18.2 Client self-service

**Decision:** Most operational configuration should be available to authorized client users.

**Examples:** products, prices, providers, branches, catalogs, tickets.

**Reason:** The ERP must be interactive and configurable without routine internal SBM assistance.

### 18.3 Franchise creation remains internal

**Decision:** A client cannot create `sbm_business.franchise`.

**Reason:** Creating a franchise implies contracting, provisioning, or activating an additional platform service.

### 18.4 AI uses APIs, not databases

**Decision:** `sbm-ai-assistant` calls `dp-api` through Tools.

**Reason:** Preserve validation, permissions, transactions, and auditability.

### 18.5 Migration before AI integration

**Decision:** Correct API ownership before building LLM Tools.

**Reason:** Avoid reworking Tool contracts and permissions later.

### 18.6 Vertical migration

**Decision:** Migrate one complete capability at a time, beginning with `Product`.

**Reason:** Reduce risk and make each change independently testable.

### 18.7 Flyway/database remains authoritative

**Decision:** Business schema changes are not generated automatically by Django migrations.

**Reason:** The existing architecture disables migrations for domain apps and uses an externally managed database.

### 18.8 Hybrid architecture by domain complexity

**Decision:** `dp-api` combines Layered Architecture for simple CRUD domains
with Hexagonal Architecture for business-critical domains.

**Reason:** A universal rewrite would introduce unnecessary abstraction in
simple modules and excessive migration risk. Incremental, vertical migrations
allow one complete domain to be isolated, validated, and used as a reference
before another candidate is authorized.

The migration unit is always a complete vertical capability:

```text
REST contract
→ presentation adapter
→ application use cases
→ domain rules and ports
→ Django ORM persistence adapter
→ existing PostgreSQL/Flyway schema
→ regression validation
```

Migrations must preserve public contracts and database ownership. They do not
permit `makemigrations`, `migrate`, schema duplication, or moving internal SBM
responsibilities into `dp-api`.

---

## 19. Rules that must remain stable

1. Client users use `dp-api` for normal Ditaly Pasta operations.
2. Internal platform administrators use `sbm-api` for platform operations.
3. A client user cannot create a franchise or tenant.
4. A client user cannot activate an uncontracted module.
5. Products, materials, services, prices, providers, branches, and client tickets belong functionally to `dp-api`.
6. Physical schema location alone does not determine API ownership.
7. `sbm-ai-assistant` must call APIs, not the ERP database directly.
8. Business validations must remain in the responsible API.
9. AI write actions must use the requesting user's permissions.
10. Do not remove duplicated `sbm-api` functionality before consumers migrate and tests pass.
11. Database, DBML, Flyway, and Django model definitions must remain synchronized.
12. Changes must be implemented and validated one step at a time.
13. Do not add multi-agent or MCP work before the first stable `dp-api` Tool exists.
14. Do not expose internal platform administration through `dp-api`.
15. Do not publish environment secrets.

---

## 20. Roadmap

### Legend

- ✅ Completed
- 🚧 In progress
- ⏳ Pending

### Phase 0 — Existing API foundation

- ✅ Django project.
- ✅ Django REST Framework.
- ✅ PostgreSQL connection.
- ✅ Multi-schema search path.
- ✅ Docker Compose.
- ✅ Jazzmin admin.
- ✅ Domain apps and routers.
- ✅ Local runtime validation.

### Phase 1 — Establish domain boundary

- ✅ Define client user versus internal SBM user.
- ✅ Define `dp-api` as client-facing API.
- ✅ Define `sbm-api` as internal platform API.
- ✅ Confirm franchise creation as internal-only.
- ✅ Produce persistent project context.
- ⏳ Create final ownership matrix by table and endpoint.

### Phase 2 — Product vertical migration

- ✅ Compare Product model in both APIs.
- ✅ Validate Product table against DBML and PostgreSQL.
- ✅ Select canonical fields and relationships.
- ✅ Update `dp-api` model mapping.
- ✅ Update serializer.
- ✅ Update ViewSet and filters.
- ✅ Validate the permitted Product operations: GET, POST, PATCH, HEAD, and logical delete.
- ✅ Establish Product as the first Hexagonal Architecture reference implementation.
- ✅ Add Product contract and application-use-case regression tests.
- 🚧 Correct Product SKU generation using the existing `sbm-api` Product app
  as the behavioral reference; source pending from the user.
- 🚧 Update `sbm-manager` consumer.
- ⏳ Deprecate Product endpoint in `sbm-api`.

### Phase 3 — Remaining catalog domain

- ⏳ Material.
- ⏳ Service.
- ⏳ Catalog.
- ⏳ Item configurations.
- ⏳ Packages and supporting lookup data.

### Phase 4 — Pricing and providers

- ⏳ Price ownership and relationships.
- ⏳ Fiscal configuration boundary.
- ✅ Provider hexagonal backend and `/api/providers/` selector contract.
- ⏳ Validate the repaired Provider selector in `sbm-manager`.
- ⏳ Shared geographic and banking lookup behavior.

### Phase 5 — Client operations

- ⏳ Branches.
- ⏳ Platforms.
- ⏳ Agreements.
- ⏳ Tickets.
- ⏳ Clients.
- ⏳ Orders and remaining operational workflows.

### Phase 6 — Security and tenancy

- ⏳ Authentication architecture.
- ⏳ Resolve custom user versus Django user.
- ⏳ Tenant context.
- ⏳ Object-level permissions.
- ⏳ Contracted-module validation.
- ⏳ Audit logging.

### Phase 7 — Production hardening

- ⏳ Production settings.
- ⏳ Secure CORS.
- ⏳ Secret management.
- ⏳ Gunicorn or equivalent.
- ⏳ Healthchecks.
- ⏳ Structured logs.
- ⏳ CI/CD.
- ⏳ Automated test suite.
- ⏳ Production deployment.

### Phase 8 — AI integration

- ⏳ Read-only Product Tool.
- ⏳ Read-only Price Tool.
- ⏳ Structured Tool errors.
- ⏳ User and tenant propagation.
- ⏳ Write Tools with approval.
- ⏳ Tool observability.

---

## Hexagonal Architecture Roadmap

Hexagonal migrations are incremental and vertical. A candidate is migrated
only when its scope is explicitly authorized, and each migration must preserve
the existing REST contract and Flyway-managed database mapping.

1. **Product (In Progress)** — establishes the reference structure and contains
   lifecycle, relationship, audit-log, PATCH, and logical-deletion rules that
   should not live in HTTP controllers.
2. **Provider (Implemented)** — contains supplier identity, contact, banking,
   dispatch, classification, confirmation, and audit data while providing a
   stable selector contract to client applications.
3. **Material** — combines units, packaging, suppliers, traceability, and
   future inventory or production constraints that require rules independent
   of the REST and persistence layers.
4. **Service** — can contain availability, costing, fulfillment, billing, and
   lifecycle rules that must remain stable across different delivery channels.
5. **Catalog** — coordinates publication, visibility, menus, product grouping,
   franchise conditions, and channel-specific presentation rules.
6. **Pricing** — contains fiscal calculations, price composition, effective
   price selection, and regulatory rules that benefit from isolated domain
   tests and replaceable data sources.
7. **Orders** — requires transactional workflows, state transitions,
   validations, idempotency, and coordination with pricing and inventory.
8. **Inventory** — owns stock invariants, reservations, adjustments, and
   concurrency-sensitive operations that must remain correct independently of
   the delivery mechanism.
9. **Ticket** — requires lifecycle transitions, assignment, priority, SLA,
   authorization, notification, and audit rules beyond basic CRUD behavior.
10. **Franchise / Tenant Provisioning** — is a critical cross-system workflow
   with contractual, security, and provisioning rules. It is a hexagonal
   candidate in its responsible internal platform service (`sbm-api`); its
   inclusion here does not transfer ownership or expose it through `dp-api`.
11. **AI Integration** — needs explicit ports for model providers and Tools,
   with approval, authorization, observability, and audit rules independent of
   a specific AI vendor.
12. **Workflow Automation** — requires durable state transitions, retries,
   idempotency, scheduling, and adapters for external systems.

`Product` remains the reference implementation. `Provider` is the second
implemented vertical migration. The other entries are future candidates, not
active refactoring scope.

---

## 21. Immediate next step

### 21.1 Current exact objective

Correct Product SKU generation in `dp-api`, using the existing Product app from
`sbm-api` as the behavioral reference while preserving the hexagonal Product
architecture and the current REST contract.

The next work must proceed in this exact order:

1. Wait for the user to provide the Product app or relevant Product files from
   `sbm-api`.
2. Read the supplied source before modifying `dp-api`.
3. Identify the exact SKU generation behavior, including:
   - source fields and normalization;
   - prefix, separators, padding, and sequence rules;
   - database lookup or counter behavior;
   - uniqueness and collision handling;
   - behavior during create versus update;
   - transaction and concurrency assumptions.
4. Compare that behavior with the current `dp-api` Product entity, create use
   case, repository port, Django persistence adapter, serializer, and database
   constraints.
5. Present the proposed implementation and affected files before applying the
   change if the supplied logic exposes an ambiguity or contract decision.
6. Implement SKU generation in the correct hexagonal layer. HTTP controllers
   must only receive the request, use cases must coordinate the operation, and
   Django ORM/database access must remain in the infrastructure adapter.
7. Preserve the current Product API behavior unless the verified legacy SKU
   contract explicitly requires an agreed request change.
8. Add focused coverage for the generation rule, uniqueness/collisions, and
   any relevant sequence boundaries.
9. Run Product-specific tests and `python manage.py check` without creating or
   executing Django migrations.

### 21.2 Success criteria for the current vertical slice

The Product SKU correction is complete only when:

1. The existing `sbm-api` generation behavior has been inspected and
   documented from source, not guessed.
2. `dp-api` generates the expected SKU through the Product create use case.
3. The rule is isolated from the REST controller and Django model callbacks.
4. SKU uniqueness and collision behavior are explicit and tested.
5. Existing Product confirmation, audit log, PATCH, HEAD, and logical-delete
   behavior remains unchanged.
6. Product regression tests and Django system checks pass.
7. No Django migration or database alteration is introduced unless separately
   reviewed and authorized.

The `sbm-manager` Product consumer migration and eventual deprecation of the
duplicate Product endpoint in `sbm-api` remain subsequent work; neither is
implicitly completed by the SKU correction.

### 21.3 Codex and Cursor workflow

Cursor remains the primary editor and visual review environment. Codex may be used through the Cursor extension or CLI for repository-wide audits and coordinated multi-file changes.

Codex must read the `sbm-manager` project context and repository instructions before working there. Its initial task in that repository should be an audit without modifications covering Product-related:

```text
API clients
services
stores/composables
views/components
routes
environment configuration
```

It must search the full `sbm-manager` repository for:

```text
products
product
sbm-api
baseURL
group
item_group
group_name
item_group_name
price_description
price_gross_amount
PUT
DELETE
```

It must distinguish shared/internal `sbm-api` consumers from Ditaly Pasta Product consumers. It must not apply frontend changes until the audit identifies the exact Product integration points and the user authorizes the migration edit.

### 21.4 Local IDE environment

A local virtual environment was created at:

```text
DP-API/.venv
```

It is used only for Cursor/Pylance import resolution and autocomplete. Docker remains the official runtime.

Dependencies are installed from:

```text
core/requirements.txt
```

Recommended Cursor interpreter:

```text
${workspaceFolder}/.venv/bin/python
```

### 21.5 Interaction rule

When the user responds only with:

```text
ok
```

it means the previous validation produced exactly the expected result. Continue directly to the next step without requesting the output again.

## 22. Executive summary

`dp-api` is the client-facing domain API for Ditaly Pasta inside SBM Suite. It runs with Django REST Framework and PostgreSQL, uses the `ditaly_pasta,sbm_business,public` search path, exposes resource ViewSets for products, providers, pricing, branches, tickets, authorization, users, and supporting business data, and was validated locally through its Jazzmin admin at `localhost:8081`.

The central architectural rule is:

```text
Client operation → dp-api
Platform operation → sbm-api
```

A client user may create products, modify prices, manage providers, branches, catalogs, and tickets. A client user may not create `sbm_business.franchise`, activate uncontracted modules, or provision platform resources.

The current migration corrects Ditaly Pasta functionality that was implemented
inside `sbm-api` due to time constraints. The first backend capability,
Product, now has a validated canonical contract in `dp-api`. The immediate next
task is to inspect the Product app that the user will provide from `sbm-api` and
correct Product SKU generation in the hexagonal `dp-api` implementation. The
Vue.js 3 `sbm-manager` Product consumer migration remains pending, while
internal and critical platform operations continue using `sbm-api`.

The migration will be vertical and incremental. The first capability is `Product`:

```text
model
→ database mapping
→ serializer
→ ViewSet
→ endpoint
→ permissions
→ frontend
→ tests
→ AI Tool
```

The Product backend mapping, serializers, permitted HTTP operations, logical deletion, and audit-log behavior are established in `dp-api`. The duplicate Product endpoint in `sbm-api` must remain available until `sbm-manager` has migrated, frontend regression tests pass, and all remaining consumers are confirmed.

The long-term target is a production-grade, configurable ERP API where client users can operate independently and AI assists them through audited, permission-aware REST Tools without bypassing domain rules.
