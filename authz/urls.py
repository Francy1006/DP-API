from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'permission-types', views.PermissionTypeViewSet)
router.register(r'permissions', views.PermissionViewSet)
router.register(r'roles', views.RoleViewSet)
router.register(r'role-permissions', views.RolePermissionsViewSet)
router.register(r'restrictions', views.RestrictionViewSet)
router.register(r'restriction-roles', views.RestrictionRolesViewSet)

urlpatterns = [
    path('', include(router.urls)),
] 