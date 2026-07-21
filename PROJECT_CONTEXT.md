# PROJECT_CONTEXT.md

> **Last updated:** 2026-07-21
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

### 3.6.1 Independent PostgreSQL and Flyway runtime

The database is not owned or provisioned by the `dp-api` container.
PostgreSQL and Flyway run as an independent database/container stack shared
through the Docker network.

The ownership boundary is:

```text
dp-api container
→ Django/DRF application and unmanaged ORM mappings

independent PostgreSQL + Flyway container stack
→ schemas, tables, columns, constraints, indexes, triggers, functions, and
  versioned database migrations
```

Consequences for all future work:

- Django models in `dp-api` remain `managed = False` for Flyway-owned tables.
- A Django model change is only an ORM mapping change; it does not imply a
  database migration.
- Do not run `python manage.py makemigrations` or
  `python manage.py migrate` for these domain tables.
- Do not create Django migration files to represent PostgreSQL changes.
- If a structural database change is genuinely required, it must be planned
  and implemented separately in the database/Flyway project and executed by
  its independent container workflow.
- DP-API work must not mutate the PostgreSQL structure merely because a Django
  mapping or API contract changes.
- Read-only schema inspection is allowed for validation, but schema/data
  mutations require separate scope and explicit authorization.

Therefore, the planned Product price-generation work is an application/API
change unless analysis proves that a database invariant requires a separate
Flyway change. No Django migration is part of that implementation.

---


### 3.7 Latest validated implementation progress — 2026-07-19

The `Product` vertical migration is implemented and accepted as the canonical
reference capability in `dp-api`. Its backend contract and `sbm-manager`
consumer have been validated together. Product is resolved; removal of any
remaining duplicate `sbm-api` endpoint is a separate retirement task and does
not reopen the Product implementation.

The migration boundary remains:

```text
Ditaly Pasta client operation
→ sbm-manager
→ dp-api

Internal or critical platform operation
→ sbm-api
```

Product SKU generation was corrected in `dp-api` after inspecting the supplied
`sbm-api/catalog` app and the live PostgreSQL trigger. Product remains a client
operation owned by `dp-api`, and `sbm-manager` now consumes its canonical
`dp-api` contract.

#### `products/models.py`

- `Product.group` was renamed to `Product.item_group`.
- The mapped database column remains `item_group`.
- `Product.price` was changed from a scalar field to a foreign key targeting `pricing.Price.code`.
- Main domain relationships were changed to protective deletion behavior where appropriate.
- The model remains unmanaged because Flyway owns the schema.
- The legacy PostgreSQL column `gross_price` remains database-only. Existing
  rows contain `0`; the commercial value exposed by the API is
  `Price.gross_amount` through `gross_amount`.

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
base_net_amount
net_amount
gross_amount
iva_amount
aditional_tax_amount
retention_amount
item_group
item_group_name
price_configuration
price_configuration_label
provider_name
type_name
category_name
package_description
```

Stale Product response fields such as `group`, `group_name`, and `price_description` are no longer exposed.

`price_configuration` is the configuration UUID. Product responses also expose
`price_configuration_label`, resolved from
`ditaly_pasta.price_configuration.price_configuration`, so API consumers can
display its business name without replacing the UUID contract.

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

Product creation starts with `version=1`. Every PATCH that produces an actual
Product change increments `version` exactly once, including price or
`price_configuration` versioning. Idempotent PATCH requests that resend the
same persisted values do not increment it. PostgreSQL updates the counter
atomically to prevent concurrent PATCH requests from losing an increment.

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
- Product SKU is server/database generated and read-only in the public command
  contract. The live `ditaly_pasta.product_before_insert` trigger generates
  `P-<provider-number>-<four-digit-sequence>`, for example `P-001-0009`.
- The provider number comes from the suffix of `provider.code` (`PVP-001` →
  `001`), not directly from an arbitrary frontend SKU value.
- Product provider is immutable after creation. A PATCH that attempts to
  change it returns HTTP 400; repeating the same provider remains accepted to
  tolerate forms that resend unchanged fields.
- Product creation generates and links a complete Price using a confirmed
  `record_type=PRODUCT` price configuration.
- Changing `base_net_amount` or `price_configuration` creates and links a new
  Price version. Exclusively owned previous Prices become non-current; shared
  legacy Prices remain untouched for their other consumers.
- Product responses expose both the configuration UUID in
  `price_configuration` and its business label in
  `price_configuration_label`.
- Product creation starts with `version=1`; every effective PATCH increments
  it atomically once, while idempotent PATCH requests do not increment it.
- The Product price-configuration selector is constrained to confirmed
  `record_type=PRODUCT` configurations.
- Product HEAD list and detail: HTTP 200.
- Product PUT and HTTP DELETE: HTTP 405.
- No Django migration was created.
- PostgreSQL structure was not altered.
- Full automated suite after the final Product changes: 42 passing.
- The Product flow was accepted through `sbm-manager` on 2026-07-19.

Audit identity is not hardcoded. At present `created_by`, `updated_by`, and
`deleted_by` are validated against `users.User.code` but are supplied by the
client request. This is a known spoofing risk caused by the unresolved mapping
between Django authentication users and business users. It belongs to the
later authentication/security phase and does not reopen the resolved Product
vertical migration.

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
├── db.sqlite3
├── scripts/
│   ├── coverage.sh
│   ├── sonar-scan.sh
│   └── qa-check.sh
├── sonar-project.properties
├── coverage.xml
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

Product is the completed reference capability. Material is the active vertical
migration objective inside this app.

#### 5.4.1 Material preflight — 2026-07-19

Material must adopt the same validated structure and behavior as Product where
the domains share a rule: hexagonal boundaries, server-controlled Price
creation/versioning, audit handling, confirmation, logical deletion, atomic
`version` increments, restricted HTTP methods, response labels, and focused
contract/use-case tests. It must not copy Product field assumptions without
checking the live Material schema and data.

Read-only PostgreSQL inspection established:

```text
ditaly_pasta.material.item_group     → integer FK to item_group.id
current Django Material.group        → stale mapping to column "group"
ditaly_pasta.material.price          → char(36), NOT NULL
physical FK material.price → price   → absent
legacy gross_price                   → integer, existing rows contain 0
Material record type                 → id 2 / MATERIAL
confirmed configuration              → MATERIAL_NORMAL_IVA
```

The live `material_before_insert()` function generates `code` when missing and
generates SKU as `M-<provider-number>-<four-digit-sequence>`. PostgreSQL
currently registers two BEFORE INSERT triggers pointing to that same function;
the function is effectively idempotent after the first trigger fills the
values, but the duplicate trigger definition belongs to a separate
Flyway/database review and must not be changed from `dp-api`.

There are currently three Material rows. All three store Price UUIDs for which
no row exists in `ditaly_pasta.price`, and no current Price has
`price_record_type=2` or a Material `record_item_code`. This is legacy dangling
data, not authorization for automatic cleanup. Before changing the Material
model to a Price foreign key or using `select_related`, the implementation must
choose and test an explicit compatibility strategy so existing Materials do
not silently disappear from list/detail endpoints.

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
/api/price-configuration/
/api/prices/
/api/fiscal-configuration-details/
```

