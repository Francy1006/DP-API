# DP-API - Documentación Técnica Completa

## Índice
1. [Descripción General](#descripción-general)
2. [Arquitectura del Sistema](#arquitectura-del-sistema)
3. [Configuración del Proyecto](#configuración-del-proyecto)
4. [Base de Datos](#base-de-datos)
5. [Modelos de Datos](#modelos-de-datos)
6. [API Endpoints](#api-endpoints)
7. [Autenticación y Permisos](#autenticación-y-permisos)
8. [Configuración de Docker](#configuración-de-docker)
9. [Despliegue](#despliegue)
10. [Guías de Desarrollo](#guías-de-desarrollo)

---

## 1. Descripción General

**DP-API** es una API REST desarrollada en Django que proporciona servicios para la gestión de catálogos, productos, proveedores y usuarios. La API está diseñada para ser consumida por aplicaciones frontend y otros servicios.

### Características Principales
- ✅ API REST completa con Django REST Framework
- ✅ Autenticación por token y sesión
- ✅ Gestión de catálogos y productos
- ✅ Sistema de proveedores
- ✅ Gestión de usuarios y roles
- ✅ Base de datos PostgreSQL con múltiples esquemas
- ✅ Documentación automática con Django Jazzmin
- ✅ Configuración Docker completa

---

## 2. Arquitectura del Sistema

### Estructura del Proyecto
```
DP-API/
├── core/                    # Proyecto principal Django
│   ├── settings.py         # Configuración principal
│   ├── urls.py             # URLs principales
│   ├── views.py            # Vistas del proyecto
│   ├── wsgi.py             # Configuración WSGI
│   └── asgi.py             # Configuración ASGI
├── store/                   # App principal de negocio
│   ├── models.py           # Modelos de datos
│   ├── views.py            # ViewSets y vistas
│   ├── serializers.py      # Serializers DRF
│   ├── urls.py             # URLs de la app
│   └── admin.py            # Configuración admin
├── templates/               # Templates HTML
├── docker-compose.yml       # Configuración Docker
├── Dockerfile              # Imagen Docker
├── requirements.txt         # Dependencias Python
└── .api-env                # Variables de entorno
```

### Tecnologías Utilizadas
- **Backend**: Django 4.2.16, Django REST Framework
- **Base de Datos**: PostgreSQL 13+
- **Autenticación**: Django REST Framework Token Auth
- **Admin**: Django Jazzmin
- **Contenedores**: Docker & Docker Compose
- **Filtros**: Django Filter
- **CORS**: django-cors-headers

---

## 3. Configuración del Proyecto

### Variables de Entorno (.api-env)
```bash
# Django settings
DEBUG=0
SECRET_KEY=MysecretKey
ALLOWED_HOSTS=localhost,127.0.0.1
CORS_ALLOWED_ORIGINS=http://localhost:8080,http://127.0.0.1:9000
STATIC_URL=static/

# Internationalization
LANGUAGE_CODE=es-ar
TIME_ZONE=America/Santiago
USE_I18N=1
USE_TZ=1

# PostgreSQL connection
DB_NAME=sbm_db
DB_USER=sbm_admin
DB_PASSWORD=FrancY1
DB_HOST=postgres
DB_PORT=5432

# Media files
MEDIA_URL=/media/
MEDIA_ROOT=os.path.join(BASE_DIR, "media")

# Django Superuser Credentials
DJANGO_SUPERUSER_USERNAME=sbm-admin
DJANGO_SUPERUSER_EMAIL=operacione@ditalypasta.cl
DJANGO_SUPERUSER_PASSWORD=sbm123
```

### Configuración Django (core/settings.py)

#### Aplicaciones Instaladas
```python
INSTALLED_APPS = [
    'jazzmin',                    # Admin moderno
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',             # API REST
    'corsheaders',                # CORS
    'django_filters',             # Filtros
    'store',                      # App principal
]
```

#### Configuración de Base de Datos
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': env("DB_NAME"),
        'USER': env("DB_USER"),
        'PASSWORD': env("DB_PASSWORD"),
        'HOST': env("DB_HOST"),
        'PORT': env("DB_PORT"),
        'OPTIONS': {
            'options': '-c search_path=ditaly_pasta,sbm_business,public',
            'connect_timeout': 10,
        },
    }
}
```

#### Configuración REST Framework
```python
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ],
}
```

#### Configuración CORS
```python
CORS_ALLOW_ALL_ORIGINS = True  # Solo para desarrollo
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOWED_ORIGINS = str(env("CORS_ALLOWED_ORIGINS")).split(",")
```

#### Deshabilitación de Migraciones
```python
MIGRATION_MODULES = {
    'store': None,
    'admin': None,
    'auth': None,
    'contenttypes': None,
    'sessions': None,
}
```

---

## 4. Base de Datos

### Esquemas de Base de Datos
El proyecto utiliza PostgreSQL con múltiples esquemas:

- **`sbm_business`**: Tablas principales del negocio
- **`ditaly_pasta`**: Tablas específicas de productos y catálogos
- **`public`**: Esquema por defecto

### Configuración de Search Path
```sql
SET search_path TO ditaly_pasta, sbm_business, public;
```

### Tablas Principales

#### Esquema sbm_business
- `menu` - Menús del sistema
- `item_group` - Grupos de items
- `item_category` - Categorías de items
- `item_type` - Tipos de items
- `user` - Usuarios del sistema
- `user_type` - Tipos de usuario
- `provider_type` - Tipos de proveedor
- `instruction` - Instrucciones del sistema
- `instruction_type` - Tipos de instrucción
- `package` - Paquetes
- `package_type` - Tipos de paquete
- `transport_type` - Tipos de transporte
- `measure_unit` - Unidades de medida
- `bank` - Bancos
- `bank_account_type` - Tipos de cuenta bancaria
- `region` - Regiones
- `district` - Distritos
- `role` - Roles del sistema
- `permission` - Permisos
- `restriction` - Restricciones

#### Esquema ditaly_pasta
- `catalog` - Catálogo de productos
- `provider` - Proveedores
- `product` - Productos
- `material` - Materiales
- `service` - Servicios
- `price` - Precios
- `item_configuration` - Configuraciones de items

---

## 5. Modelos de Datos

### Modelos Principales

#### Menu
```python
class Menu(models.Model):
    id = models.AutoField(primary_key=True)
    menu = models.CharField(max_length=50, verbose_name="Menú")
    description = models.TextField(verbose_name="Descripción")
    
    class Meta:
        db_table = 'menu'
        verbose_name = "Menú"
        verbose_name_plural = "Menús"
        ordering = ['menu']
```

#### ItemGroup
```python
class ItemGroup(models.Model):
    id = models.AutoField(primary_key=True)
    group_name = models.CharField(max_length=50, verbose_name="Nombre del Grupo")
    description = models.TextField(verbose_name="Descripción")
    catalog_render = models.BooleanField(default=True, verbose_name="Renderizar en Catálogo")
    
    class Meta:
        db_table = 'item_group'
        verbose_name = "Grupo de Items"
        verbose_name_plural = "Grupos de Items"
        ordering = ['group_name']
```

#### ItemCategory
```python
class ItemCategory(models.Model):
    id = models.AutoField(primary_key=True)
    category = models.CharField(max_length=50, verbose_name="Categoría")
    description = models.TextField(verbose_name="Descripción")
    catalog_render = models.BooleanField(default=True, verbose_name="Renderizar en Catálogo")
    
    class Meta:
        db_table = 'item_category'
        verbose_name = "Categoría de Items"
        verbose_name_plural = "Categorías de Items"
        ordering = ['category']
```

#### ItemType
```python
class ItemType(models.Model):
    id = models.AutoField(primary_key=True)
    type = models.CharField(max_length=50, verbose_name="Tipo")
    description = models.TextField(verbose_name="Descripción")
    
    class Meta:
        db_table = 'item_type'
        verbose_name = "Tipo de Item"
        verbose_name_plural = "Tipos de Items"
        ordering = ['type']
```

#### User
```python
class User(models.Model):
    id = models.AutoField(primary_key=True)
    code = models.CharField(max_length=36, unique=True, verbose_name="Código")
    type = models.ForeignKey(UserType, on_delete=models.CASCADE, db_column='type')
    google_id = models.CharField(max_length=255, unique=True, verbose_name="Google ID")
    mail = models.CharField(max_length=255, unique=True, verbose_name="Email")
    phone = models.BigIntegerField(verbose_name="Teléfono")
    name = models.CharField(max_length=255, verbose_name="Nombre")
    last_name = models.CharField(max_length=255, verbose_name="Apellido")
    is_active = models.BooleanField(null=True, blank=True, verbose_name="Activo")
    is_deleted = models.BooleanField(null=True, blank=True, verbose_name="Eliminado")
    is_confirmed = models.BooleanField(null=True, blank=True, verbose_name="Confirmado")
    created_at = models.DateTimeField(default=timezone.now, verbose_name="Fecha de Creación")
    updated_at = models.DateTimeField(null=True, blank=True, verbose_name="Fecha de Actualización")
    confirmed_at = models.DateTimeField(null=True, blank=True, verbose_name="Fecha de Confirmación")
    deleted_at = models.DateTimeField(null=True, blank=True, verbose_name="Fecha de Eliminación")
    deleted_by = models.CharField(max_length=36, null=True, blank=True, verbose_name="Eliminado por")
    log = models.TextField(default="init;", verbose_name="Log")
    version = models.IntegerField(default=1, verbose_name="Versión")
    
    class Meta:
        db_table = 'user'
        verbose_name = "Usuario"
        verbose_name_plural = "Usuarios"
        ordering = ['name']
```

#### Catalog
```python
class Catalog(models.Model):
    id = models.AutoField(primary_key=True)
    code = models.CharField(max_length=36, unique=True, null=True, blank=True, verbose_name="Código")
    sku = models.CharField(max_length=50, verbose_name="SKU")
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE, db_column='menu')
    group = models.ForeignKey(ItemGroup, on_delete=models.CASCADE, db_column='item_group')
    category = models.ForeignKey(ItemCategory, on_delete=models.CASCADE, db_column='category')
    type = models.ForeignKey(ItemType, on_delete=models.CASCADE, db_column='type')
    restriction = models.CharField(max_length=36, verbose_name="Restricción")
    name = models.CharField(max_length=50, verbose_name="Nombre")
    description = models.TextField(verbose_name="Descripción")
    obs = models.CharField(max_length=255, null=True, blank=True, verbose_name="Observaciones")
    chef_recommendation = models.BooleanField(default=False, verbose_name="Recomendación del Chef")
    usage_instructions = models.ForeignKey(Instruction, on_delete=models.CASCADE, db_column='usage_instructions')
    price = models.CharField(max_length=36, verbose_name="Precio", db_column='base_gross_price')
    min_quantity_purchase = models.IntegerField(default=1, verbose_name="Cantidad Mínima de Compra")
    rations_quantity = models.IntegerField(default=1, verbose_name="Cantidad de Raciones")
    cover_image = models.URLField(max_length=2083, null=True, blank=True, verbose_name="Imagen de Portada")
    secondary_image = models.URLField(max_length=2083, null=True, blank=True, verbose_name="Imagen Secundaria")
    complementary_image = models.URLField(max_length=2083, null=True, blank=True, verbose_name="Imagen Complementaria")
    image_gallery = models.URLField(max_length=2083, null=True, blank=True, verbose_name="Galería de Imágenes")
    configuration = models.CharField(max_length=36, verbose_name="Configuración")
    is_visible = models.BooleanField(default=True, verbose_name="Visible")
    is_deleted = models.BooleanField(null=True, blank=True, verbose_name="Eliminado")
    is_confirmed = models.BooleanField(null=True, blank=True, verbose_name="Confirmado")
    created_at = models.DateTimeField(default=timezone.now, verbose_name="Fecha de Creación")
    updated_at = models.DateTimeField(null=True, blank=True, verbose_name="Fecha de Actualización")
    confirmed_at = models.DateTimeField(null=True, blank=True, verbose_name="Fecha de Confirmación")
    deleted_at = models.DateTimeField(null=True, blank=True, verbose_name="Fecha de Eliminación")
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, db_column='created_by', to_field='code', related_name='catalogs_created')
    confirmed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, db_column='confirmed_by', to_field='code', related_name='catalogs_confirmed')
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, db_column='updated_by', to_field='code', related_name='catalogs_updated')
    deleted_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, db_column='deleted_by', to_field='code', related_name='catalogs_deleted')
    log = models.TextField(default="init;", verbose_name="Log")
    version = models.IntegerField(default=1, verbose_name="Versión")
    
    class Meta:
        db_table = 'catalog'
        verbose_name = "Catálogo"
        verbose_name_plural = "Catálogos"
        ordering = ['-created_at']
```

#### Provider
```python
class Provider(models.Model):
    id = models.AutoField(primary_key=True)
    code = models.CharField(max_length=36, unique=True, verbose_name="Código")
    provider = models.CharField(max_length=50, unique=True, verbose_name="Proveedor")
    type = models.ForeignKey(ProviderType, on_delete=models.CASCADE, db_column='type')
    rating = models.IntegerField(default=0, verbose_name="Calificación")
    obs_provider = models.TextField(verbose_name="Observaciones del Proveedor")
    contact_name = models.CharField(max_length=100, null=True, blank=True, verbose_name="Nombre de Contacto")
    contact_mail = models.CharField(max_length=255, null=True, blank=True, verbose_name="Email de Contacto")
    contact_phone = models.BigIntegerField(null=True, blank=True, verbose_name="Teléfono de Contacto")
    contact_phone2 = models.BigIntegerField(null=True, blank=True, verbose_name="Teléfono de Contacto 2")
    website_url = models.TextField(null=True, blank=True, verbose_name="URL del Sitio Web")
    obs_contact = models.CharField(max_length=255, null=True, blank=True, verbose_name="Observaciones de Contacto")
    company_name = models.CharField(max_length=255, null=True, blank=True, verbose_name="Nombre de la Empresa")
    company_rut = models.CharField(max_length=12, null=True, blank=True, verbose_name="RUT de la Empresa")
    company_activity = models.CharField(max_length=255, null=True, blank=True, verbose_name="Actividad de la Empresa")
    legal_representative = models.CharField(max_length=255, null=True, blank=True, verbose_name="Representante Legal")
    billing_address = models.TextField(null=True, blank=True, verbose_name="Dirección de Facturación")
    billing_mail = models.CharField(max_length=255, null=True, blank=True, verbose_name="Email de Facturación")
    billing_phone = models.BigIntegerField(null=True, blank=True, verbose_name="Teléfono de Facturación")
    company_bank = models.ForeignKey(Bank, on_delete=models.SET_NULL, null=True, blank=True, db_column='company_bank')
    bank_account_type = models.ForeignKey(BankAccountType, on_delete=models.SET_NULL, null=True, blank=True, db_column='bank_account_type')
    bank_account_number = models.CharField(max_length=255, null=True, blank=True, verbose_name="Número de Cuenta Bancaria")
    bank_account_mail = models.CharField(max_length=255, null=True, blank=True, verbose_name="Email de Cuenta Bancaria")
    dispatch_address = models.CharField(max_length=255, null=True, blank=True, verbose_name="Dirección de Despacho")
    dispatch_maps_location = models.CharField(max_length=255, null=True, blank=True, verbose_name="Ubicación en Maps")
    obs_dispatch = models.TextField(null=True, blank=True, verbose_name="Observaciones de Despacho")
    dispatch_district = models.ForeignKey(District, on_delete=models.SET_NULL, null=True, blank=True, db_column='dispatch_district')
    dispatch_region = models.ForeignKey(Region, on_delete=models.SET_NULL, null=True, blank=True, db_column='dispatch_region')
    is_active = models.BooleanField(default=True, verbose_name="Activo")
    is_deleted = models.BooleanField(null=True, blank=True, verbose_name="Eliminado")
    is_confirmed = models.BooleanField(null=True, blank=True, verbose_name="Confirmado")
    created_at = models.DateTimeField(default=timezone.now, verbose_name="Fecha de Creación")
    updated_at = models.DateTimeField(null=True, blank=True, verbose_name="Fecha de Actualización")
    confirmed_at = models.DateTimeField(null=True, blank=True, verbose_name="Fecha de Confirmación")
    deleted_at = models.DateTimeField(null=True, blank=True, verbose_name="Fecha de Eliminación")
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, db_column='created_by', to_field='code', related_name='providers_created')
    confirmed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, db_column='confirmed_by', to_field='code', related_name='providers_confirmed')
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, db_column='updated_by', to_field='code', related_name='providers_updated')
    deleted_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, db_column='deleted_by', to_field='code', related_name='providers_deleted')
    log = models.TextField(default="init;", verbose_name="Log")
    version = models.IntegerField(default=1, verbose_name="Versión")
    
    class Meta:
        db_table = 'provider'
        verbose_name = "Proveedor"
        verbose_name_plural = "Proveedores"
        ordering = ['provider']
