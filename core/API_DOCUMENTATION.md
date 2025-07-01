# API Documentation - ItemGroup CRUD

## Base URL
```
http://localhost:8000/store/api/
```

## Endpoints Principales

### 1. Listar grupos
**GET** `/item-groups/`

### 2. Obtener grupo específico
**GET** `/item-groups/{id}/`

### 3. Crear grupo
**POST** `/item-groups/`
```json
{
    "group_name": "Electrónicos",
    "description": "Productos electrónicos",
    "catalog_render": true
}
```

### 4. Actualizar grupo
**PUT** `/item-groups/{id}/`

### 5. Eliminar grupo
**DELETE** `/item-groups/{id}/`

### 6. Solo grupos de catálogo
**GET** `/item-groups/catalog_groups/`

## Ejemplo Flask

```python
import requests

def get_groups():
    response = requests.get("http://localhost:8000/store/api/item-groups/")
    return response.json() if response.status_code == 200 else []

def get_catalog_groups():
    response = requests.get("http://localhost:8000/store/api/item-groups/catalog_groups/")
    return response.json() if response.status_code == 200 else []
```

## Filtros
- `?catalog_render=true` - Solo grupos de catálogo
- `?search=texto` - Búsqueda por nombre/descripción
- `?ordering=group_name` - Ordenamiento

## Autenticación

Para usar la API con autenticación, primero obtén un token:

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

## Notas importantes

1. **CORS**: La API está configurada para permitir requests desde `localhost:3000` y `localhost:5000`
2. **Paginación**: Los resultados están paginados (20 items por página)
3. **Filtros**: Puedes combinar filtros, búsqueda y ordenamiento
4. **Validación**: Todos los campos son validados antes de guardar
5. **Timestamps**: Los campos `created_at` y `updated_at` se manejan automáticamente 