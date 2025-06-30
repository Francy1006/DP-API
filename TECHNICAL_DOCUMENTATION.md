# DOCUMENTACIÓN TÉCNICA - DP-API

## ÍNDICE
1. [Descripción General](#1-descripción-general)
2. [Arquitectura del Sistema](#2-arquitectura-del-sistema)
3. [Configuración del Proyecto](#3-configuración-del-proyecto)
4. [Estructura de Aplicaciones](#4-estructura-de-aplicaciones)
5. [Modelos de Datos](#5-modelos-de-datos)
6. [API Endpoints](#6-api-endpoints)
7. [Configuración de Base de Datos](#7-configuración-de-base-de-datos)
8. [Autenticación y Autorización](#8-autenticación-y-autorización)
9. [Configuración de Docker](#9-configuración-de-docker)
10. [Variables de Entorno](#10-variables-de-entorno)
11. [Dependencias](#11-dependencias)
12. [Flujo de Datos](#12-flujo-de-datos)
13. [Consideraciones de Seguridad](#13-consideraciones-de-seguridad)
14. [Mantenimiento y Actualizaciones](#14-mantenimiento-y-actualizaciones)

---

## 1. DESCRIPCIÓN GENERAL

**DP-API** es una API REST desarrollada en Django que gestiona un sistema de catálogo de productos para Ditaly Pasta. El sistema maneja productos, materiales, servicios, proveedores, usuarios y configuraciones relacionadas con la gestión de inventario y catálogo.

### Características Principales:
- API REST completa con Django REST Framework
- Sistema de autenticación por tokens
- Gestión de catálogo de productos
- Sistema de roles y permisos
- Gestión de proveedores y materiales
- Interfaz administrativa con Django Jazzmin
- Configuración Docker para despliegue

---

## 2. ARQUITECTURA DEL SISTEMA

### Stack Tecnológico:
- **Backend**: Django 4.2.7
- **API**: Django REST Framework 3.14.0
- **Base de Datos**: MySQL 8.0
- **Contenedorización**: Docker & Docker Compose
- **Autenticación**: Token Authentication
- **CORS**: django-cors-headers
- **Filtros**: django-filter
- **Admin**: Django Jazzmin

### Estructura de Directorios:
```
DP-API/
├── core/                          # Aplicación principal Django
│   ├── core/                      # Configuración del proyecto
│   │   ├── settings.py           # Configuración principal
│   │   ├── urls.py               # URLs principales
│   │   ├── views.py              # Vistas principales
│   │   ├── asgi.py               # Configuración ASGI
│   │   └── wsgi.py               # Configuración WSGI
│   ├── store/                     # Aplicación de negocio
│   │   ├── models.py             # Modelos de datos
│   │   ├── views.py              # Vistas y ViewSets
│   │   ├── serializers.py        # Serializers para API
│   │   ├── urls.py               # URLs de la aplicación
│   │   └── admin.py              # Configuración admin
│   ├── templates/                 # Plantillas HTML
│   ├── .api-env                   # Variables de entorno
│   ├── requirements.txt           # Dependencias Python
│   └── Dockerfile                 # Configuración Docker
├── docker-compose.yml             # Orquestación de contenedores
└── TECHNICAL_DOCUMENTATION.md     # Este documento
```

---

## 3. CONFIGURACIÓN DEL PROYECTO

### Configuración Principal (settings.py)

#### Aplicaciones Instaladas:
```python
INSTALLED_APPS = [
    'jazzmin',                      # Tema moderno para admin
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',               # API REST
    'corsheaders',                  # CORS
    'django_filters',               # Filtros avanzados
    'store',                        # Aplicación principal
]
```

#### Middleware:
```python
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',  # CORS
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
```

#### Configuración REST Framework:
```python
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
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

---

## 4. ESTRUCTURA DE APLICACIONES

### Aplicación: `store`

La aplicación `store` es el núcleo del sistema y contiene todos los modelos de negocio.

#### Funcionalidades:
- Gestión de catálogo de productos
- Gestión de materiales y servicios
- Sistema de proveedores
- Gestión de usuarios y roles
- Sistema de permisos y restricciones
- Configuraciones de paquetes y transportes

---

## 5. MODELOS DE DATOS

### Modelos Principales

#### 1. Menu
```python
class Menu(models.Model):
    id = models.AutoField(primary_key=True)
    menu = models.CharField(max_length=50)
    description = models.TextField()
```
**Tabla**: `menu`
**Propósito**: Gestión de menús del sistema

#### 2. ItemCategory
```python
class ItemCategory(models.Model):
    id = models.AutoField(primary_key=True)
    category = models.CharField(max_length=50)
    description = models.TextField()
    cataloge_render = models.BooleanField(default=True)
```
**Tabla**: `item_category`
**Propósito**: Categorías de items con opción de renderizado en catálogo

#### 3. ItemType
```python
class ItemType(models.Model):
    id = models.AutoField(primary_key=True)
    type = models.CharField(max_length=50)
    description = models.TextField()
```
**Tabla**: `item_type`
**Propósito**: Tipos de items del sistema

#### 4. ItemGroup
```python
class ItemGroup(models.Model):
    id = models.AutoField(primary_key=True)
    group_name = models.CharField(max_length=50)
    description = models.TextField()
    cataloge_render = models.BooleanField(default=True)
```
**Tabla**: `item_group`
**Propósito**: Grupos de items con opción de renderizado en catálogo

#### 5. Cataloge
```python
class Cataloge(models.Model):
    id = models.AutoField(primary_key=True)
    code = models.CharField(max_length=36, unique=True)
    sku = models.CharField(max_length=50)
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE)
    group = models.ForeignKey(ItemGroup, on_delete=models.CASCADE)
    category = models.ForeignKey(ItemCategory, on_delete=models.CASCADE)
    type = models.ForeignKey(ItemType, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    description = models.TextField()
    base_gross_price = models.IntegerField(default=0)
    is_visible = models.BooleanField(default=True)
    # ... campos de auditoría
```
**Tabla**: `cataloge`
**Propósito**: Catálogo principal de productos

#### 6. User
```python
class User(models.Model):
    id = models.AutoField(primary_key=True)
    code = models.CharField(max_length=36, unique=True)
    type = models.ForeignKey(UserType, on_delete=models.CASCADE)
    google_id = models.CharField(max_length=255, unique=True)
    mail = models.EmailField(unique=True)
    phone = models.BigIntegerField()
    name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    is_active = models.BooleanField()
    # ... campos de auditoría
```
**Tabla**: `user`
**Propósito**: Gestión de usuarios del sistema

#### 7. Provider
```python
class Provider(models.Model):
    id = models.AutoField(primary_key=True)
    code = models.CharField(max_length=36, unique=True)
    provider = models.CharField(max_length=50, unique=True)
    type = models.ForeignKey(ProviderType, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)
    contact_name = models.CharField(max_length=100)
    contact_mail = models.EmailField()
    contact_phone = models.BigIntegerField()
    # ... campos de empresa y facturación
```
**Tabla**: `provider`
**Propósito**: Gestión de proveedores

#### 8. Product
```python
class Product(models.Model):
    id = models.AutoField(primary_key=True)
    code = models.CharField(max_length=36, unique=True)
    sku = models.CharField(max_length=50)
    description = models.TextField()
    provider = models.ForeignKey(Provider, on_delete=models.CASCADE)
    type = models.ForeignKey(ItemType, on_delete=models.CASCADE)
    group = models.ForeignKey(ItemGroup, on_delete=models.CASCADE)
    category = models.ForeignKey(ItemCategory, on_delete=models.CASCADE)
    package = models.ForeignKey(Package, on_delete=models.CASCADE)
    gross_price = models.IntegerField(default=0)
    # ... campos de auditoría
```
**Tabla**: `product`
**Propósito**: Gestión de productos

### Modelos de Seguridad

#### 9. Role
```python
class Role(models.Model):
    id = models.CharField(primary_key=True, max_length=36, default=uuid.uuid4)
    role = models.CharField(max_length=50, unique=True)
    description = models.TextField()
    # ... campos de auditoría
```
**Tabla**: `role`
**Propósito**: Roles del sistema

#### 10. Permission
```python
class Permission(models.Model):
    id = models.CharField(primary_key=True, max_length=36, default=uuid.uuid4)
    permission = models.CharField(max_length=50, unique=True)
    description = models.TextField()
    type = models.ForeignKey(PermissionType, on_delete=models.CASCADE)
    # ... campos de auditoría
```
**Tabla**: `permission`
**Propósito**: Permisos del sistema

#### 11. RolePermissions
```python
class RolePermissions(models.Model):
    id = models.CharField(primary_key=True, max_length=36, default=uuid.uuid4)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    permission = models.ForeignKey(Permission, on_delete=models.CASCADE)
    # ... campos de auditoría
```
**Tabla**: `role_permissions`
**Propósito**: Relación muchos a muchos entre roles y permisos

### Modelos de Configuración

#### 12. Package
```python
class Package(models.Model):
    id = models.AutoField(primary_key=True)
    description = models.TextField()
    package_type = models.ForeignKey(PackageType, on_delete=models.CASCADE)
    transport_type = models.ForeignKey(TransportType, on_delete=models.CASCADE)
    size = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    weight = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    measure_unit = models.ForeignKey(MeasureUnit, on_delete=models.CASCADE)
    # ... campos de auditoría
```
**Tabla**: `package`
**Propósito**: Configuración de paquetes

#### 13. Instruction
```python
class Instruction(models.Model):
    id = models.CharField(primary_key=True, max_length=36, default=uuid.uuid4)
    instruction = models.CharField(max_length=50)
    description = models.TextField()
    url_documentation = models.URLField()
    type = models.ForeignKey(InstructionType, on_delete=models.CASCADE)
    # ... campos de auditoría
```
**Tabla**: `instruction`
**Propósito**: Instrucciones del sistema

---

## 6. API ENDPOINTS

### URLs Principales

#### Core URLs (`core/urls.py`):
```
/                           # Vista principal
/api/                       # Vista raíz de la API
/api/health/                # Health check
/api/info/                  # Información de la API
/admin/                     # Admin de Django
/api-auth/                  # Autenticación REST Framework
/api-token-auth/            # Autenticación por token
```

#### Store URLs (`store/urls.py`):

##### ViewSets (Router automático):
```
/api/menus/                 # CRUD de menús
/api/item-categories/       # CRUD de categorías
/api/item-types/           # CRUD de tipos
/api/item-groups/          # CRUD de grupos
/api/instruction-types/    # CRUD de tipos de instrucción
/api/instructions/         # CRUD de instrucciones
/api/cataloge/             # CRUD de catálogo
/api/restrictions/         # CRUD de restricciones
/api/permission-types/     # CRUD de tipos de permiso
/api/permissions/          # CRUD de permisos
/api/roles/                # CRUD de roles
/api/restriction-roles/    # CRUD de restricción-roles
/api/role-permissions/     # CRUD de rol-permisos
/api/package-types/        # CRUD de tipos de paquete
/api/transport-types/      # CRUD de tipos de transporte
/api/measure-units/        # CRUD de unidades de medida
/api/provider-types/       # CRUD de tipos de proveedor
/api/bank-account-types/   # CRUD de tipos de cuenta bancaria
/api/regions/              # CRUD de regiones
/api/districts/            # CRUD de distritos
/api/banks/                # CRUD de bancos
/api/user-types/           # CRUD de tipos de usuario
/api/users/                # CRUD de usuarios
/api/user-tokens/          # CRUD de tokens de usuario
/api/packages/             # CRUD de paquetes
/api/item-configurations/  # CRUD de configuraciones
/api/item-configuration-details/ # CRUD de detalles de configuración
/api/providers/            # CRUD de proveedores
/api/products/             # CRUD de productos
/api/materials/            # CRUD de materiales
/api/services/             # CRUD de servicios
```

##### Endpoints Especiales:
```
/api/item-categories/catalog_categories/           # Solo categorías de catálogo
/api/item-categories/{id}/toggle_catalog_render/   # Alternar renderizado
/api/item-groups/catalog_groups/                   # Solo grupos de catálogo
/api/item-groups/{id}/toggle_catalog_render/       # Alternar renderizado
/api/instructions/active/                          # Solo instrucciones activas
/api/instructions/confirmed/                       # Solo instrucciones confirmadas
/api/instructions/{id}/confirm/                    # Confirmar instrucción
/api/instructions/{id}/soft_delete/                # Eliminación lógica
/api/instructions/{id}/restore/                    # Restaurar instrucción
/api/cataloge/visible/                             # Solo catálogo visible
/api/cataloge/{id}/toggle_visibility/              # Alternar visibilidad
```

### Operaciones CRUD por Endpoint

Cada ViewSet proporciona las siguientes operaciones:
- `GET /api/{model}/` - Listar todos (con paginación)
- `POST /api/{model}/` - Crear nuevo
- `GET /api/{model}/{id}/` - Obtener específico
- `PUT /api/{model}/{id}/` - Actualizar completo
- `PATCH /api/{model}/{id}/` - Actualizar parcial
- `DELETE /api/{model}/{id}/` - Eliminar

---

## 7. CONFIGURACIÓN DE BASE DE DATOS

### Configuración MySQL:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': env("DB_NAME"),           # ditaly_pasta
        'USER': env("DB_USER"),           # sbmqa
        'PASSWORD': env("DB_PASSWORD"),   # FrancY1
        'HOST': env("DB_HOST"),           # mysql
        'PORT': env("DB_PORT"),           # 3306
        'OPTIONS': {
            'charset': 'utf8mb4',
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
        },
    }
}
```

### Configuración de Migraciones:
```python
MIGRATION_MODULES = {
    'store': None,  # Deshabilitado - usando Flyway
}
```

---

## 8. AUTENTICACIÓN Y AUTORIZACIÓN

### Métodos de Autenticación:
1. **Session Authentication**: Para interfaz web
2. **Basic Authentication**: Para API
3. **Token Authentication**: Para API REST

### Endpoints de Autenticación:
```
/api-token-auth/            # Obtener token
/api-auth/                  # Interfaz de autenticación
```

### Sistema de Permisos:
- **PermissionType**: Tipos de permisos
- **Permission**: Permisos específicos
- **Role**: Roles del sistema
- **RolePermissions**: Asignación de permisos a roles
- **Restriction**: Restricciones del sistema
- **RestrictionRoles**: Asignación de restricciones a roles

---

## 9. CONFIGURACIÓN DE DOCKER

### Docker Compose:
```yaml
version: '3.9'

services:
  api:
    container_name: core
    build: ./core
    command: sh -c "sleep 10s; python manage.py migrate; python manage.py runserver 0.0.0.0:8081"
    ports:
      - "8081:8081"
    env_file:
      - ./core/.api-env
    volumes:
      - ./core:/usr/src/app
    networks:
      - shared-net

networks:
  shared-net:
    external: true
```

### Configuración del Contenedor:
- **Puerto**: 8081
- **Volumen**: Montaje del código fuente
- **Red**: shared-net (externa)
- **Variables de entorno**: Desde `.api-env`

---

## 10. VARIABLES DE ENTORNO

### Archivo `.api-env`:
```bash
# Django settings
DEBUG=0
SECRET_KEY=MysecretKey
ALLOWED_HOSTS=localhost,127.0.0.1,192.168.90.183,flask-app,core
CORS_ALLOWED_ORIGINS=http://localhost:8080,http://127.0.0.1:9000,http://flask-app:8001
STATIC_URL=static/

# Internationalization
LANGUAGE_CODE=es-ar
TIME_ZONE=America/Santiago
USE_I18N=1
USE_TZ=1

# MySQL connection
DB_NAME=ditaly_pasta
DB_USER=sbmqa
DB_PASSWORD=FrancY1
DB_HOST=mysql
DB_PORT=3306

# Media files
MEDIA_URL=/media/
MEDIA_ROOT=os.path.join(BASE_DIR, "media")

# Django Superuser Credentials
DJANGO_SUPERUSER_USERNAME=sbm-admin
DJANGO_SUPERUSER_EMAIL=operacione@ditalypasta.cl
DJANGO_SUPERUSER_PASSWORD=sbm123
```

---

## 11. DEPENDENCIAS

### Python Dependencies (`requirements.txt`):
```
asgiref==3.8.1
coverage==7.6.4
Django==4.2.7
django-cors-headers==4.3.1
django-environ==0.11.2
django-filter==23.3
djangorestframework==3.14.0
exceptiongroup==1.2.2
importlib_metadata==8.5.0
iniconfig==2.0.0
Markdown==3.7
mysqlclient==2.2.0
packaging==24.1
pillow==11.0.0
pluggy==1.5.0
pytest==8.3.3
pytest-django==4.9.0
sqlparse==0.5.1
tomli==2.0.2
typing_extensions==4.12.2
zipp==3.20.2
django-jazzmin==2.6.0
```

---

## 12. FLUJO DE DATOS

### 1. Gestión de Catálogo:
```
User Request → API Endpoint → ViewSet → Serializer → Model → Database
```

### 2. Autenticación:
```
Request → Token Authentication → Permission Check → Role Validation → Response
```

### 3. Filtrado y Búsqueda:
```
Request → Django Filter Backend → Search Filter → Ordering Filter → Response
```

### 4. Paginación:
```
QuerySet → PageNumberPagination → Serialized Response → JSON Response
```

---

## 13. CONSIDERACIONES DE SEGURIDAD

### 1. Autenticación:
- Tokens de autenticación para API
- Sesiones para interfaz web
- Validación de permisos por rol

### 2. CORS:
- Configuración específica de orígenes permitidos
- Credenciales habilitadas para desarrollo

### 3. Base de Datos:
- Conexión segura a MySQL
- Validación de datos en modelos
- Campos de auditoría para trazabilidad

### 4. Variables de Entorno:
- Configuración sensible en archivos .env
- No hardcodeo de credenciales

---

## 14. MANTENIMIENTO Y ACTUALIZACIONES

### Comandos Útiles:

#### Desarrollo:
```bash
# Iniciar servicios
docker-compose up -d

# Ver logs
docker-compose logs -f api

# Acceder al contenedor
docker exec -it core bash

# Crear superusuario
docker-compose exec api python manage.py createsuperuser

# Ejecutar migraciones
docker-compose exec api python manage.py migrate

# Recolectar archivos estáticos
docker-compose exec api python manage.py collectstatic
```

#### Producción:
```bash
# Reconstruir imagen
docker-compose build --no-cache

# Reiniciar servicios
docker-compose restart

# Backup de base de datos
docker-compose exec mysql mysqldump -u root -p ditaly_pasta > backup.sql
```

### Monitoreo:
- Health check endpoint: `/api/health/`
- Información de API: `/api/info/`
- Logs de Django en contenedor
- Logs de MySQL en contenedor de base de datos

### Actualizaciones:
1. Actualizar código fuente
2. Reconstruir imagen Docker
3. Reiniciar servicios
4. Verificar endpoints de health check
5. Validar funcionalidad crítica

---

## NOTAS ADICIONALES

### Características Especiales:
- **Soft Delete**: Implementado en modelos principales
- **Auditoría**: Campos de tracking automático
- **Confirmación**: Sistema de confirmación de registros
- **Visibilidad**: Control de visibilidad en catálogo
- **Renderizado**: Control de renderizado en catálogo

### Optimizaciones:
- Paginación automática (20 items por página)
- Filtros avanzados con django-filter
- Búsqueda y ordenamiento automático
- Serialización optimizada

### Interfaz Administrativa:
- Django Jazzmin para tema moderno
- Configuración personalizada de iconos
- Búsqueda en modelos principales
- Navegación expandida

---

**Última actualización**: Diciembre 2024
**Versión del documento**: 1.0
**Mantenido por**: Equipo de Desarrollo DP-API 