```

---

## 6. API Endpoints

### Base URL
```
http://localhost:8081/api/
```

### Endpoints Principales

#### Catálogos
```
GET    /api/catalogs/                    # Listar catálogos
POST   /api/catalogs/                    # Crear catálogo
GET    /api/catalogs/{id}/               # Obtener catálogo específico
PUT    /api/catalogs/{id}/               # Actualizar catálogo
DELETE /api/catalogs/{id}/               # Eliminar catálogo
GET    /api/catalogs/visible/            # Solo catálogos visibles
POST   /api/catalogs/{id}/toggle_visibility/  # Alternar visibilidad
```

**Campos del Catálogo:**
- `id` - ID único
- `sku` - Código SKU
- `name` - Nombre del producto
- `description` - Descripción
- `menu_name` - Nombre del menú
- `group_name` - Nombre del grupo
- `category_name` - Nombre de la categoría
- `type_name` - Nombre del tipo
- `chef_recommendation` - Recomendación del chef
- `is_visible` - Visible en catálogo
- `cover_image` - Imagen de portada
- `secondary_image` - Imagen secundaria
- `complementary_image` - Imagen complementaria
- `image_gallery` - Galería de imágenes
- `price` - Precio
- `min_quantity_purchase` - Cantidad mínima de compra
- `rations_quantity` - Cantidad de raciones
- `created_at` - Fecha de creación

#### Menús
```
GET    /api/menus/                       # Listar menús
POST   /api/menus/                       # Crear menú
GET    /api/menus/{id}/                  # Obtener menú específico
PUT    /api/menus/{id}/                  # Actualizar menú
DELETE /api/menus/{id}/                  # Eliminar menú
```

#### Grupos de Items
```
GET    /api/item-groups/                 # Listar grupos
POST   /api/item-groups/                 # Crear grupo
GET    /api/item-groups/{id}/            # Obtener grupo específico
PUT    /api/item-groups/{id}/            # Actualizar grupo
DELETE /api/item-groups/{id}/            # Eliminar grupo
GET    /api/item-groups/catalog_groups/  # Solo grupos de catálogo
POST   /api/item-groups/{id}/toggle_catalog_render/  # Alternar renderizado
```

#### Categorías de Items
```
GET    /api/item-categories/             # Listar categorías
POST   /api/item-categories/             # Crear categoría
GET    /api/item-categories/{id}/        # Obtener categoría específica
PUT    /api/item-categories/{id}/        # Actualizar categoría
DELETE /api/item-categories/{id}/        # Eliminar categoría
GET    /api/item-categories/catalog_categories/  # Solo categorías de catálogo
POST   /api/item-categories/{id}/toggle_catalog_render/  # Alternar renderizado
```

#### Tipos de Items
```
GET    /api/item-types/                  # Listar tipos
POST   /api/item-types/                  # Crear tipo
GET    /api/item-types/{id}/             # Obtener tipo específico
PUT    /api/item-types/{id}/             # Actualizar tipo
DELETE /api/item-types/{id}/             # Eliminar tipo
```

#### Proveedores
```
GET    /api/providers/                   # Listar proveedores
POST   /api/providers/                   # Crear proveedor
GET    /api/providers/{id}/              # Obtener proveedor específico
PUT    /api/providers/{id}/              # Actualizar proveedor
DELETE /api/providers/{id}/              # Eliminar proveedor
GET    /api/providers/active/            # Solo proveedores activos
```

#### Usuarios
```
GET    /api/users/                       # Listar usuarios
POST   /api/users/                       # Crear usuario
GET    /api/users/{id}/                  # Obtener usuario específico
PUT    /api/users/{id}/                  # Actualizar usuario
DELETE /api/users/{id}/                  # Eliminar usuario
```

#### Instrucciones
```
GET    /api/instructions/                # Listar instrucciones
POST   /api/instructions/                # Crear instrucción
GET    /api/instructions/{id}/           # Obtener instrucción específica
PUT    /api/instructions/{id}/           # Actualizar instrucción
DELETE /api/instructions/{id}/           # Eliminar instrucción
GET    /api/instructions/active/         # Solo instrucciones activas
GET    /api/instructions/confirmed/      # Solo instrucciones confirmadas
POST   /api/instructions/{id}/confirm/   # Confirmar instrucción
POST   /api/instructions/{id}/soft_delete/  # Eliminación lógica
POST   /api/instructions/{id}/restore/   # Restaurar instrucción
```

#### Paquetes
```
GET    /api/packages/                    # Listar paquetes
POST   /api/packages/                    # Crear paquete
GET    /api/packages/{id}/               # Obtener paquete específico
PUT    /api/packages/{id}/               # Actualizar paquete
DELETE /api/packages/{id}/               # Eliminar paquete
```

#### Bancos
```
GET    /api/banks/                       # Listar bancos
POST   /api/banks/                       # Crear banco
GET    /api/banks/{id}/                  # Obtener banco específico
PUT    /api/banks/{id}/                  # Actualizar banco
DELETE /api/banks/{id}/                  # Eliminar banco
```

#### Regiones
```
GET    /api/regions/                     # Listar regiones
POST   /api/regions/                     # Crear región
GET    /api/regions/{id}/                # Obtener región específica
PUT    /api/regions/{id}/                # Actualizar región
DELETE /api/regions/{id}/                # Eliminar región
```

#### Distritos
```
GET    /api/districts/                   # Listar distritos
POST   /api/districts/                   # Crear distrito
GET    /api/districts/{id}/              # Obtener distrito específico
PUT    /api/districts/{id}/              # Actualizar distrito
DELETE /api/districts/{id}/              # Eliminar distrito
```

### Endpoints de Información
```
GET    /api/                             # Información general de la API
GET    /api/health/                      # Estado de salud
GET    /api/info/                        # Información del sistema
```

### Endpoints de Autenticación
```
POST   /api-token-auth/                  # Obtener token de autenticación
GET    /api-auth/                        # Autenticación por sesión
```

### Filtros y Búsqueda
Todos los endpoints soportan:
- **Filtros**: `?field=value`
- **Búsqueda**: `?search=texto`
- **Ordenamiento**: `?ordering=field` o `?ordering=-field`
- **Paginación**: `?page=1`

### Ejemplos de Uso

#### Obtener catálogos con filtros
```bash
curl -H "Authorization: Token tu_token" \
     "http://localhost:8081/api/catalogs/?is_visible=true&search=pasta"
