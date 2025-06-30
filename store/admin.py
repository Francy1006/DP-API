from django.contrib import admin
from .models import ItemGroup, Menu, ItemCategory, ItemType, InstructionType, Instruction, Catalog


@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    """
    Configuración del admin para Menu
    """
    list_display = ['id', 'menu', 'description']
    list_display_links = ['id', 'menu']
    search_fields = ['menu', 'description']
    ordering = ['menu']
    list_per_page = 20


@admin.register(ItemCategory)
class ItemCategoryAdmin(admin.ModelAdmin):
    """
    Configuración del admin para ItemCategory
    """
    list_display = ['id', 'category', 'description', 'catalog_render']
    list_display_links = ['id', 'category']
    list_filter = ['catalog_render']
    search_fields = ['category', 'description']
    ordering = ['category']
    list_per_page = 20
    list_editable = ['catalog_render']


@admin.register(ItemType)
class ItemTypeAdmin(admin.ModelAdmin):
    """
    Configuración del admin para ItemType
    """
    list_display = ['id', 'type', 'description']
    list_display_links = ['id', 'type']
    search_fields = ['type', 'description']
    ordering = ['type']
    list_per_page = 20


@admin.register(ItemGroup)
class ItemGroupAdmin(admin.ModelAdmin):
    """
    Configuración del admin para ItemGroup
    """
    list_display = ['id', 'group_name', 'description', 'catalog_render']
    list_display_links = ['id', 'group_name']
    list_filter = ['catalog_render']
    search_fields = ['group_name', 'description']
    ordering = ['group_name']
    list_per_page = 20
    list_editable = ['catalog_render']


@admin.register(InstructionType)
class InstructionTypeAdmin(admin.ModelAdmin):
    """
    Configuración del admin para InstructionType
    """
    list_display = [
        'id', 'type', 'description', 'is_deleted', 'is_confirmed', 
        'created_at', 'created_by'
    ]
    list_display_links = ['id', 'type']
    list_filter = [
        'is_deleted', 'is_confirmed', 'created_at', 
        'confirmed_at', 'deleted_at'
    ]
    search_fields = ['type', 'description', 'created_by']
    ordering = ['type']
    list_per_page = 20
    readonly_fields = [
        'id', 'created_at', 'updated_at', 'confirmed_at', 'deleted_at'
    ]
    
    fieldsets = (
        ('Información Básica', {
            'fields': ('type', 'description')
        }),
        ('Estado', {
            'fields': ('is_deleted', 'is_confirmed')
        }),
        ('Fechas', {
            'fields': ('created_at', 'updated_at', 'confirmed_at', 'deleted_at'),
            'classes': ('collapse',)
        }),
        ('Usuarios', {
            'fields': ('created_by', 'confirmed_by', 'updated_by', 'deleted_by'),
            'classes': ('collapse',)
        }),
    )
    
    def get_queryset(self, request):
        """
        Mostrar todos los tipos incluyendo eliminados
        """
        return super().get_queryset(request)
    
    def get_readonly_fields(self, request, obj=None):
        """
        Hacer algunos campos de solo lectura según el estado
        """
        readonly_fields = list(super().get_readonly_fields(request, obj))
        if obj and obj.is_deleted:
            readonly_fields.extend(['type', 'description'])
        return readonly_fields


@admin.register(Instruction)
class InstructionAdmin(admin.ModelAdmin):
    """
    Configuración del admin para Instruction
    """
    list_display = [
        'id', 'instruction', 'type', 'is_deleted', 'is_confirmed', 
        'created_at', 'created_by'
    ]
    list_display_links = ['id', 'instruction']
    list_filter = [
        'type', 'is_deleted', 'is_confirmed', 'created_at', 
        'confirmed_at', 'deleted_at'
    ]
    search_fields = ['instruction', 'description', 'created_by']
    ordering = ['-created_at']
    list_per_page = 20
    readonly_fields = [
        'id', 'created_at', 'updated_at', 'confirmed_at', 'deleted_at'
    ]
    
    fieldsets = (
        ('Información Básica', {
            'fields': ('instruction', 'description', 'url_documentation', 'type')
        }),
        ('Estado', {
            'fields': ('is_deleted', 'is_confirmed')
        }),
        ('Fechas', {
            'fields': ('created_at', 'updated_at', 'confirmed_at', 'deleted_at'),
            'classes': ('collapse',)
        }),
        ('Usuarios', {
            'fields': ('created_by', 'confirmed_by', 'updated_by', 'deleted_by'),
            'classes': ('collapse',)
        }),
    )
    
    def get_queryset(self, request):
        """
        Mostrar todas las instrucciones incluyendo eliminadas
        """
        return super().get_queryset(request)
    
    def get_readonly_fields(self, request, obj=None):
        """
        Hacer algunos campos de solo lectura según el estado
        """
        readonly_fields = list(super().get_readonly_fields(request, obj))
        if obj and obj.is_deleted:
            readonly_fields.extend(['instruction', 'description', 'url_documentation', 'type'])
        return readonly_fields


@admin.register(Catalog)
class CatalogAdmin(admin.ModelAdmin):
    """
    Configuración del admin para Catalog
    """
    list_display = [
        'id', 'sku', 'name', 'menu', 'group', 'category', 'type',
        'is_visible', 'is_deleted', 'is_confirmed', 'created_at'
    ]
    list_display_links = ['id', 'sku', 'name']
    list_filter = [
        'menu', 'group', 'category', 'type', 'is_visible', 'is_deleted', 
        'is_confirmed', 'chef_recommendation', 'created_at', 'confirmed_at', 'deleted_at'
    ]
    search_fields = ['sku', 'name', 'description', 'created_by']
    ordering = ['-created_at']
    list_per_page = 20
    readonly_fields = [
        'id', 'created_at', 'updated_at', 'confirmed_at', 'deleted_at'
    ]
    
    fieldsets = (
        ('Información Básica', {
            'fields': ('sku', 'name', 'description', 'OBS')
        }),
        ('Clasificación', {
            'fields': ('menu', 'group', 'category', 'type', 'restriction')
        }),
        ('Precios y Cantidades', {
            'fields': ('base_gross_price', 'min_quantity_purchase', 'rations_quantity')
        }),
        ('Imágenes', {
            'fields': ('cover_image', 'secondary_image', 'complementary_image', 'image_gallery'),
            'classes': ('collapse',)
        }),
        ('Configuración', {
            'fields': ('usage_instructions', 'configuration', 'chef_recommendation', 'is_visible')
        }),
        ('Estado', {
            'fields': ('is_deleted', 'is_confirmed')
        }),
        ('Fechas', {
            'fields': ('created_at', 'updated_at', 'confirmed_at', 'deleted_at'),
            'classes': ('collapse',)
        }),
        ('Usuarios', {
            'fields': ('created_by', 'confirmed_by', 'updated_by', 'deleted_by'),
            'classes': ('collapse',)
        }),
        ('Sistema', {
            'fields': ('LOG', 'version'),
            'classes': ('collapse',)
        }),
    )
    
    def get_queryset(self, request):
        """
        Mostrar todos los catálogos incluyendo eliminados
        """
        return super().get_queryset(request)
    
    def get_readonly_fields(self, request, obj=None):
        """
        Hacer algunos campos de solo lectura según el estado
        """
        readonly_fields = list(super().get_readonly_fields(request, obj))
        if obj and obj.is_deleted:
            readonly_fields.extend(['sku', 'name', 'description'])
        return readonly_fields
