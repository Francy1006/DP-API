from django.contrib import admin
from .models import (
    ItemGroup, Menu, ItemCategory, ItemType, InstructionType, Instruction, 
    Catalog, Restriction, BankAccountType, Region, District, Bank, UserType, 
    User, UserToken, Package, ItemConfiguration, ItemConfigurationDetail, 
    Provider, Product, Material, Service, PermissionType, Permission, Role, 
    RestrictionRoles, RolePermissions, PackageType, TransportType, MeasureUnit, 
    ProviderType, Price, FiscalDirectiveType, FiscalDirective, FiscalFormula, 
    PriceFiscalConfiguration, FiscalConfigurationDetail
)


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
            'fields': ('sku', 'name', 'description', 'obs')
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
            'fields': ('log', 'version'),
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


@admin.register(Restriction)
class RestrictionAdmin(admin.ModelAdmin):
    """
    Configuración del admin para Restriction
    """
    list_display = [
        'id', 'restriction', 'description', 'is_deleted', 'is_confirmed', 
        'created_at', 'created_by'
    ]
    list_display_links = ['id', 'restriction']
    list_filter = [
        'is_deleted', 'is_confirmed', 'created_at', 
        'confirmed_at', 'deleted_at'
    ]
    search_fields = ['restriction', 'description', 'created_by']
    ordering = ['restriction']
    list_per_page = 20
    readonly_fields = [
        'id', 'created_at', 'updated_at', 'confirmed_at', 'deleted_at'
    ]
    
    fieldsets = (
        ('Información Básica', {
            'fields': ('restriction', 'description')
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
            'fields': ('log', 'version'),
            'classes': ('collapse',)
        }),
    )
    
    def get_queryset(self, request):
        """
        Mostrar todas las restricciones incluyendo eliminadas
        """
        return super().get_queryset(request)
    
    def get_readonly_fields(self, request, obj=None):
        """
        Hacer algunos campos de solo lectura según el estado
        """
        readonly_fields = list(super().get_readonly_fields(request, obj))
        if obj and obj.is_deleted:
            readonly_fields.extend(['restriction', 'description'])
        return readonly_fields


@admin.register(BankAccountType)
class BankAccountTypeAdmin(admin.ModelAdmin):
    list_display = ['type', 'description']
    search_fields = ['type', 'description']
    ordering = ['type']


@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    list_display = ['region', 'description']
    search_fields = ['region', 'description']
    ordering = ['region']


@admin.register(District)
class DistrictAdmin(admin.ModelAdmin):
    list_display = ['district', 'region', 'description']
    list_filter = ['region']
    search_fields = ['district', 'description']
    ordering = ['district']


@admin.register(Bank)
class BankAdmin(admin.ModelAdmin):
    list_display = ['bank', 'description', 'created_at']
    search_fields = ['bank', 'description']
    ordering = ['bank']
    readonly_fields = ['created_at']


@admin.register(UserType)
class UserTypeAdmin(admin.ModelAdmin):
    list_display = ['type', 'description', 'created_at']
    search_fields = ['type', 'description']
    ordering = ['type']
    readonly_fields = ['created_at']


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['code', 'name', 'last_name', 'mail', 'type', 'is_active', 'is_confirmed']
    list_filter = ['type', 'is_active', 'is_confirmed', 'is_deleted', 'created_at']
    search_fields = ['code', 'name', 'last_name', 'mail', 'google_id']
    ordering = ['name', 'last_name']
    readonly_fields = ['created_at', 'updated_at', 'confirmed_at', 'deleted_at']
    fieldsets = (
        ('Información Básica', {
            'fields': ('code', 'type', 'google_id', 'mail', 'phone', 'name', 'last_name')
        }),
        ('Estado', {
            'fields': ('is_active', 'is_confirmed', 'is_deleted')
        }),
        ('Fechas', {
            'fields': ('created_at', 'updated_at', 'confirmed_at', 'deleted_at', 'deleted_by'),
            'classes': ('collapse',)
        }),
        ('Auditoría', {
            'fields': ('log', 'version'),
            'classes': ('collapse',)
        }),
    )