```

#### Crear un catálogo
```bash
curl -X POST \
     -H "Authorization: Token tu_token" \
     -H "Content-Type: application/json" \
     -d '{
       "sku": "PASTA001",
       "name": "Pasta Carbonara",
       "description": "Pasta italiana con salsa carbonara",
       "menu": 1,
       "group": 1,
       "category": 1,
       "type": 1,
       "restriction": "uuid-restriction",
       "usage_instructions": "uuid-instructions",
       "price": "uuid-price",
       "configuration": "uuid-config",
       "created_by": "uuid-user"
     }' \
     "http://localhost:8081/api/catalogs/"
```

---

## 7. Autenticación y Permisos

### Tipos de Autenticación

#### 1. Autenticación por Token
```bash
# Obtener token
curl -X POST \
     -H "Content-Type: application/json" \
     -d '{"username": "admin", "password": "password"}' \
     "http://localhost:8081/api-token-auth/"

# Usar token
curl -H "Authorization: Token tu_token_aqui" \
     "http://localhost:8081/api/catalogs/"
```

#### 2. Autenticación por Sesión
```bash
# Loguearse en el admin
# Ir a http://localhost:8081/admin/
# Luego acceder a la API desde el navegador
```

#### 3. Autenticación Básica
```bash
curl -u username:password \
     "http://localhost:8081/api/catalogs/"
