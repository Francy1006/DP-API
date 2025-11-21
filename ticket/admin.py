from django.contrib import admin
from .models import Ticket


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ['id', 'code', 'sku', 'description', 'type', 'category', 'filter_classification', 'is_active', 'is_confirmed', 'created_at']
    list_filter = ['is_active', 'is_confirmed', 'is_deleted', 'type', 'category', 'filter_classification', 'created_at']
    search_fields = ['code', 'sku', 'description']
    readonly_fields = ['id', 'created_at', 'updated_at', 'confirmed_at', 'deleted_at', 'log', 'version']
    
    fieldsets = (
        ('Información Básica', {
            'fields': ('id', 'code', 'sku', 'description', 'obs')
        }),
        ('Imágenes', {
            'fields': ('cover_image', 'secondary_image', 'complementary_image', 'image_gallery')
        }),
        ('Configuración', {
            'fields': ('type', 'item_group', 'category', 'filter_classification', 'package', 'package_unit', 'min_package_purchase', 'price', 'url')
        }),
        ('Estado', {
            'fields': ('is_active', 'is_deleted', 'is_confirmed')
        }),
        ('Auditoría', {
            'fields': ('created_by', 'confirmed_by', 'updated_by', 'deleted_by')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at', 'confirmed_at', 'deleted_at')
        }),
        ('Sistema', {
            'fields': ('log', 'version')
        }),
    )