@admin.register(UserToken)
class UserTokenAdmin(admin.ModelAdmin):
    list_display = ['id', 'user_id', 'ip_address', 'created_at', 'expires_at', 'revoked_at']
    list_filter = ['created_at', 'expires_at', 'revoked_at']
    search_fields = ['user_id__name', 'user_id__last_name', 'ip_address']
    ordering = ['-created_at']
    readonly_fields = ['created_at']


@admin.register(Package)
class PackageAdmin(admin.ModelAdmin):
    list_display = ['description', 'package_type', 'transport_type', 'size', 'weight', 'is_confirmed']
    list_filter = ['package_type', 'transport_type', 'measure_unit', 'is_confirmed', 'is_deleted', 'created_at']
    search_fields = ['description']
    ordering = ['description']
    readonly_fields = ['created_at', 'updated_at', 'confirmed_at', 'deleted_at']
    fieldsets = (
        ('Información Básica', {
            'fields': ('description', 'package_type', 'transport_type')
        }),
        ('Especificaciones', {
            'fields': ('size', 'weight', 'measure_unit', 'quantity_unit')
        }),
        ('Instrucciones', {
            'fields': ('storage_instructions', 'transport_instructions')
        }),
        ('Estado', {
            'fields': ('is_confirmed', 'is_deleted')
        }),
        ('Fechas', {
            'fields': ('created_at', 'updated_at', 'confirmed_at', 'deleted_at'),
            'classes': ('collapse',)
        }),
        ('Auditoría', {
            'fields': ('created_by', 'confirmed_by', 'updated_by', 'deleted_by'),
            'classes': ('collapse',)
        }),
    )


@admin.register(ItemConfiguration)
class ItemConfigurationAdmin(admin.ModelAdmin):
    list_display = ['configuration', 'package', 'is_confirmed', 'created_at']
    list_filter = ['package', 'is_confirmed', 'is_deleted', 'created_at']
    search_fields = ['configuration', 'description', 'code']
    ordering = ['configuration']
    readonly_fields = ['created_at', 'updated_at', 'confirmed_at', 'deleted_at']
    fieldsets = (
        ('Información Básica', {
            'fields': ('code', 'configuration', 'description', 'package')
        }),
        ('Estado', {
            'fields': ('is_confirmed', 'is_deleted')
        }),
        ('Fechas', {
            'fields': ('created_at', 'updated_at', 'confirmed_at', 'deleted_at'),
            'classes': ('collapse',)
        }),
        ('Auditoría', {
            'fields': ('created_by', 'confirmed_by', 'updated_by', 'deleted_by', 'log', 'version'),
            'classes': ('collapse',)
        }),
    )