```

### Permisos
- **IsAuthenticated**: Requiere autenticación para todos los endpoints
- **IsAuthenticatedOrReadOnly**: Permite lectura pública, escritura solo autenticada
- **IsAdminUser**: Solo usuarios administradores

### Crear Superusuario
```bash
docker-compose exec core python manage.py createsuperuser
```

---

## 8. Configuración de Docker

### Docker Compose (docker-compose.yml)
```yaml
version: '3.8'

services:
  api:
    container_name: core
    build: ./core
    command: sh -c "sleep 10s; python manage.py runserver 0.0.0.0:8000"
    ports:
      - "8081:8000"
    env_file:
      - ./.api-env
    volumes:
      - .:/usr/src/app
    networks:
      - sbm-network

networks:
  sbm-network:
    external: true
    name: sbm-db_sbm-network
```

### Dockerfile (core/Dockerfile)
```dockerfile
FROM python:3.9-slim

WORKDIR /usr/src/app

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements e instalar dependencias Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código de la aplicación
COPY . .

# Exponer puerto
EXPOSE 8000

# Comando por defecto
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
```

### Entrypoint (entrypoint.sh)
```bash
#!/bin/sh 

echo "Starting Django application"

exec "$@"
```

### Comandos Docker

#### Iniciar servicios
```bash
docker-compose up -d
```

#### Ver logs
```bash
docker-compose logs
```

#### Ejecutar comandos en el contenedor
```bash
docker-compose exec core python manage.py shell
docker-compose exec core python manage.py createsuperuser
```

#### Reiniciar servicios
```bash
docker-compose restart
```

#### Detener servicios
```bash
docker-compose down
```

---

## 9. Despliegue

### Requisitos del Sistema
- Docker 20.10+
- Docker Compose 2.0+
- PostgreSQL 13+
- 2GB RAM mínimo
- 10GB espacio en disco

### Pasos de Despliegue

#### 1. Clonar el repositorio
```bash
git clone <repository-url>
cd DP-API
```

#### 2. Configurar variables de entorno
```bash
cp .api-env.example .api-env
# Editar .api-env con los valores correctos
```

#### 3. Construir y ejecutar
```bash
docker-compose up -d --build
```

#### 4. Crear superusuario
```bash
docker-compose exec core python manage.py createsuperuser
```

#### 5. Verificar funcionamiento
```bash
curl http://localhost:8081/api/health/
```

### Configuración de Producción

#### Variables de entorno para producción
```bash
DEBUG=0
ALLOWED_HOSTS=tu-dominio.com,www.tu-dominio.com
CORS_ALLOWED_ORIGINS=https://tu-dominio.com
SECRET_KEY=tu-secret-key-seguro
```

#### Configuración de base de datos para producción
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'production_db',
        'USER': 'production_user',
        'PASSWORD': 'secure_password',
        'HOST': 'production_host',
        'PORT': '5432',
        'OPTIONS': {
            'options': '-c search_path=ditaly_pasta,sbm_business,public',
            'connect_timeout': 10,
        },
    }
}
```

