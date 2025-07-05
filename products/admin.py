from django.contrib import admin
from .models import (
    Menu, ItemCategory, ItemType, ItemGroup, PackageType, TransportType,
    MeasureUnit, Package, Catalog, ItemConfiguration, ItemConfigurationDetail,
    Product, Material, Service
)

@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    list_display = ['menu', 'description']
    search_fields = ['menu', 'description']
    ordering = ['menu']


@admin.register(ItemCategory)
class ItemCategoryAdmin(admin.ModelAdmin):
    list_display = ['category', 'description', 'catalog_render']
    list_filter = ['catalog_render']
    search_fields = ['category', 'description']
    ordering = ['category']


@admin.register(ItemType)
class ItemTypeAdmin(admin.ModelAdmin):
    list_display = ['type', 'description']
    search_fields = ['type', 'description']
    ordering = ['type']


@admin.register(ItemGroup)
class ItemGroupAdmin(admin.ModelAdmin):
    list_display = ['group_name', 'description', 'catalog_render']
    list_filter = ['catalog_render']
    search_fields = ['group_name', 'description']
    ordering = ['group_name']


@admin.register(PackageType)
class PackageTypeAdmin(admin.ModelAdmin):
    list_display = ['type', 'description']
    search_fields = ['type', 'description']
    ordering = ['type']


@admin.register(TransportType)
class TransportTypeAdmin(admin.ModelAdmin):
    list_display = ['type', 'description']
    search_fields = ['type', 'description']
    ordering = ['type']


@admin.register(MeasureUnit)
class MeasureUnitAdmin(admin.ModelAdmin):
    list_display = ['measure_unit', 'description']
    search_fields = ['measure_unit', 'description']
    ordering = ['measure_unit']


