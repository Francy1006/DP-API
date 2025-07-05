from django.contrib import admin
from .models import Role, Permission, PermissionType, RolePermissions, Restriction, RestrictionRoles

@admin.register(PermissionType)
class PermissionTypeAdmin(admin.ModelAdmin):
    list_display = ['type', 'description', 'is_deleted', 'is_confirmed', 'created_at']
    list_filter = ['is_deleted', 'is_confirmed', 'created_at']
    search_fields = ['type', 'description']
    ordering = ['type']
    readonly_fields = ['id', 'created_at', 'updated_at', 'confirmed_at', 'deleted_at']


@admin.register(Permission)
class PermissionAdmin(admin.ModelAdmin):
    list_display = ['permission', 'type', 'description', 'is_deleted', 'is_confirmed', 'created_at']
    list_filter = ['type', 'is_deleted', 'is_confirmed', 'created_at']
    search_fields = ['permission', 'description']
    ordering = ['permission']
    readonly_fields = ['id', 'created_at', 'updated_at', 'confirmed_at', 'deleted_at', 'log', 'version']
    fieldsets = (
        ('Información del Permiso', {
            'fields': ('permission', 'description', 'type')
        }),
        ('Estado', {
            'fields': ('is_deleted', 'is_confirmed')
        }),
        ('Auditoría', {
            'fields': ('created_at', 'updated_at', 'confirmed_at', 'deleted_at', 'log', 'version'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ['role', 'description', 'is_deleted', 'is_confirmed', 'created_at']
    list_filter = ['is_deleted', 'is_confirmed', 'created_at']
    search_fields = ['role', 'description']
    ordering = ['role']
    readonly_fields = ['id', 'created_at', 'updated_at', 'confirmed_at', 'deleted_at', 'log', 'version']
    fieldsets = (
        ('Información del Rol', {
            'fields': ('role', 'description')
        }),
        ('Estado', {
            'fields': ('is_deleted', 'is_confirmed')
        }),
        ('Auditoría', {
            'fields': ('created_at', 'updated_at', 'confirmed_at', 'deleted_at', 'log', 'version'),
            'classes': ('collapse',)
        }),
    )


@admin.register(RolePermissions)
class RolePermissionsAdmin(admin.ModelAdmin):
    list_display = ['role', 'permission', 'is_deleted', 'is_confirmed', 'created_at']
    list_filter = ['role', 'permission', 'is_deleted', 'is_confirmed', 'created_at']
    search_fields = ['role__role', 'permission__permission']
    ordering = ['-created_at']
    readonly_fields = ['id', 'created_at', 'updated_at', 'confirmed_at', 'deleted_at']


@admin.register(Restriction)
class RestrictionAdmin(admin.ModelAdmin):
    list_display = ['restriction', 'description', 'is_deleted', 'is_confirmed', 'created_at']
    list_filter = ['is_deleted', 'is_confirmed', 'created_at']
    search_fields = ['restriction', 'description']
    ordering = ['restriction']
    readonly_fields = ['id', 'created_at', 'updated_at', 'confirmed_at', 'deleted_at', 'log', 'version']
    fieldsets = (
        ('Información de la Restricción', {
            'fields': ('restriction', 'description')
        }),
        ('Estado', {
            'fields': ('is_deleted', 'is_confirmed')
        }),
        ('Auditoría', {
            'fields': ('created_at', 'updated_at', 'confirmed_at', 'deleted_at', 'log', 'version'),
            'classes': ('collapse',)
        }),
    )


@admin.register(RestrictionRoles)
class RestrictionRolesAdmin(admin.ModelAdmin):
    list_display = ['restriction', 'role', 'is_deleted', 'is_confirmed', 'created_at']
    list_filter = ['restriction', 'role', 'is_deleted', 'is_confirmed', 'created_at']
    search_fields = ['restriction__restriction', 'role__role']
    ordering = ['-created_at']
    readonly_fields = ['id', 'created_at', 'updated_at', 'confirmed_at', 'deleted_at']