---

## 10. Guías de Desarrollo

### Estructura de Desarrollo

#### Agregar un nuevo modelo
1. Definir el modelo en `store/models.py`
2. Crear el serializer en `store/serializers.py`
3. Crear el ViewSet en `store/views.py`
4. Registrar las URLs en `store/urls.py`
5. Configurar el admin en `store/admin.py`

#### Ejemplo: Agregar modelo Product
```python
# store/models.py
class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    
    class Meta:
        db_table = 'product'

# store/serializers.py
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'price']

# store/views.py
class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

# store/urls.py
router.register(r'products', views.ProductViewSet)

# store/admin.py
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price']
```

### Convenciones de Código

#### Nombres de archivos
- Modelos: `models.py`
- Serializers: `serializers.py`
- Views: `views.py`
- URLs: `urls.py`
- Admin: `admin.py`

#### Nombres de clases
- Modelos: `PascalCase` (ej: `Product`)
- Serializers: `PascalCase + Serializer` (ej: `ProductSerializer`)
- ViewSets: `PascalCase + ViewSet` (ej: `ProductViewSet`)

#### Nombres de URLs
- Endpoints: `kebab-case` (ej: `/api/products/`)
- Acciones: `snake_case` (ej: `/api/products/active/`)

### Testing

#### Ejecutar tests
```bash
docker-compose exec core python manage.py test
```