`/api/price-configuration/` exposes standard CRUD for the Flyway-owned
`ditaly_pasta.price_configuration` table. Its Django model is unmanaged,
`code` remains generated by the PostgreSQL insert trigger, and the foreign
keys to franchise configuration, variable formula, record type, and business
users are represented and validated by the ORM.

The client may modify prices and permitted commercial configurations. Global fiscal or platform policy ownership must be reviewed table by table.

#### Product price generation/versioning analysis — 2026-07-17

This subsection preserves historical analysis. It is superseded by the final
accepted Product contract documented in section 3.7: `base_net_amount` and a
valid PRODUCT `price_configuration` are writable commands; derived Price
amounts are read-only responses; changing either writable value versions the
Price. References below to a future gross-only contract are not active work.

Planning sources reviewed:

- Complete `SBM-API.zip`, especially `catalog`, `price`, `calculation`, and
  `fiscal`.
- `SBM-business.dbml` definitions for `ditaly_pasta.product`,
  `ditaly_pasta.price`, `ditaly_pasta.price_configuration`, calculation
  concepts, and fiscal directives.
- Current `dp-api` Product and pricing code.
- Read-only inspection of the live PostgreSQL configuration and price rows.

No implementation code or database structure was changed during this analysis.

The authoritative price table is `ditaly_pasta.price`. A Product stores the
current price code in `product.price → price.code`. Relevant Price fields are:

```text
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

The live Product configuration is:

```text
price_configuration = PRODUCT_NORMAL_IVA
price_configuration.code = cd746343-baf4-4359-b2e6-9bd829631e30
record_type = 1 (PRODUCT)
is_confirmed = true
IVA variable = 0.190
```

The configured Product formula represents:

```text
net/base amount = base_net_amount
IVA amount      = base_net_amount * iva
gross amount    = base_net_amount * (1 + iva)
```

Example validated from current data:

```text
base_net_amount = 16,980
iva_amount      = 3,226
gross_amount    = 20,206
```

##### Behavior found in `sbm-api`

The old Product implementation does not update the existing Price row when
the amount changes. Its intended behavior is versioning:

1. Product create receives a base-net amount and price configuration.
2. It creates a Price row before creating the Product.
3. Product PATCH accepts `price_data` with `base_net_amount` and
   `price_configuration`.
4. When either changes, it marks the old price `is_current=false`.
5. It creates a new Price with `record_item_code=product.code`,
   `price_record_type=1`, and `is_current=true`.
6. It links `product.price` to the new Price code.

That implementation is only a behavioral reference and must not be copied
literally. It duplicates formula evaluation across serializers/views, uses
`eval()`, and some Product paths access `variable_formula.price_variables`, a
property that does not exist on the supplied `VariableFormula` model. Other
paths inconsistently use `formula_template` or `formula_translate`. The direct
`PriceViewSet` also permits broad CRUD and is not the safe contract for a
client changing a Product price.

##### Historical requested target behavior — superseded

At the time of the analysis, a gross-only Product input was proposed. That
proposal was not the final accepted contract. The historical proposal stated
that the client would not submit or control:

```text
price code
base_net_amount
net_amount
iva_amount
aditional_tax_amount
retention_amount
price_configuration
record_item_code
price_record_type
is_current
```

The proposed Product request field is the already exposed
`price_gross_amount`. The intended contracts to validate in the next chat are:

```json
// Product creation fragment
{
  "price_gross_amount": 20206
}
```

```json
// Product price change fragment
{
  "price_gross_amount": 25000,
  "updated_by": "<business-user-code>"
}
```

The existing `price` UUID should become read-only in Product commands once
server-side price creation is active. It remains present in responses as the
identifier of the generated current Price.

For the currently supported `PRODUCT_NORMAL_IVA` rule, gross is authoritative.
The backend should use `Decimal`, never binary float or unrestricted `eval()`,
and derive values so the stored identity is exact:

```text
base_net_amount = monetary_round(gross_amount / (1 + iva))
net_amount      = base_net_amount
iva_amount      = gross_amount - net_amount
gross_amount    = exact client-supplied integer
additional tax  = 0 unless the selected configuration defines it
retention       = 0 unless the selected configuration defines it
```

The rounding policy must be explicit and tested. The initial recommended rule
for integer CLP values is `Decimal` with `ROUND_HALF_UP`. A future configuration
with additional taxes or retention requires an explicit inverse-calculation
strategy; it must not silently reuse the simple IVA-only inverse formula.

##### Required versioning and transaction rules

Price changes must execute atomically:

```text
lock Product/current Price
→ validate current Product price ownership
→ resolve confirmed PRODUCT price configuration
→ resolve applicable fiscal variables
→ calculate derived values
→ create new Price version
→ mark owned previous version not current
→ relink Product.price
→ update Product audit fields/log
→ commit
```

If the submitted gross amount equals the current gross amount, the operation
should be idempotent and must not create another Price row.

The database currently has no partial unique constraint guaranteeing one
`is_current=true` Price per `record_item_code`; this invariant must be enforced
by the application transaction and covered by tests. Flyway remains the owner
of any future database constraint.

Current test data contains an important legacy inconsistency: Price
`bf397d95-c18c-4620-88c9-af621f553951` is linked by six Products. The old
algorithm assumes one Price owner per Product and would incorrectly affect all
consumers if copied directly. Product price versioning now audits ownership
using `price.record_item_code`, `price_record_type`, and Product references.
When the previous Price is shared or inconsistently owned, it creates and links
a new Product-owned Price without marking the shared row non-current. An
exclusively owned valid Product Price is still deactivated normally. No data
cleanup is performed by this compatibility behavior.

##### Historical architectural scope — resolved

This Product-price slice has been implemented and resolved. The boundaries are
retained below as historical rationale and regression constraints, not as the
current objective.

Recommended boundaries:

- Product presentation accepts only `price_gross_amount` as the client-editable
  monetary value.
- An application use case coordinates Product and Price creation/versioning.
- A pricing domain policy performs deterministic gross-to-components
  calculation without Django or DRF.
- Repository ports expose current-price lookup, configuration/fiscal-variable
  lookup, Price creation, current-version transition, and Product relinking.
- Django ORM and `transaction.atomic()` remain infrastructure concerns.
- PostgreSQL and Flyway remain the source of truth.
- Do not introduce SQLAlchemy, a dependency-injection framework, or an
  external formula/hexagonal library.

Expected implementation files must be confirmed after re-reading the current
repository, but likely include Product command/serializer/view/use-case files
and a small hexagonal pricing slice under `pricing/domain`,
`pricing/application`, and `pricing/infrastructure`.

Required coverage:

- Product create with only gross price creates and links one correct Price.
- Gross-to-net/IVA calculation for 19% IVA and rounding boundaries.
- Product price PATCH creates a new version and preserves history.
- Same gross amount is idempotent.
- Invalid, zero, negative, non-integer, or missing gross values follow an
  explicitly agreed validation rule.
- Direct client attempts to set Price internals are ignored or rejected.
- Shared legacy Price detection does not corrupt another Product.
- Transaction rollback leaves old Price and Product link unchanged on error.
- Product audit log records the gross-price change and ends in `;`.
- Existing SKU, immutable-provider, confirmation, soft-delete, HEAD, and
  disabled PUT/DELETE behavior remains unchanged.

Historical open decisions (resolved by the accepted Product contract):

1. Confirm `price_gross_amount` as the writable request field name.
2. Confirm whether gross price is mandatory on Product create or whether the
   existing `price` UUID remains temporarily supported for compatibility.
3. Confirm the validation rule for gross price `0` and minimum allowed value.
4. Confirm `ROUND_HALF_UP` for conversion to integer CLP.
5. Decide how existing Products sharing one Price will be normalized or
   handled during their first price change.
6. Confirm whether a newly generated Price inherits Product confirmation state
   or remains under the current Price confirmation convention.

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

Product resolution state:

- Product creation without client-supplied SKU and Provider immutability were
  validated through the real integrated flow.
- `sbm-manager` consumes the canonical `dp-api` Product contract, including
  response labels, price-configuration filtering, and logical deletion.
- Regression coverage includes lifecycle, Price versioning, shared legacy
  Price protection, confirmation, audit, and atomic `version` increments.
- The PostgreSQL trigger's `MAX(sequence) + 1` concurrency strategy remains a
  production-hardening concern, not unfinished Product behavior.
- Authenticated business-user attribution remains a platform security task.
- The equivalent `sbm-api` endpoint may be deprecated after the remaining
  consumer audit; Product behavior itself is resolved.

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
dp-api Product backend contract → completed and validated
dp-api Product lifecycle/Price  → completed and validated
sbm-manager Product consumer    → migrated and accepted
sbm-api Product endpoint        → retirement pending consumer audit
```

