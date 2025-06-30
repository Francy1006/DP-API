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
# Nuevos ViewSets
router.register(r'cataloge', views.CatalogeViewSet)
router.register(r'restrictions', views.RestrictionViewSet)
router.register(r'permission-types', views.PermissionTypeViewSet)
router.register(r'permissions', views.PermissionViewSet)
router.register(r'roles', views.RoleViewSet)
router.register(r'restriction-roles', views.RestrictionRolesViewSet)
router.register(r'role-permissions', views.RolePermissionsViewSet)
router.register(r'package-types', views.PackageTypeViewSet)
router.register(r'transport-types', views.TransportTypeViewSet)
router.register(r'measure-units', views.MeasureUnitViewSet)
router.register(r'provider-types', views.ProviderTypeViewSet)
router.register(r'bank-account-types', views.BankAccountTypeViewSet)
router.register(r'regions', views.RegionViewSet)
router.register(r'districts', views.DistrictViewSet)
router.register(r'banks', views.BankViewSet)
router.register(r'user-types', views.UserTypeViewSet)
router.register(r'users', views.UserViewSet)
router.register(r'user-tokens', views.UserTokenViewSet)
router.register(r'packages', views.PackageViewSet)
router.register(r'item-configurations', views.ItemConfigurationViewSet)
router.register(r'item-configuration-details', views.ItemConfigurationDetailViewSet)
router.register(r'providers', views.ProviderViewSet)
router.register(r'products', views.ProductViewSet)
router.register(r'materials', views.MaterialViewSet)
router.register(r'services', views.ServiceViewSet)

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
# Endpoints disponibles:
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
# InstructionType:
# GET /api/instruction-types/ - Listar todos
# POST /api/instruction-types/ - Crear nuevo
# GET /api/instruction-types/{id}/ - Obtener específico
# PUT /api/instruction-types/{id}/ - Actualizar
# DELETE /api/instruction-types/{id}/ - Eliminar
#
# Instruction:
# GET /api/instructions/ - Listar todos
# POST /api/instructions/ - Crear nuevo
# GET /api/instructions/{id}/ - Obtener específico
# PUT /api/instructions/{id}/ - Actualizar
# DELETE /api/instructions/{id}/ - Eliminar
# GET /api/instructions/active/ - Solo activas
# GET /api/instructions/confirmed/ - Solo confirmadas
# POST /api/instructions/{id}/confirm/ - Confirmar
# POST /api/instructions/{id}/soft_delete/ - Eliminación lógica
# POST /api/instructions/{id}/restore/ - Restaurar
#
# Cataloge:
# GET /api/cataloge/ - Listar todos
# POST /api/cataloge/ - Crear nuevo
# GET /api/cataloge/{id}/ - Obtener específico
# PUT /api/cataloge/{id}/ - Actualizar
# DELETE /api/cataloge/{id}/ - Eliminar
# GET /api/cataloge/visible/ - Solo visibles
# POST /api/cataloge/{id}/toggle_visibility/ - Alternar visibilidad
#
# Restriction:
# GET /api/restrictions/ - Listar todos
# POST /api/restrictions/ - Crear nuevo
# GET /api/restrictions/{id}/ - Obtener específico
# PUT /api/restrictions/{id}/ - Actualizar
# DELETE /api/restrictions/{id}/ - Eliminar
#
# PermissionType:
# GET /api/permission-types/ - Listar todos
# POST /api/permission-types/ - Crear nuevo
# GET /api/permission-types/{id}/ - Obtener específico
# PUT /api/permission-types/{id}/ - Actualizar
# DELETE /api/permission-types/{id}/ - Eliminar
#
# Permission:
# GET /api/permissions/ - Listar todos
# POST /api/permissions/ - Crear nuevo
# GET /api/permissions/{id}/ - Obtener específico
# PUT /api/permissions/{id}/ - Actualizar
# DELETE /api/permissions/{id}/ - Eliminar
#
# Role:
# GET /api/roles/ - Listar todos
# POST /api/roles/ - Crear nuevo
# GET /api/roles/{id}/ - Obtener específico
# PUT /api/roles/{id}/ - Actualizar
# DELETE /api/roles/{id}/ - Eliminar
#
# RestrictionRoles:
# GET /api/restriction-roles/ - Listar todos
# POST /api/restriction-roles/ - Crear nuevo
# GET /api/restriction-roles/{id}/ - Obtener específico
# PUT /api/restriction-roles/{id}/ - Actualizar
# DELETE /api/restriction-roles/{id}/ - Eliminar
#
# RolePermissions:
# GET /api/role-permissions/ - Listar todos
# POST /api/role-permissions/ - Crear nuevo
# GET /api/role-permissions/{id}/ - Obtener específico
# PUT /api/role-permissions/{id}/ - Actualizar
# DELETE /api/role-permissions/{id}/ - Eliminar
#
# PackageType:
# GET /api/package-types/ - Listar todos
# POST /api/package-types/ - Crear nuevo
# GET /api/package-types/{id}/ - Obtener específico
# PUT /api/package-types/{id}/ - Actualizar
# DELETE /api/package-types/{id}/ - Eliminar
#
# TransportType:
# GET /api/transport-types/ - Listar todos
# POST /api/transport-types/ - Crear nuevo
# GET /api/transport-types/{id}/ - Obtener específico
# PUT /api/transport-types/{id}/ - Actualizar
# DELETE /api/transport-types/{id}/ - Eliminar
#
# MeasureUnit:
# GET /api/measure-units/ - Listar todos
# POST /api/measure-units/ - Crear nuevo
# GET /api/measure-units/{id}/ - Obtener específico
# PUT /api/measure-units/{id}/ - Actualizar
# DELETE /api/measure-units/{id}/ - Eliminar
#
# ProviderType:
# GET /api/provider-types/ - Listar todos
# POST /api/provider-types/ - Crear nuevo
# GET /api/provider-types/{id}/ - Obtener específico
# PUT /api/provider-types/{id}/ - Actualizar
# DELETE /api/provider-types/{id}/ - Eliminar
#
# BankAccountType:
# GET /api/bank-account-types/ - Listar todos
# POST /api/bank-account-types/ - Crear nuevo
# GET /api/bank-account-types/{id}/ - Obtener específico
# PUT /api/bank-account-types/{id}/ - Actualizar
# DELETE /api/bank-account-types/{id}/ - Eliminar
#
# Region:
# GET /api/regions/ - Listar todos
# POST /api/regions/ - Crear nuevo
# GET /api/regions/{id}/ - Obtener específico
# PUT /api/regions/{id}/ - Actualizar
# DELETE /api/regions/{id}/ - Eliminar
#
# District:
# GET /api/districts/ - Listar todos
# POST /api/districts/ - Crear nuevo
# GET /api/districts/{id}/ - Obtener específico
# PUT /api/districts/{id}/ - Actualizar
# DELETE /api/districts/{id}/ - Eliminar
#
# Bank:
# GET /api/banks/ - Listar todos
# POST /api/banks/ - Crear nuevo
# GET /api/banks/{id}/ - Obtener específico
# PUT /api/banks/{id}/ - Actualizar
# DELETE /api/banks/{id}/ - Eliminar
#
# UserType:
# GET /api/user-types/ - Listar todos
# POST /api/user-types/ - Crear nuevo
# GET /api/user-types/{id}/ - Obtener específico
# PUT /api/user-types/{id}/ - Actualizar
# DELETE /api/user-types/{id}/ - Eliminar
#
# User:
# GET /api/users/ - Listar todos
# POST /api/users/ - Crear nuevo
# GET /api/users/{id}/ - Obtener específico
# PUT /api/users/{id}/ - Actualizar
# DELETE /api/users/{id}/ - Eliminar
# GET /api/users/active/ - Solo activos
#
# UserToken:
# GET /api/user-tokens/ - Listar todos
# POST /api/user-tokens/ - Crear nuevo
# GET /api/user-tokens/{id}/ - Obtener específico
# PUT /api/user-tokens/{id}/ - Actualizar
# DELETE /api/user-tokens/{id}/ - Eliminar
#
# Package:
# GET /api/packages/ - Listar todos
# POST /api/packages/ - Crear nuevo
# GET /api/packages/{id}/ - Obtener específico
# PUT /api/packages/{id}/ - Actualizar
# DELETE /api/packages/{id}/ - Eliminar
#
# ItemConfiguration:
# GET /api/item-configurations/ - Listar todos
# POST /api/item-configurations/ - Crear nuevo
# GET /api/item-configurations/{id}/ - Obtener específico
# PUT /api/item-configurations/{id}/ - Actualizar
# DELETE /api/item-configurations/{id}/ - Eliminar
#
# ItemConfigurationDetail:
# GET /api/item-configuration-details/ - Listar todos
# POST /api/item-configuration-details/ - Crear nuevo
# GET /api/item-configuration-details/{id}/ - Obtener específico
# PUT /api/item-configuration-details/{id}/ - Actualizar
# DELETE /api/item-configuration-details/{id}/ - Eliminar
#
# Provider:
# GET /api/providers/ - Listar todos
# POST /api/providers/ - Crear nuevo
# GET /api/providers/{id}/ - Obtener específico
# PUT /api/providers/{id}/ - Actualizar
# DELETE /api/providers/{id}/ - Eliminar
# GET /api/providers/active/ - Solo activos
#
# Product:
# GET /api/products/ - Listar todos
# POST /api/products/ - Crear nuevo
# GET /api/products/{id}/ - Obtener específico
# PUT /api/products/{id}/ - Actualizar
# DELETE /api/products/{id}/ - Eliminar
# GET /api/products/active/ - Solo activos
#
# Material:
# GET /api/materials/ - Listar todos
# POST /api/materials/ - Crear nuevo
# GET /api/materials/{id}/ - Obtener específico
# PUT /api/materials/{id}/ - Actualizar
# DELETE /api/materials/{id}/ - Eliminar
# GET /api/materials/active/ - Solo activos
#
# Service:
# GET /api/services/ - Listar todos
# POST /api/services/ - Crear nuevo
# GET /api/services/{id}/ - Obtener específico
# PUT /api/services/{id}/ - Actualizar
# DELETE /api/services/{id}/ - Eliminar
# GET /api/services/active/ - Solo activos
#
# Parámetros de consulta disponibles:
# - ?search=texto - Búsqueda en campos de texto
# - ?ordering=campo - Ordenamiento
# - ?campo=valor - Filtrado por campo específico
# - ?include_deleted=true - Incluir registros eliminados (donde aplique) 