from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    MenuViewSet, ItemCategoryViewSet, ItemTypeViewSet, ItemGroupViewSet,
    InstructionTypeViewSet, InstructionViewSet, CatalogViewSet, RestrictionViewSet,
    PermissionTypeViewSet, PermissionViewSet, RoleViewSet, RestrictionRolesViewSet,
    RolePermissionsViewSet, PackageTypeViewSet, TransportTypeViewSet, MeasureUnitViewSet,
    ProviderTypeViewSet, BankAccountTypeViewSet, RegionViewSet, DistrictViewSet,
    BankViewSet, UserTypeViewSet, UserViewSet, UserTokenViewSet, PackageViewSet,
    ItemConfigurationViewSet, ItemConfigurationDetailViewSet, ProviderViewSet,
    ProductViewSet, MaterialViewSet, ServiceViewSet,
    PriceViewSet, FiscalDirectiveTypeViewSet, FiscalDirectiveViewSet,
    FiscalFormulaViewSet, PriceFiscalConfigurationViewSet, FiscalConfigurationDetailViewSet
)

# Configurar el router para ViewSets
router = DefaultRouter()
router.register(r'menus', MenuViewSet)
router.register(r'item-categories', ItemCategoryViewSet)
router.register(r'item-types', ItemTypeViewSet)
router.register(r'item-groups', ItemGroupViewSet)
router.register(r'instruction-types', InstructionTypeViewSet)
router.register(r'instructions', InstructionViewSet)
# Nuevos ViewSets
router.register(r'catalog', CatalogViewSet)
router.register(r'restrictions', RestrictionViewSet)
router.register(r'permission-types', PermissionTypeViewSet)
router.register(r'permissions', PermissionViewSet)
router.register(r'roles', RoleViewSet)
router.register(r'restriction-roles', RestrictionRolesViewSet)
router.register(r'role-permissions', RolePermissionsViewSet)
router.register(r'package-types', PackageTypeViewSet)
router.register(r'transport-types', TransportTypeViewSet)
router.register(r'measure-units', MeasureUnitViewSet)
router.register(r'provider-types', ProviderTypeViewSet)
router.register(r'bank-account-types', BankAccountTypeViewSet)
router.register(r'regions', RegionViewSet)
router.register(r'districts', DistrictViewSet)
router.register(r'banks', BankViewSet)
router.register(r'user-types', UserTypeViewSet)
router.register(r'users', UserViewSet)
router.register(r'user-tokens', UserTokenViewSet)
router.register(r'packages', PackageViewSet)
router.register(r'item-configurations', ItemConfigurationViewSet)
router.register(r'item-configuration-details', ItemConfigurationDetailViewSet)
router.register(r'providers', ProviderViewSet)
router.register(r'products', ProductViewSet)
router.register(r'materials', MaterialViewSet)
router.register(r'services', ServiceViewSet)

# Nuevas rutas para precios y configuración fiscal
router.register(r'prices', PriceViewSet)
router.register(r'fiscal-directive-types', FiscalDirectiveTypeViewSet)
router.register(r'fiscal-directives', FiscalDirectiveViewSet)
router.register(r'fiscal-formulas', FiscalFormulaViewSet)
router.register(r'price-fiscal-configurations', PriceFiscalConfigurationViewSet)
router.register(r'fiscal-configuration-details', FiscalConfigurationDetailViewSet)

# URLs para ViewSets
viewset_urls = [
    path('', include(router.urls)),
]

# Eliminamos api_view_urls y la suma en urlpatterns
urlpatterns = viewset_urls

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
# Catalog:
# GET /api/catalog/ - Listar todos
# POST /api/catalog/ - Crear nuevo
# GET /api/catalog/{id}/ - Obtener específico
# PUT /api/catalog/{id}/ - Actualizar
# DELETE /api/catalog/{id}/ - Eliminar
# GET /api/catalog/visible/ - Solo visibles
# POST /api/catalog/{id}/toggle_visibility/ - Alternar visibilidad
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