Current Material migration state:

```text
live schema/data preflight       → completed
dp-api Material vertical slice  → implemented and backend-validated
sbm-manager Material consumer   → current next objective
legacy dangling Material prices → compatible read/explicit repair implemented
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

### 15.1 Current validated state

`dp-api` has a formal, module-local QA foundation for Product and retains the
existing Material, Pricing, and Provider regression tests.

Latest validated suite state:

```text
54 Product tests
71 passing tests in the complete suite
Product package coverage: 73.64% including branches
Product package line coverage: 78.44%
Product package branch coverage: 33.19%
```

The Product suite covers domain/use-case behavior, serializer and ViewSet
contracts, API routing through DRF `APIClient`, pagination, filters, creation,
PATCH, Price versioning, immutable Provider behavior, disabled PUT/DELETE,
HEAD, logical deletion, audit handling, and previously fixed regressions.

`coverage.xml` is generated reproducibly at the repository root. SonarQube
Community Build is now configured locally, imports the report successfully, and
analyzes the Product scope through the repository QA scripts.

Existing testing-related dependencies confirmed in the project context include:

- `pytest`;
- `pytest-django`;
- `pytest-cov`;
- `coverage`.

The unused legacy `coreapi` dependency was removed. This also removed its
`pkg_resources` deprecation warning from pytest execution.

The transversal SBM Suite QA standard recommends:

- `pytest` as the primary runner;
- `pytest-django` for Django integration;
- `pytest-cov` for coverage;
- Factory Boy and Faker for reusable test data;
- `unittest.mock` for isolated mocks;
- deterministic, isolated tests;
- explicit success and failure cases;
- module-level regression protection;
- coverage reports prepared for later SonarQube analysis.

### 15.2 Immediate QA objective

The first standardized QA structure for the `products` Django app is complete,
using Product as the reference capability.

All Product tests must live under:

```text
products/tests/
```

The repository must not introduce a root-level `tests/` hierarchy for this
initial phase.

Final implemented structure:

```text
products/
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   ├── factories.py
│   ├── test_models.py
│   ├── test_price_policy.py
│   ├── test_serializers.py
│   ├── test_use_cases.py
│   ├── test_views.py
│   ├── test_api.py
│   └── test_regression.py
```

`test_price_policy.py` preserves the existing safe Decimal formula-engine tests
that previously lived in `pricing/test_product_price_policy.py`. No root-level
`tests/` directory was introduced.

### 15.3 Scope of this QA slice

This completed QA slice was restricted to Product.

Completed work:

1. Audited and preserved all 36 existing Product-related tests.
2. Reorganized them under `products/tests/` by responsibility.
3. Added 18 focused tests, bringing Product to 54 tests.
4. Configured `pytest.ini`, `pytest-cov`, `.coveragerc`, reusable fixtures, and
   deterministic builders.
5. Mounted pytest and coverage configuration into the Docker runtime.
6. Generated terminal and Cobertura XML reports.
7. Preserved all Product behavior and avoided unrelated implementation changes.

Restrictions respected:

- rewrite the Product implementation;
- reopen accepted Product architecture decisions;
- modify the public Product contract;
- run or create Django migrations;
- modify PostgreSQL, DBML, Flyway, triggers, constraints, or seed data;
- introduce Testcontainers yet;
- configure SonarQube yet;
- configure CI/CD pipelines yet;
- migrate tests for every Django app;
- modify `sbm-manager`;
- remove the duplicate Product endpoint from `sbm-api`;
- perform Git operations unless separately authorized.

### 15.4 Product behaviors that must remain protected

The Product suite must continue validating the accepted behavior documented in
this context, including at minimum:

#### Read contract

- Product list returns HTTP 200.
- Product detail returns HTTP 200 for visible products.
- Standard pagination remains available.
- Response fields use the accepted canonical names.
- `item_group` replaces stale `group`.
- relationship labels remain exposed.
- internal `log` remains hidden.
- logically deleted Products remain excluded from normal queries.

#### Create contract

- Product creation returns HTTP 201.
- SKU is generated by PostgreSQL and is read-only to clients.
- Provider is required according to the active contract.
- a complete current Price is created and linked.
- only confirmed Product price configurations are accepted.
- Product starts with `version=1`.
- confirmation audit is server-controlled.
- client attempts to control confirmation audit fields fail safely.
- Product audit log starts with the accepted `INIT` format and ends in `;`.

#### Update contract

- PATCH returns HTTP 200 for valid partial updates.
- PUT returns HTTP 405.
- HTTP DELETE returns HTTP 405.
- Provider is immutable after creation.
- resending the same Provider remains tolerated.
- effective Product changes increment `version` exactly once.
- idempotent PATCH requests do not increment `version`.
- confirmation and unconfirmation update audit fields correctly.
- `base_net_amount` or `price_configuration` changes create and link a new
  Price version.
- idempotent pricing PATCH does not create another Price.
- an exclusively owned prior Price becomes non-current.
- shared or inconsistently owned legacy Prices are not corrupted.
- transaction failure leaves the Product and previous Price state unchanged.

#### Logical deletion contract

Method:

```text
POST
```

Path:

```text
/api/products/{id}/delete/
```

Expected behavior:

- Product remains physically stored;
- `is_active=False`;
- `is_deleted=True`;
- deletion audit fields are populated;
- deletion log uses the accepted format and ends in `;`;
- Product disappears from normal list and detail access.

#### Technical contract

- `python manage.py check` continues passing.
- all existing Product regression tests continue passing.
- no Django migration is generated.
- no PostgreSQL structure or data is mutated outside normal rolled-back test
  transactions.
- tests are deterministic and repeatable.
- tests do not depend on manually prepared production-like records.
- secrets and real credentials are never embedded in tests.

### 15.5 Recommended test responsibilities

#### `products/tests/conftest.py`

Use for Product-specific reusable pytest fixtures only.

It may provide:

- API client;
- authenticated Django user where required;
- business user records;
- Provider;
- ItemGroup;
- ItemType;
- ItemCategory;
- Package;
- Product price configuration;
- current Price;
- Product;
- helpers for accepted request payloads.

Do not create a global root `conftest.py` in this phase unless repository
inspection proves it is already present and shared safely.

#### `products/tests/factories.py`

Use for reusable Factory Boy factories if Factory Boy is introduced.

Factories must:

- create only the minimum required records;
- respect unmanaged model mappings;
- avoid triggering unauthorized schema changes;
- keep generated values deterministic where behavior depends on exact fields;
- distinguish Django authentication users from business users.

If introducing Factory Boy would expand scope or dependency management
unnecessarily, fixtures may be used first and Factory Boy left as a documented
next improvement.

#### `products/tests/test_models.py`

Cover mapping and low-level Product invariants that can be tested without
duplicating database-owned trigger behavior.

Examples:

- mapped field names;
- relationship behavior;
- unmanaged model status where relevant;
- canonical field access;
- logical visibility helpers if implemented at model or manager level.

Do not attempt to unit-test PostgreSQL trigger internals as pure Python logic.

#### `products/tests/test_serializers.py`

Cover request and response contract validation.

Examples:

- accepted writable fields;
- read-only fields;
- rejected confirmation audit fields;
- canonical `item_group` naming;
- price configuration validation;
- invalid relationship identifiers;
- response labels;
- concealed internal log field.

#### `products/tests/test_use_cases.py`

Cover application and domain behavior independently where the current
hexagonal implementation exposes use cases or policies.

Examples:

- Product creation orchestration;
- Product PATCH behavior;
- Provider immutability;
- Product version increments;
- Price versioning;
- idempotency;
- shared legacy Price protection;
- confirmation transitions;
- rollback behavior.

Mocks must be used only where they improve isolation. Integration-sensitive
behavior must still be covered with real Django ORM tests.

#### `products/tests/test_views.py`

Cover DRF ViewSet/controller concerns.

Examples:

- permitted methods;
- disabled PUT and physical DELETE;
- filters;
- queryset visibility;
- logical-delete action;
- HTTP status mapping;
- validation error responses.

#### `products/tests/test_api.py`

Cover Product API flows through DRF's API client.

Examples:

- list;
- retrieve;
- create;
- ordinary PATCH;
- price PATCH;
- confirmation;
- unconfirmation;
- logical deletion;
- HEAD;
- invalid foreign keys;
- invalid price configuration;
- protected read-only fields.

#### `products/tests/test_regression.py`

Protect previously fixed defects and integration-sensitive Product behavior.

Examples:

- stale `group` names do not reappear;
- stale Price fields are not queried;
- shared Price rows are not deactivated incorrectly;
- SKU remains server/database generated;
- Product response labels remain stable;
- Product audit formatting remains stable;
- atomic `version` increments remain stable.

### 15.6 Test naming convention

Use:

```text
test_<behavior>_<condition>_<expected_result>
```

Examples:

```text
test_create_product_with_valid_data_returns_201
test_create_product_with_client_supplied_sku_ignores_or_rejects_value
test_patch_product_with_changed_provider_returns_400
test_patch_product_with_same_provider_returns_200
test_patch_product_with_same_values_does_not_increment_version
test_patch_product_price_creates_new_price_version
test_delete_product_logically_hides_product_from_list
test_put_product_returns_405
test_http_delete_product_returns_405
```

Test names must describe observable behavior, not implementation details.

### 15.7 QA execution and coverage

Docker remains the official runtime. The current operational QA interface is
provided by scripts under `scripts/`:

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

Generate a current Product test and coverage report:

```bash
./scripts/coverage.sh
```

The coverage script executes the Product pytest suite inside the existing
Compose `api` service, generates Cobertura XML inside `dp-core`, and copies the
artifact to:

```text
DP-API/coverage.xml
```

Coverage purpose:

```text
pytest executes tests
→ pytest-cov records executed lines and branches
→ coverage.xml stores the machine-readable result
→ SonarScanner imports coverage.xml
→ SonarQube displays coverage and applies the Quality Gate
```

SonarScanner does not run pytest. `coverage.xml` must therefore be regenerated
before analysis whenever application code or tests change.

Direct validated test commands remain available:

```bash
docker compose --env-file .env.dev run --rm --no-deps   --entrypoint pytest api products/tests/