#### Ejecutar tests específicos
```bash
docker-compose exec core python manage.py test store.tests
```

### Debugging

#### Logs de Django
```bash
docker-compose logs core
```

#### Shell de Django
```bash
docker-compose exec core python manage.py shell
```

#### Verificar base de datos
```bash
docker-compose exec core python manage.py dbshell
```

### Monitoreo

#### Endpoints de salud
- `GET /api/health/` - Estado general
- `GET /api/info/` - Información del sistema

#### Logs
- Django logs: `docker-compose logs core`
- Base de datos: Verificar conexión PostgreSQL

---

## 11. Troubleshooting

### Problemas Comunes

#### Error de conexión a base de datos
```bash
# Verificar que PostgreSQL esté ejecutándose
docker ps | grep postgres

# Verificar variables de entorno
cat .api-env

# Probar conexión
docker-compose exec core python manage.py dbshell
```

#### Error de migraciones
```bash
# Verificar configuración de MIGRATION_MODULES
# Las migraciones están deshabilitadas por diseño
```

#### Error de permisos
```bash
# Verificar que el usuario tenga permisos en PostgreSQL
# Verificar configuración de search_path
```

#### Error de CORS
```bash
# Verificar CORS_ALLOWED_ORIGINS en settings.py
# Verificar configuración de CORS en el frontend
```

### Comandos de Diagnóstico

#### Verificar estado de servicios
```bash
docker-compose ps
docker-compose logs
```

#### Verificar conectividad de red
```bash
docker network ls
docker network inspect sbm-db_sbm-network
```

#### Verificar configuración de base de datos
```bash
docker-compose exec core python manage.py check
```

---

## 12. Referencias

### Documentación Oficial
- [Django Documentation](https://docs.djangoproject.com/)
- [Django REST Framework](https://www.django-rest-framework.org/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [Docker Documentation](https://docs.docker.com/)

### Recursos Adicionales
- [Django Best Practices](https://docs.djangoproject.com/en/stable/misc/api-stability/)
- [REST API Design](https://restfulapi.net/)
- [PostgreSQL Schemas](https://www.postgresql.org/docs/current/ddl-schemas.html)

---

**Última actualización**: Julio 2025
**Versión**: 1.0.0
**Mantenido por**: Equipo de Desarrollo DP-API 