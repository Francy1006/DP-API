# API Documentation - DP-API

## Base URL
```
http://localhost:8081/api/
```

## Endpoints Principales

### Grupos de Items (ItemGroup)
- **GET** `/item-groups/` - Listar todos los grupos
- **POST** `/item-groups/` - Crear un nuevo grupo
- **GET** `/item-groups/{id}/` - Obtener un grupo específico
- **PUT** `/item-groups/{id}/` - Actualizar un grupo
- **DELETE** `/item-groups/{id}/` - Eliminar un grupo
- **GET** `/item-groups/catalog_groups/` - Solo grupos para catálogo
- **POST** `/item-groups/{id}/toggle_catalog_render/` - Alternar renderizado en catálogo

### Categorías de Items (ItemCategory)
- **GET** `/item-categories/` - Listar todas las categorías
- **POST** `/item-categories/` - Crear una nueva categoría
- **GET** `/item-categories/{id}/` - Obtener una categoría específica
- **PUT** `/item-categories/{id}/` - Actualizar una categoría
- **DELETE** `/item-categories/{id}/` - Eliminar una categoría
- **GET** `/item-categories/catalog_categories/` - Solo categorías para catálogo
- **POST** `/item-categories/{id}/toggle_catalog_render/` - Alternar renderizado en catálogo

### Tipos de Items (ItemType)
- **GET** `/item-types/` - Listar todos los tipos
- **POST** `/item-types/` - Crear un nuevo tipo
- **GET** `/item-types/{id}/` - Obtener un tipo específico
- **PUT** `/item-types/{id}/` - Actualizar un tipo
- **DELETE** `/item-types/{id}/` - Eliminar un tipo

### Menús
- **GET** `/menus/` - Listar todos los menús
- **POST** `/menus/` - Crear un nuevo menú
- **GET** `/menus/{id}/` - Obtener un menú específico
- **PUT** `/menus/{id}/` - Actualizar un menú
- **DELETE** `/menus/{id}/` - Eliminar un menú

### Tipos de Instrucción (InstructionType)
- **GET** `/instruction-types/` - Listar todos los tipos de instrucciones
- **POST** `/instruction-types/` - Crear un nuevo tipo de instrucción
- **GET** `/instruction-types/{id}/` - Obtener un tipo específico
- **PUT** `/instruction-types/{id}/` - Actualizar un tipo
- **DELETE** `/instruction-types/{id}/` - Eliminar un tipo

### Instrucciones (Instruction)
- **GET** `/instructions/` - Listar todas las instrucciones activas
- **POST** `/instructions/` - Crear una nueva instrucción
- **GET** `/instructions/{id}/` - Obtener una instrucción específica
- **PUT** `/instructions/{id}/` - Actualizar una instrucción
- **DELETE** `/instructions/{id}/` - Eliminación lógica de instrucción
- **GET** `/instructions/active/` - Solo instrucciones activas
- **GET** `/instructions/confirmed/` - Solo instrucciones confirmadas
- **POST** `/instructions/{id}/confirm/` - Confirmar una instrucción
- **POST** `/instructions/{id}/soft_delete/` - Eliminación lógica
- **POST** `/instructions/{id}/restore/` - Restaurar instrucción eliminada

### Otros Endpoints
- **GET** `/health/` - Verificación de salud de la API
- **GET** `/info/` - Información general de la API
- **POST** `/api-token-auth/` - Autenticación por token
- **GET** `/admin/` - Panel de administración de Django

## Modelo ItemGroup

- **id** (AutoField)
- **group_name** (CharField, max_length=50)
- **description** (TextField)
- **catalog_render** (BooleanField, default=True)

## Ejemplo de Petición para Crear un Grupo
```json
{
    "group_name": "Electrónicos",
    "description": "Productos electrónicos",
    "catalog_render": true
}
```

## Filtros Disponibles
- `?catalog_render=true` - Solo grupos de catálogo
- `?search=texto` - Búsqueda por nombre/descripción
- `?ordering=group_name` - Ordenamiento

## Ejemplo de Consumo en Python
```python
import requests

# Listar grupos
def get_groups():
    response = requests.get("http://localhost:8081/api/item-groups/")
    return response.json() if response.status_code == 200 else []

# Listar solo grupos de catálogo
def get_catalog_groups():
    response = requests.get("http://localhost:8081/api/item-groups/catalog_groups/")
    return response.json() if response.status_code == 200 else []
```

## Autenticación

Para usar la API, primero obtén un token:

**POST** `/api-token-auth/`
```json
{
    "username": "admin",
    "password": "tu_password"
}
```
**Response:**
```json
{
    "token": "tu_token_aqui"
}
```
Luego incluye el token en los headers:
```
Authorization: Token tu_token_aqui
```

## Notas Técnicas

1. **CORS**: La API permite requests desde cualquier origen en desarrollo (`CORS_ALLOW_ALL_ORIGINS = True`).
2. **Paginación**: Los resultados están paginados (20 items por página).
3. **Filtros**: Puedes combinar filtros, búsqueda y ordenamiento.
4. **Validación**: Todos los campos son validados antes de guardar.
5. **Timestamps**: Los campos `created_at` y `updated_at` se manejan automáticamente (en modelos que los incluyen).
6. **Panel Admin**: Acceso vía `/admin/`.

---

Para más detalles, consulta la documentación técnica o explora el endpoint `/api/` para ver todos los recursos disponibles. 