@admin.register(Package)
class PackageAdmin(admin.ModelAdmin):
    list_display = ['description', 'package_type', 'transport_type', 'size', 'weight', 'is_deleted', 'is_confirmed', 'created_at']
    list_filter = ['package_type', 'transport_type', 'is_deleted', 'is_confirmed', 'created_at']
    search_fields = ['description']
    ordering = ['description']
    readonly_fields = ['id', 'created_at', 'updated_at', 'confirmed_at', 'deleted_at']
    fieldsets = (
        ('Información del Paquete', {
            'fields': ('description', 'package_type', 'transport_type')
        }),
        ('Especificaciones', {
            'fields': ('size', 'weight', 'measure_unit', 'quantity_unit')
        }),
        ('Instrucciones', {
            'fields': ('storage_instructions', 'transport_instructions')
        }),
        ('Estado', {
            'fields': ('is_deleted', 'is_confirmed')
        }),
        ('Auditoría', {
            'fields': ('created_at', 'updated_at', 'confirmed_at', 'deleted_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Catalog)
class CatalogAdmin(admin.ModelAdmin):
    list_display = ['name', 'sku', 'menu', 'group', 'category', 'type', 'chef_recommendation', 'is_visible', 'is_deleted', 'is_confirmed', 'created_at']
    list_filter = ['menu', 'group', 'category', 'type', 'chef_recommendation', 'is_visible', 'is_deleted', 'is_confirmed', 'created_at']
    search_fields = ['name', 'sku', 'description']
    ordering = ['-created_at']
    readonly_fields = ['id', 'created_at', 'updated_at', 'confirmed_at', 'deleted_at', 'log', 'version']
    fieldsets = (
        ('Información Básica', {
            'fields': ('code', 'sku', 'name', 'description', 'obs')
        }),
        ('Clasificación', {
            'fields': ('menu', 'group', 'category', 'type', 'restriction')
        }),
        ('Características', {
            'fields': ('chef_recommendation', 'usage_instructions', 'price', 'min_quantity_purchase', 'rations_quantity')
        }),
        ('Imágenes', {
            'fields': ('cover_image', 'secondary_image', 'complementary_image', 'image_gallery')
        }),
        ('Configuración', {
            'fields': ('configuration', 'is_visible')
        }),
        ('Estado', {
            'fields': ('is_deleted', 'is_confirmed')
        }),
        ('Auditoría', {
            'fields': ('created_at', 'updated_at', 'confirmed_at', 'deleted_at', 'log', 'version'),
            'classes': ('collapse',)
        }),
    )


@admin.register(ItemConfiguration)
class ItemConfigurationAdmin(admin.ModelAdmin):
    list_display = ['code', 'configuration', 'description', 'package', 'is_deleted', 'is_confirmed', 'created_at']
    list_filter = ['package', 'is_deleted', 'is_confirmed', 'created_at']
    search_fields = ['code', 'configuration', 'description']
    ordering = ['configuration']
    readonly_fields = ['id', 'created_at', 'updated_at', 'confirmed_at', 'deleted_at', 'log', 'version']


@admin.register(ItemConfigurationDetail)
class ItemConfigurationDetailAdmin(admin.ModelAdmin):
    list_display = ['code', 'detail', 'type', 'configuration', 'id_item', 'is_deleted', 'is_confirmed', 'created_at']
    list_filter = ['type', 'configuration', 'is_deleted', 'is_confirmed', 'created_at']
    search_fields = ['code', 'detail', 'id_item']
    ordering = ['code']
    readonly_fields = ['created_at', 'updated_at', 'confirmed_at', 'deleted_at']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['code', 'sku', 'description', 'provider', 'type', 'group', 'category', 'is_active', 'is_deleted', 'is_confirmed', 'created_at']
    list_filter = ['provider', 'type', 'group', 'category', 'is_active', 'is_deleted', 'is_confirmed', 'created_at']
    search_fields = ['code', 'sku', 'description']
    ordering = ['description']
    readonly_fields = ['id', 'created_at', 'updated_at', 'confirmed_at', 'deleted_at', 'log', 'version']
    fieldsets = (
        ('Información Básica', {
            'fields': ('code', 'sku', 'description', 'obs')
        }),
        ('Clasificación', {
            'fields': ('type', 'group', 'category')
        }),
        ('Proveedor y Precios', {
            'fields': ('provider', 'price', 'package_unit', 'min_package_purchase')
        }),
        ('Paquete y URL', {
            'fields': ('package', 'url')
        }),
        ('Estado', {
            'fields': ('is_active', 'is_deleted', 'is_confirmed')
        }),
        ('Auditoría', {
            'fields': ('created_at', 'updated_at', 'confirmed_at', 'deleted_at', 'log', 'version'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    list_display = ['code', 'sku', 'description', 'provider', 'type', 'group', 'category', 'is_active', 'is_deleted', 'is_confirmed', 'created_at']
    list_filter = ['provider', 'type', 'group', 'category', 'is_active', 'is_deleted', 'is_confirmed', 'created_at']
    search_fields = ['code', 'sku', 'description']
    ordering = ['description']
    readonly_fields = ['id', 'created_at', 'updated_at', 'confirmed_at', 'deleted_at', 'log', 'version']
    fieldsets = (
        ('Información Básica', {
            'fields': ('code', 'sku', 'description', 'obs')
        }),
        ('Clasificación', {
            'fields': ('type', 'group', 'category')
        }),
        ('Proveedor y Precios', {
            'fields': ('provider', 'price', 'package_unit', 'min_package_purchase')
        }),
        ('Paquete y URL', {
            'fields': ('package', 'url')
        }),
        ('Estado', {
            'fields': ('is_active', 'is_deleted', 'is_confirmed')
        }),
        ('Auditoría', {
            'fields': ('created_at', 'updated_at', 'confirmed_at', 'deleted_at', 'log', 'version'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ['code', 'sku', 'description', 'provider', 'type', 'group', 'category', 'is_active', 'is_deleted', 'is_confirmed', 'created_at']
    list_filter = ['provider', 'type', 'group', 'category', 'is_active', 'is_deleted', 'is_confirmed', 'created_at']
    search_fields = ['code', 'sku', 'description']
    ordering = ['description']
    readonly_fields = ['id', 'created_at', 'updated_at', 'confirmed_at', 'deleted_at', 'log', 'version']
    fieldsets = (
        ('Información Básica', {
            'fields': ('code', 'sku', 'description', 'obs')
        }),
        ('Clasificación', {
            'fields': ('type', 'group', 'category')
        }),
        ('Proveedor y Precios', {
            'fields': ('provider', 'price', 'package_unit', 'min_package_purchase')
        }),
        ('URL', {
            'fields': ('url',)
        }),
        ('Estado', {
            'fields': ('is_active', 'is_deleted', 'is_confirmed')
        }),
        ('Auditoría', {
            'fields': ('created_at', 'updated_at', 'confirmed_at', 'deleted_at', 'log', 'version'),
            'classes': ('collapse',)
        }),
    )