docker compose --env-file .env.dev run --rm --no-deps   --entrypoint pytest api

docker compose --env-file .env.dev run --rm --no-deps   --entrypoint python api manage.py check
```

Validated pytest results on 2026-07-21:

```text
Product tests                    54 passed
Complete suite                   71 passed
Django system check              0 issues
Coverage including branches      73.64%
Line coverage                    78.44%
Branch coverage                  33.19%
Coverage artifact                coverage.xml
```

Only test files are omitted by `.coveragerc`. Application modules are not
hidden. The lowest Product-specific result remains the Django ORM repository
adapter at 27.85%. The preferred 80% package target remains a future
improvement; the initial 70% pytest-cov target is satisfied.

### 15.8 SonarQube integration

SonarQube Community Build is running locally in an independent Docker Compose
stack with its own PostgreSQL database. It does not use or modify the DP-API
business database.

The local project is configured as:

```text
Display name: DP-API
Project key:  DP-API
Branch:       main
```

Authentication uses a project analysis token loaded from the local environment:

```text
SONAR_HOST_URL=http://host.docker.internal:9000
SONAR_TOKEN=<project-analysis-token>
```

The token and environment files must never be committed. The token grants
analysis access to the current SonarQube project; it is not a Django or
PostgreSQL credential.

Repository scanner configuration is stored in:

```text
sonar-project.properties
```

Current effective scope:

```text
sonar.sources=products
sonar.tests=products/tests
sonar.python.version=3.11
sonar.python.coverage.reportPaths=coverage.xml
```

The scanner runs in a disposable container and mounts the repository at
`/usr/src/app` because the generated Cobertura report references the same
container path. Its persistent plugin cache is stored under `.sonar/cache`, and
`.sonar/` must remain ignored by Git.

Run only SonarScanner:

```bash
./scripts/sonar-scan.sh
```

Run the complete QA sequence:

```bash
./scripts/qa-check.sh
```

The combined script executes:

```text
coverage.sh
→ tests pass and coverage.xml is refreshed
→ sonar-scan.sh
→ analysis uploaded to SonarQube
```

`set -e` stops the flow if pytest, coverage generation, copying the report, or
SonarScanner fails.

Latest validated SonarQube state on 2026-07-21:

```text
Analyzed scope                   products
Indexed files                   52
SonarQube coverage              67.9%
Reliability rating              B
Reliability issues              2
Maintainability rating          A
Maintainability issues          21
Security rating                 A
Security issues                 0
Security hotspots               0
Duplicated lines                12.2%
Quality Gate                    Passed
```

The SonarQube coverage percentage is not expected to equal the pytest-cov total
exactly. Pytest-cov reports line and branch percentages for the Python package;
SonarQube calculates coverage from executable lines and conditions using its own
combined metric.

The current Quality Gate passes, so SonarQube would not block a merge while the
pipeline is configured to honor this gate. Passing does not mean automatic
production deployment; CI/CD, approvals and deployment rules remain separate.

Remaining non-blocking scanner warnings:

- ARM64 Mac executes the available scanner image through AMD64 emulation;
- uncommitted or newly created test files may lack SCM blame information;
- Community Build has limited advanced security analysis.

Immediate quality work should prioritize the two Reliability issues, then the
12.2% duplication, followed by the maintainability findings and the preferred
80% coverage target.

### 15.9 Definition of done for this QA slice

The Product QA reorganization completed with the following verified state:

1. Product tests are under `products/tests/`.
2. Existing coverage was preserved and expanded.
3. Product behavior and public contracts were unchanged.
4. Product and complete suites pass.
5. `python manage.py check` passes.
6. Coverage and `coverage.xml` are reproducible.
7. No migration, database schema change, or persistent-data mutation occurred.
8. The repository is ready for a separately authorized SonarQube phase.

### 15.10 Codex execution rules for this task

Before modifying files, Codex must:

1. read this complete `PROJECT_CONTEXT.md`;
2. inspect repository instructions and `git status`;
3. preserve every existing user change;
4. inventory current Product tests and pytest configuration;
5. identify whether tests currently live in `products/tests.py`,
   `products/tests/`, or another location;
6. identify the exact Docker command used to execute tests;
7. identify existing coverage configuration;
8. report the proposed file moves and additions before implementing them.

During implementation, Codex must:

- change only files required for Product QA standardization;
- preserve the accepted Product implementation;
- avoid speculative refactors;
- keep tests focused and deterministic;
- prefer reusable fixtures over copied setup;
- avoid excessive mocking;
- never expose secrets;
- never run migrations;
- never mutate PostgreSQL structure;
- never perform Git operations without authorization;
- validate one step at a time.

After implementation, Codex must report:

- files created;
- files moved;
- files modified;
- exact test command executed;
- focused Product result;
- complete suite result;
- Django system-check result;
- coverage result;
- generated artifacts;
- any remaining gap before SonarQube.

### 15.11 Product QA implementation record — 2026-07-21

Created:

- `pytest.ini`;
- `.coveragerc`;
- `products/tests/__init__.py`;
- `products/tests/conftest.py`;
- `products/tests/factories.py`;
- `products/tests/test_models.py`;
- `products/tests/test_price_policy.py`;
- `products/tests/test_serializers.py`;
- `products/tests/test_use_cases.py`;
- `products/tests/test_views.py`;
- `products/tests/test_api.py`;
- `products/tests/test_regression.py`.

Moved and reorganized without losing tests:

```text
products/test_product_hexagonal.py
pricing/test_product_price_patch.py
pricing/test_product_price_policy.py
→ products/tests/
```

The empty placeholder `products/tests.py` was removed because it conflicts with
the new package structure. `core/requirements.txt` gained `pytest-cov` and
removed unused `coreapi`; `docker-compose.yml` now mounts pytest and coverage
configuration read-only. `README.md` gained only the minimal operational test
commands required for developers.

Important decisions and limitations:

- Factory Boy and Faker were not added; deterministic builders and fixtures
  cover the current need without extra dependencies.
- API tests use DRF `APIClient` with in-memory ports. They validate routing,
  HTTP orchestration, serialization, and domain interaction without touching
  persistent data.
- Real ORM, PostgreSQL-trigger, and transaction integration tests remain a gap.
  Because Product and Price mappings are unmanaged, those tests require a
  dedicated database initialized by the real Flyway schema. The development
  database must not be used as a test substitute.
- Coverage omits only test files. No application module is hidden.
- No Product implementation, public contract, migration, Flyway artifact,
  PostgreSQL structure, or persistent row was changed.
- SonarQube is configured locally and imports Product coverage successfully.
- CI/CD integration remains intentionally unconfigured.

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
2. Complete the active Material vertical migration using resolved Product as
   the reference implementation.
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
- ✅ Correct Product SKU generation using the existing `sbm-api` Product app
  and live PostgreSQL trigger as behavioral references.
- ✅ Implement safe Product Price creation/versioning for amount and
  configuration changes.
- ✅ Implement Product response labels, confirmation audit, logical deletion,
  and atomic entity-version increments.
- ✅ Update and validate the `sbm-manager` Product consumer.
- ✅ Accept Product as resolved and use it as the reference vertical slice.
- ⏳ Retire the duplicate Product endpoint in `sbm-api` after the remaining
  consumer audit; this is cleanup, not unfinished Product behavior.

### Phase 3 — Remaining catalog domain

- ✅ Material backend: hexagonal CRUD, Price creation/versioning, labels,
  lifecycle, audit, entity versioning, and legacy compatibility implemented.
- 🚧 Material: migrate and validate the `sbm-manager` consumer against the
  stable backend contract.
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

### Phase 6 — QA foundation and code quality

- ✅ Standardize Product tests under `products/tests/`.
- ✅ Preserve and reorganize existing Product regression coverage.
- ✅ Configure reproducible Product-focused pytest execution.
- ✅ Generate `coverage.xml` with pytest coverage tooling.
- ✅ Establish the 73.64% Product-package coverage baseline.
- ✅ Document test commands and structure.
- ✅ Configure local SonarQube after Product QA validation.
- ✅ Validate the initial local Quality Gate (`Passed`).
- ⏳ Tighten Quality Gate thresholds and connect them to CI/CD merge blocking.
- ⏳ Extend the same pattern incrementally to Material and later modules.

### Phase 7 — Security and tenancy

- ⏳ Authentication architecture.
- ⏳ Resolve custom user versus Django user.
- ⏳ Tenant context.
- ⏳ Object-level permissions.
- ⏳ Contracted-module validation.
- ⏳ Audit logging.

### Phase 8 — Production hardening

- ⏳ Production settings.
- ⏳ Secure CORS.
- ⏳ Secret management.
- ⏳ Gunicorn or equivalent.
- ⏳ Healthchecks.
- ⏳ Structured logs.
- ⏳ CI/CD.
- ⏳ Automated test suite.
- ⏳ Production deployment.

### Phase 9 — AI integration

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

1. **Product (Implemented / Resolved)** — establishes the reference structure and contains
   lifecycle, relationship, audit-log, PATCH, and logical-deletion rules that
   should not live in HTTP controllers.
2. **Provider (Implemented)** — contains supplier identity, contact, banking,
   dispatch, classification, confirmation, and audit data while providing a
   stable selector contract to client applications.
3. **Material (Backend Implemented / Frontend Pending)** — combines units,
   packaging, suppliers, traceability, and future inventory or production
   constraints through a hexagonal backend; its `sbm-manager` consumer remains
   to be migrated and accepted.
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

`Product` remains the completed reference implementation. `Provider` and the
`dp-api` Material backend are implemented. The active Material scope is now
the `sbm-manager` consumer migration and integrated acceptance; the other
entries remain future candidates.

---

## 21. Immediate next step

### 21.1 Current exact objective

The Product QA foundation and local SonarQube integration are complete and
validated. The next QA objective is to review and resolve the current SonarQube
findings before introducing CI/CD enforcement.

Current priorities are:

1. inspect and resolve the 2 Reliability issues;
2. reduce duplicated lines from the current 12.2%;
3. review the 21 Maintainability issues;
4. raise coverage toward the preferred 80% target;
5. define stricter New Code Quality Gate conditions;
6. integrate the validated QA flow into CI/CD only after the local baseline is
   accepted.

The immediate technical debt within testing remains real ORM coverage for
unmanaged Product/Price tables. That requires a dedicated Flyway-initialized
test database and must not be approximated by using the persistent development
database.

### 21.2 Required structure

Implemented structure:

```text
products/
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   ├── factories.py
│   ├── test_models.py
│   ├── test_price_policy.py
│   ├── test_serializers.py
│   ├── test_use_cases.py
│   ├── test_views.py
│   ├── test_api.py
│   └── test_regression.py
```

No repository-level `tests/` directory was created.

### 21.3 Required validation sequence

Latest validated results:

```text
Product-focused pytest suite  → 54 passed
Complete dp-api pytest suite  → 71 passed
Django system check           → 0 issues
Coverage including branches   → 73.64%
Line coverage                 → 78.44%
Branch coverage               → 33.19%
XML coverage                  → coverage.xml at repository root
```

The initial 70% threshold is met. The preferred 80% package target remains
pending, principally because the unmanaged ORM repository lacks safe database
integration coverage and Material code is included in the `products` package.

### 21.4 SonarQube current state and next QA phase

Completed:

1. local SonarQube Community Build and PostgreSQL stack;
2. local `DP-API` project and project analysis token;
3. `sonar-project.properties` configuration;
4. Product-only source and test scope;
5. Python 3.11 analyzer configuration;
6. successful `coverage.xml` ingestion;
7. persistent local scanner cache;
8. `coverage.sh`, `sonar-scan.sh`, and `qa-check.sh` workflow;
9. initial analysis and passing Quality Gate.

The next separately authorized phase may:

1. inspect Reliability findings;
2. correct genuine bugs without changing accepted contracts;
3. reduce duplication;
4. evaluate an initial stricter Quality Gate for New Code;
5. connect the scripts to CI/CD and block merges when the Quality Gate fails.

### 21.5 Non-negotiable restrictions

- No Django migrations.
- No PostgreSQL structural changes.
- No DBML or Flyway changes.
- No Product contract redesign.
- No Material implementation work.
- No `sbm-manager` changes.
- No CI/CD pipeline implementation without separate authorization.
- No Git operations unless separately authorized.
- No secret exposure.
- No deletion of passing tests without an equivalent replacement.

### 21.6 Completed QA criteria

Completed state:

1. Product tests live under `products/tests/`.
2. Product-focused and complete suites pass.
3. Django system checks pass.
4. Coverage reports and `coverage.xml` are generated.
5. Coverage and gaps are documented.
6. No accepted Product behavior changed.
7. No migration or persistent database mutation occurred.
8. SonarQube imports Product coverage successfully.
9. The local Quality Gate passes.
10. CI/CD enforcement remains a separate authorized phase.

### 21.7 Codex and Cursor workflow

Cursor remains the editor and visual review environment. Codex may perform the
repository-wide audit and coordinated test reorganization.

Codex must begin with an audit and must not modify files until it has identified:

```text
existing Product tests
pytest configuration
coverage configuration
Docker test command
shared fixtures
Product use cases and adapters
current changed files
```

The user validates each major step before Codex proceeds.

### 21.8 Local IDE environment

A local virtual environment exists at:

```text
DP-API/.venv
```

It is used only for Cursor/Pylance import resolution and autocomplete. Docker
remains the official runtime.

Dependencies are installed from:

```text
core/requirements.txt
```

Recommended Cursor interpreter:

```text
${workspaceFolder}/.venv/bin/python
```

### 21.9 Interaction rule

When the user responds only with:

```text
ok
```

it means the previous validation produced exactly the expected result. Continue
directly to the next step without requesting the output again.


## 22. Executive summary

`dp-api` is the client-facing domain API for Ditaly Pasta inside SBM Suite. It runs with Django REST Framework and PostgreSQL, uses the `ditaly_pasta,sbm_business,public` search path, exposes resource ViewSets for products, providers, pricing, branches, tickets, authorization, users, and supporting business data, and was validated locally through its Jazzmin admin at `localhost:8081`.

The central architectural rule is:

```text
Client operation → dp-api
Platform operation → sbm-api
```

A client user may create products, modify prices, manage providers, branches, catalogs, and tickets. A client user may not create `sbm_business.franchise`, activate uncontracted modules, or provision platform resources.

The current migration corrects Ditaly Pasta functionality that was implemented
inside `sbm-api` due to time constraints. Product is now the completed and
accepted canonical reference in `dp-api`: its database-generated SKU,
hexagonal lifecycle, Price creation/versioning, response labels, confirmation,
logical deletion, audit, and entity-version behavior are integrated with
`sbm-manager`. The Material backend now applies that pattern through a
hexagonal CRUD and safe Price lifecycle. Its compatibility contract preserves
three legacy rows whose stored Price UUIDs do not exist and supports explicit
repair through a pricing PATCH. Migrating and accepting the `sbm-manager`
Material consumer is the active next step. Internal and critical platform
operations continue using `sbm-api`.

The migration remains vertical and incremental. Product supplies the accepted
capability template now being applied selectively to Material:

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

The Product implementation is resolved. Its duplicate endpoint in `sbm-api`
may be retired only after all remaining consumers are audited. That retirement
is separate from the active Material implementation and must not trigger a
Product rewrite.

The Product QA foundation and local SonarQube integration are now operational.
Product tests are standardized under `products/tests/`; `coverage.sh` regenerates
pytest and Cobertura results; `sonar-scan.sh` performs static analysis; and
`qa-check.sh` executes both stages in order. The latest local Quality Gate passes
with 67.9% SonarQube coverage, Reliability B with 2 issues, Maintainability A
with 21 issues, Security A with no detected issues, and 12.2% duplicated lines.
The next QA work is to resolve the Reliability findings, reduce duplication,
raise coverage and only then introduce CI/CD enforcement. Database changes and
unrelated module refactors remain outside this QA scope.

The long-term target is a production-grade, configurable ERP API where client users can operate independently and AI assists them through audited, permission-aware REST Tools without bypassing domain rules.
