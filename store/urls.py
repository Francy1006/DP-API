from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# Configurar el router para ViewSets
router = DefaultRouter()
router.register(r'menus', views.MenuViewSet)
router.register(r'item-categories', views.ItemCategoryViewSet)
router.register(r'item-types', views.ItemTypeViewSet)
router.register(r'item-groups', views.ItemGroupViewSet)
router.register(r'instruction-types', views.InstructionTypeViewSet)
router.register(r'instructions', views.InstructionViewSet)

# URLs para ViewSets
viewset_urls = [
    path('', include(router.urls)),
]

# URLs para API Views individuales
api_view_urls = [
    # Menu URLs
    path('menus/', views.MenuListAPIView.as_view(), name='menu-list'),
    path('menus/<int:pk>/', views.MenuDetailAPIView.as_view(), name='menu-detail'),
    
    # ItemCategory URLs
    path('item-categories/', views.ItemCategoryListAPIView.as_view(), name='item-category-list'),
    path('item-categories/<int:pk>/', views.ItemCategoryDetailAPIView.as_view(), name='item-category-detail'),
    
    # ItemType URLs
    path('item-types/', views.ItemTypeListAPIView.as_view(), name='item-type-list'),
    path('item-types/<int:pk>/', views.ItemTypeDetailAPIView.as_view(), name='item-type-detail'),
    
    # ItemGroup URLs
    path('item-groups/', views.ItemGroupListAPIView.as_view(), name='item-group-list'),
    path('item-groups/<int:pk>/', views.ItemGroupDetailAPIView.as_view(), name='item-group-detail'),
    
    # InstructionType URLs
    path('instruction-types/', views.InstructionTypeListAPIView.as_view(), name='instruction-type-list'),
    path('instruction-types/<int:pk>/', views.InstructionTypeDetailAPIView.as_view(), name='instruction-type-detail'),
    
    # Instruction URLs
    path('instructions/', views.InstructionListAPIView.as_view(), name='instruction-list'),
    path('instructions/<str:pk>/', views.InstructionDetailAPIView.as_view(), name='instruction-detail'),
]

# Combinar todas las URLs
urlpatterns = viewset_urls + api_view_urls

# URLs adicionales del ViewSet
# Estas se generan automáticamente:
# 
# ItemGroup:
# GET /api/item-groups/ - Listar todos
# POST /api/item-groups/ - Crear nuevo
# GET /api/item-groups/{id}/ - Obtener específico
# PUT /api/item-groups/{id}/ - Actualizar
# DELETE /api/item-groups/{id}/ - Eliminar
# GET /api/item-groups/catalog_groups/ - Solo grupos de catálogo
# POST /api/item-groups/{id}/toggle_catalog_render/ - Alternar renderizado
#
# Menu:
# GET /api/menus/ - Listar todos
# POST /api/menus/ - Crear nuevo
# GET /api/menus/{id}/ - Obtener específico
# PUT /api/menus/{id}/ - Actualizar
# DELETE /api/menus/{id}/ - Eliminar
#
# ItemCategory:
# GET /api/item-categories/ - Listar todos
# POST /api/item-categories/ - Crear nuevo
# GET /api/item-categories/{id}/ - Obtener específico
# PUT /api/item-categories/{id}/ - Actualizar
# DELETE /api/item-categories/{id}/ - Eliminar
# GET /api/item-categories/catalog_categories/ - Solo categorías de catálogo
# POST /api/item-categories/{id}/toggle_catalog_render/ - Alternar renderizado
#
# ItemType:
# GET /api/item-types/ - Listar todos
# POST /api/item-types/ - Crear nuevo
# GET /api/item-types/{id}/ - Obtener específico
# PUT /api/item-types/{id}/ - Actualizar
# DELETE /api/item-types/{id}/ - Eliminar 