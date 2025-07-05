from django.contrib import admin
from .models import User, UserType, UserToken

@admin.register(UserType)
class UserTypeAdmin(admin.ModelAdmin):
    list_display = ['type', 'description', 'created_at']
    search_fields = ['type', 'description']
    ordering = ['type']
    readonly_fields = ['created_at']


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['name', 'last_name', 'mail', 'type', 'is_active', 'is_confirmed', 'created_at']
    list_filter = ['type', 'is_active', 'is_confirmed', 'is_deleted', 'created_at']
    search_fields = ['name', 'last_name', 'mail', 'google_id']
    readonly_fields = ['id', 'created_at', 'updated_at', 'confirmed_at', 'deleted_at', 'log', 'version']
    ordering = ['name']
    fieldsets = (
        ('Información Personal', {
            'fields': ('name', 'last_name', 'mail', 'phone', 'google_id')
        }),
        ('Tipo y Estado', {
            'fields': ('type', 'is_active', 'is_confirmed', 'is_deleted')
        }),
        ('Auditoría', {
            'fields': ('created_at', 'updated_at', 'confirmed_at', 'deleted_at', 'deleted_by', 'log', 'version'),
            'classes': ('collapse',)
        }),
    )


@admin.register(UserToken)
class UserTokenAdmin(admin.ModelAdmin):
    list_display = ['user_id', 'ip_address', 'created_at', 'expires_at', 'revoked_at']
    list_filter = ['created_at', 'expires_at', 'revoked_at']
    search_fields = ['user_id__name', 'user_id__mail', 'ip_address']
    readonly_fields = ['id', 'created_at']
    ordering = ['-created_at']
    fieldsets = (
        ('Información del Token', {
            'fields': ('user_id', 'token', 'ip_address', 'user_agent')
        }),
        ('Fechas', {
            'fields': ('created_at', 'expires_at', 'revoked_at')
        }),
    )