@admin.register(ItemConfigurationDetail)
class ItemConfigurationDetailAdmin(admin.ModelAdmin):
    list_display = ['detail', 'type', 'configuration', 'is_confirmed']
    list_filter = ['type', 'configuration', 'is_confirmed', 'is_deleted', 'created_at']
    search_fields = ['detail', 'code', 'id_item']
    ordering = ['configuration', 'detail']
    readonly_fields = ['created_at', 'updated_at', 'confirmed_at', 'deleted_at']
    fieldsets = (
        ('Información Básica', {
            'fields': ('code', 'detail', 'type', 'configuration', 'id_item')
        }),
        ('Estado', {
            'fields': ('is_confirmed', 'is_deleted')
        }),
        ('Fechas', {
            'fields': ('created_at', 'updated_at', 'confirmed_at', 'deleted_at'),
            'classes': ('collapse',)
        }),
        ('Auditoría', {
            'fields': ('created_by', 'confirmed_by', 'updated_by', 'deleted_by'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Provider)
class ProviderAdmin(admin.ModelAdmin):
    list_display = ['provider', 'type', 'rating', 'company_name', 'is_active', 'is_confirmed']
    list_filter = ['type', 'rating', 'is_active', 'is_confirmed', 'is_deleted', 'created_at']
    search_fields = ['provider', 'company_name', 'contact_name', 'code']
    ordering = ['provider']
    readonly_fields = ['created_at', 'updated_at', 'confirmed_at', 'deleted_at']
    fieldsets = (
        ('Información Básica', {
            'fields': ('code', 'provider', 'type', 'rating', 'obs_provider')
        }),
        ('Información de Contacto', {
            'fields': ('contact_name', 'contact_mail', 'contact_phone', 'contact_phone2', 'website_url', 'obs_contact'),
            'classes': ('collapse',)
        }),
        ('Información de Empresa', {
            'fields': ('company_name', 'company_rut', 'company_activity', 'legal_representative'),
            'classes': ('collapse',)
        }),
        ('Información de Facturación', {
            'fields': ('billing_address', 'billing_mail', 'billing_phone', 'company_bank', 'bank_account_type', 'bank_account_number', 'bank_account_mail'),
            'classes': ('collapse',)
        }),
        ('Información de Despacho', {
            'fields': ('dispatch_address', 'dispatch_maps_location', 'OBS_dispatch', 'dispatch_district', 'dispatch_region'),
            'classes': ('collapse',)
        }),
        ('Estado', {
            'fields': ('is_active', 'is_confirmed', 'is_deleted')
        }),
        ('Fechas', {
            'fields': ('created_at', 'updated_at', 'confirmed_at', 'deleted_at'),
            'classes': ('collapse',)
        }),
        ('Auditoría', {
            'fields': ('created_by', 'confirmed_by', 'updated_by', 'deleted_by', 'log', 'version'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['description', 'sku', 'provider', 'type', 'price', 'is_active', 'is_confirmed']
    list_filter = ['provider', 'type', 'group', 'category', 'is_active', 'is_confirmed', 'is_deleted', 'created_at']
    search_fields = ['description', 'sku', 'code', 'obs']
    ordering = ['description']
    readonly_fields = ['created_at', 'updated_at', 'confirmed_at', 'deleted_at']
    fieldsets = (
        ('Información Básica', {
            'fields': ('code', 'sku', 'description', 'obs')
        }),
        ('Clasificación', {
            'fields': ('provider', 'type', 'group', 'category')
        }),
        ('Precios y Cantidades', {
            'fields': ('package_unit', 'min_package_purchase', 'price')
        }),
        ('Información Adicional', {
            'fields': ('url', 'package')
        }),
        ('Estado', {
            'fields': ('is_active', 'is_confirmed', 'is_deleted')
        }),
        ('Fechas', {
            'fields': ('created_at', 'updated_at', 'confirmed_at', 'deleted_at'),
            'classes': ('collapse',)
        }),
        ('Auditoría', {
            'fields': ('created_by', 'confirmed_by', 'updated_by', 'deleted_by', 'log', 'version'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    list_display = ['description', 'sku', 'provider', 'type', 'price', 'is_active', 'is_confirmed']
    list_filter = ['provider', 'type', 'group', 'category', 'is_active', 'is_confirmed', 'is_deleted', 'created_at']
    search_fields = ['description', 'sku', 'code', 'obs']
    ordering = ['description']
    readonly_fields = ['created_at', 'updated_at', 'confirmed_at', 'deleted_at']
    fieldsets = (
        ('Información Básica', {
            'fields': ('code', 'sku', 'description', 'obs')
        }),
        ('Clasificación', {
            'fields': ('provider', 'type', 'group', 'category')
        }),
        ('Precios y Cantidades', {
            'fields': ('package_unit', 'min_package_purchase', 'price')
        }),
        ('Información Adicional', {
            'fields': ('url', 'package')
        }),
        ('Estado', {
            'fields': ('is_active', 'is_confirmed', 'is_deleted')
        }),
        ('Fechas', {
            'fields': ('created_at', 'updated_at', 'confirmed_at', 'deleted_at'),
            'classes': ('collapse',)
        }),
        ('Auditoría', {
            'fields': ('created_by', 'confirmed_by', 'updated_by', 'deleted_by', 'log', 'version'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ['description', 'sku', 'provider', 'type', 'price', 'is_active', 'is_confirmed']
    list_filter = ['provider', 'type', 'group', 'category', 'is_active', 'is_confirmed', 'is_deleted', 'created_at']
    search_fields = ['description', 'sku', 'code', 'obs']
    ordering = ['description']
    readonly_fields = ['created_at', 'updated_at', 'confirmed_at', 'deleted_at']
    fieldsets = (
        ('Información Básica', {
            'fields': ('code', 'sku', 'description', 'obs')
        }),
        ('Clasificación', {
            'fields': ('provider', 'type', 'group', 'category')
        }),
        ('Precios y Cantidades', {
            'fields': ('package_unit', 'min_package_purchase', 'price')
        }),
        ('Información Adicional', {
            'fields': ('url',)
        }),
        ('Estado', {
            'fields': ('is_active', 'is_confirmed', 'is_deleted')
        }),
        ('Fechas', {
            'fields': ('created_at', 'updated_at', 'confirmed_at', 'deleted_at'),
            'classes': ('collapse',)
        }),
        ('Auditoría', {
            'fields': ('created_by', 'confirmed_by', 'updated_by', 'deleted_by', 'log', 'version'),
            'classes': ('collapse',)
        }),
    )


@admin.register(PermissionType)
class PermissionTypeAdmin(admin.ModelAdmin):
    list_display = ['type', 'description']
    search_fields = ['type', 'description']
    ordering = ['type']


@admin.register(Permission)
class PermissionAdmin(admin.ModelAdmin):
    list_display = ['permission', 'type', 'is_confirmed', 'created_at']
    list_filter = ['type', 'is_confirmed', 'is_deleted', 'created_at']
    search_fields = ['permission', 'description']
    ordering = ['permission']
    readonly_fields = ['created_at', 'updated_at', 'confirmed_at', 'deleted_at']
    fieldsets = (
        ('Información Básica', {
            'fields': ('permission', 'description', 'type')
        }),
        ('Estado', {
            'fields': ('is_confirmed', 'is_deleted')
        }),
        ('Fechas', {
            'fields': ('created_at', 'updated_at', 'confirmed_at', 'deleted_at'),
            'classes': ('collapse',)
        }),
        ('Auditoría', {
            'fields': ('created_by', 'updated_by', 'confirmed_by', 'deleted_by', 'log', 'version'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ['role', 'is_confirmed', 'created_at']
    list_filter = ['is_confirmed', 'is_deleted', 'created_at']
    search_fields = ['role', 'description']
    ordering = ['role']
    readonly_fields = ['created_at', 'updated_at', 'confirmed_at', 'deleted_at']
    fieldsets = (
        ('Información Básica', {
            'fields': ('role', 'description')
        }),
        ('Estado', {
            'fields': ('is_confirmed', 'is_deleted')
        }),
        ('Fechas', {
            'fields': ('created_at', 'updated_at', 'confirmed_at', 'deleted_at'),
            'classes': ('collapse',)
        }),
        ('Auditoría', {
            'fields': ('created_by', 'confirmed_by', 'updated_by', 'deleted_by', 'log', 'version'),
            'classes': ('collapse',)
        }),
    )


@admin.register(RestrictionRoles)
class RestrictionRolesAdmin(admin.ModelAdmin):
    list_display = ['restriction', 'role', 'is_confirmed', 'created_at']
    list_filter = ['restriction', 'role', 'is_confirmed', 'is_deleted', 'created_at']
    search_fields = ['restriction__restriction', 'role__role']
    ordering = ['restriction', 'role']
    readonly_fields = ['created_at', 'updated_at', 'confirmed_at', 'deleted_at']
    fieldsets = (
        ('Información Básica', {
            'fields': ('restriction', 'role')
        }),
        ('Estado', {
            'fields': ('is_confirmed', 'is_deleted')
        }),
        ('Fechas', {
            'fields': ('created_at', 'updated_at', 'confirmed_at', 'deleted_at'),
            'classes': ('collapse',)
        }),
        ('Auditoría', {
            'fields': ('created_by', 'confirmed_by', 'updated_by', 'deleted_by'),
            'classes': ('collapse',)
        }),
    )


@admin.register(RolePermissions)
class RolePermissionsAdmin(admin.ModelAdmin):
    list_display = ['role', 'permission', 'is_confirmed', 'created_at']
    list_filter = ['role', 'permission', 'is_confirmed', 'is_deleted', 'created_at']
    search_fields = ['role__role', 'permission__permission']
    ordering = ['role', 'permission']
    readonly_fields = ['created_at', 'updated_at', 'confirmed_at', 'deleted_at']
    fieldsets = (
        ('Información Básica', {
            'fields': ('role', 'permission')
        }),
        ('Estado', {
            'fields': ('is_confirmed', 'is_deleted')
        }),
        ('Fechas', {
            'fields': ('created_at', 'updated_at', 'confirmed_at', 'deleted_at'),
            'classes': ('collapse',)
        }),
        ('Auditoría', {
            'fields': ('created_by', 'confirmed_by', 'updated_by', 'deleted_by'),
            'classes': ('collapse',)
        }),
    )


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


@admin.register(ProviderType)
class ProviderTypeAdmin(admin.ModelAdmin):
    list_display = ['type', 'description']
    search_fields = ['type', 'description']
    ordering = ['type']


@admin.register(Price)
class PriceAdmin(admin.ModelAdmin):
    list_display = ('code', 'net_amount', 'gross_amount', 'iva_amount', 'is_active', 'created_at')
    list_filter = ('is_active', 'is_deleted', 'is_confirmed', 'created_at')
    search_fields = ('code',)
    readonly_fields = ('id', 'created_at', 'updated_at', 'confirmed_at', 'deleted_at')
    ordering = ('-created_at',)


@admin.register(FiscalDirectiveType)
class FiscalDirectiveTypeAdmin(admin.ModelAdmin):
    list_display = ('type', 'description')
    search_fields = ('type', 'description')
    ordering = ('type',)


@admin.register(FiscalDirective)
class FiscalDirectiveAdmin(admin.ModelAdmin):
    list_display = ('code', 'fiscal_directive', 'type', 'percentage', 'is_deleted', 'is_confirmed')
    list_filter = ('type', 'is_deleted', 'is_confirmed', 'created_at')
    search_fields = ('code', 'fiscal_directive', 'type__type')
    readonly_fields = ('id', 'created_at', 'updated_at', 'confirmed_at', 'deleted_at')
    ordering = ('fiscal_directive',)


@admin.register(FiscalFormula)
class FiscalFormulaAdmin(admin.ModelAdmin):
    list_display = ('id', 'formula', 'is_deleted', 'is_confirmed', 'created_at')
    list_filter = ('is_deleted', 'is_confirmed', 'created_at')
    search_fields = ('formula', 'formula_template')
    readonly_fields = ('id', 'created_at', 'updated_at', 'confirmed_at', 'deleted_at')
    ordering = ('formula',)


@admin.register(PriceFiscalConfiguration)
class PriceFiscalConfigurationAdmin(admin.ModelAdmin):
    list_display = ('id', 'fiscal_configuration', 'fiscal_formula', 'is_deleted', 'is_confirmed')
    list_filter = ('fiscal_formula', 'is_deleted', 'is_confirmed', 'created_at')
    search_fields = ('fiscal_configuration', 'fiscal_formula__formula')
    readonly_fields = ('id', 'created_at', 'updated_at', 'confirmed_at', 'deleted_at')
    ordering = ('fiscal_configuration',)


@admin.register(FiscalConfigurationDetail)
class FiscalConfigurationDetailAdmin(admin.ModelAdmin):
    list_display = ('id', 'price_fiscal_configuration', 'price', 'fiscal_directive')
    list_filter = ('price_fiscal_configuration', 'fiscal_directive')
    search_fields = ('price', 'fiscal_directive')
    ordering = ('id',)
