from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# Configurar el router para ViewSets
router = DefaultRouter()
router.register(r'item-groups', views.ItemGroupViewSet, basename='itemgroup')

# URLs para vistas individuales (alternativa al ViewSet)
urlpatterns = [
    # URLs del ViewSet (recomendado)
    path('api/', include(router.urls)),
    
    # URLs individuales (para mayor control)
    path('api/item-groups/', views.ItemGroupListAPIView.as_view(), name='itemgroup-list'),
    path('api/item-groups/<int:pk>/', views.ItemGroupDetailAPIView.as_view(), name='itemgroup-detail'),
]

# URLs adicionales del ViewSet
# Estas se generan automáticamente:
# GET /api/item-groups/ - Listar todos
# POST /api/item-groups/ - Crear nuevo
# GET /api/item-groups/{id}/ - Obtener específico
# PUT /api/item-groups/{id}/ - Actualizar
# DELETE /api/item-groups/{id}/ - Eliminar
# GET /api/item-groups/catalog_groups/ - Solo grupos de catálogo
# POST /api/item-groups/{id}/toggle_catalog_render/ - Alternar renderizado 