from django.http import JsonResponse
from django.shortcuts import render


def home(request):
    """
    Vista principal que muestra la página HTML de la API de Ditaly Pasta
    """
    context = {
        "api_name": "Ditaly Pasta API",
        "version": "1.0.0",
        "company": "Ditaly Pasta",
        "endpoints": [
            {
                "name": "Admin Panel",
                "url": "/admin/",
                "description": "Panel de administración de Django",
                "method": "GET"
            },
            {
                "name": "Item Groups",
                "url": "/store/api/item-groups/",
                "description": "CRUD completo para grupos de items",
                "method": "GET, POST, PUT, DELETE"
            },
            {
                "name": "Catalog Groups",
                "url": "/store/api/item-groups/catalog_groups/",
                "description": "Solo grupos que se renderizan en catálogo",
                "method": "GET"
            },
            {
                "name": "Authentication",
                "url": "/api-token-auth/",
                "description": "Autenticación por token",
                "method": "POST"
            }
        ]
    }
    
    return render(request, 'home.html', context)


def api_root(request):
    """
    Vista raíz de la API que lista todos los endpoints disponibles
    """
    api_endpoints = {
        "item_groups": {
            "url": "/store/api/item-groups/",
            "methods": ["GET", "POST"],
            "description": "CRUD completo para grupos de items"
        },
        "catalog_groups": {
            "url": "/store/api/item-groups/catalog_groups/",
            "methods": ["GET"],
            "description": "Solo grupos que se renderizan en catálogo"
        },
        "admin": {
            "url": "/admin/",
            "methods": ["GET"],
            "description": "Panel de administración de Django"
        },
        "auth": {
            "url": "/api-token-auth/",
            "methods": ["POST"],
            "description": "Autenticación por token"
        }
    }
    
    return JsonResponse(api_endpoints, json_dumps_params={'indent': 2}) 