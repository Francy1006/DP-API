from rest_framework import serializers
from .models import (
    ItemGroup, Menu, ItemCategory, ItemType, InstructionType, Instruction, 
    Cataloge, Restriction, BankAccountType, Region, District, Bank, UserType, 
    User, UserToken, Package, ItemConfiguration, ItemConfigurationDetail, 
    Provider, Product, Material, Service, PermissionType, Permission, Role, 
    RestrictionRoles, RolePermissions, PackageType, TransportType, MeasureUnit, 
    ProviderType
)


# Menu Serializers
class MenuSerializer(serializers.ModelSerializer):
    """
    Serializer para el modelo Menu
    """
    class Meta:
        model = Menu
        fields = ['id', 'menu', 'description']
        read_only_fields = ['id']


class MenuListSerializer(serializers.ModelSerializer):
    """
    Serializer simplificado para listar menús
    """
    class Meta:
        model = Menu
        fields = ['id', 'menu']


# ItemCategory Serializers
class ItemCategorySerializer(serializers.ModelSerializer):
    """
    Serializer para el modelo ItemCategory
    """
    class Meta:
        model = ItemCategory
        fields = ['id', 'category', 'description', 'cataloge_render']
        read_only_fields = ['id']


class ItemCategoryListSerializer(serializers.ModelSerializer):
    """
    Serializer simplificado para listar categorías de items
    """
    class Meta:
        model = ItemCategory
        fields = ['id', 'category', 'cataloge_render']


# ItemType Serializers
class ItemTypeSerializer(serializers.ModelSerializer):
    """
    Serializer para el modelo ItemType
    """
    class Meta:
        model = ItemType
        fields = ['id', 'type', 'description']
        read_only_fields = ['id']


class ItemTypeListSerializer(serializers.ModelSerializer):
    """
    Serializer simplificado para listar tipos de items
    """
    class Meta:
        model = ItemType
        fields = ['id', 'type']


# ItemGroup Serializers (existing)
class ItemGroupSerializer(serializers.ModelSerializer):
    """
    Serializer para el modelo ItemGroup
    """
    class Meta:
        model = ItemGroup
        fields = ['id', 'group_name', 'description', 'cataloge_render']
        read_only_fields = ['id']


class ItemGroupListSerializer(serializers.ModelSerializer):
    """
    Serializer simplificado para listar grupos de items
    """
    class Meta:
        model = ItemGroup
        fields = ['id', 'group_name', 'cataloge_render']


# InstructionType Serializers
class InstructionTypeSerializer(serializers.ModelSerializer):
    """
    Serializer para el modelo InstructionType
    """
    class Meta:
        model = InstructionType
        fields = [
            'id', 'type', 'description', 'is_deleted', 'is_confirmed',
            'created_at', 'updated_at', 'confirmed_at', 'deleted_at',
            'created_by', 'confirmed_by', 'updated_by', 'deleted_by'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'confirmed_at', 'deleted_at']


class InstructionTypeListSerializer(serializers.ModelSerializer):
    """
    Serializer simplificado para listar tipos de instrucciones
    """
    class Meta:
        model = InstructionType
        fields = ['id', 'type', 'is_confirmed']


# Instruction Serializers
class InstructionSerializer(serializers.ModelSerializer):
    """
    Serializer para el modelo Instruction
    """
    type_name = serializers.CharField(source='type.type', read_only=True)
    
    class Meta:
        model = Instruction
        fields = [
            'id', 'instruction', 'description', 'url_documentation', 
            'type', 'type_name', 'is_deleted', 'is_confirmed',
            'created_at', 'updated_at', 'confirmed_at', 'deleted_at',
            'created_by', 'confirmed_by', 'updated_by', 'deleted_by'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'confirmed_at', 'deleted_at']


class InstructionListSerializer(serializers.ModelSerializer):
    """
    Serializer simplificado para listar instrucciones
    """
    type_name = serializers.CharField(source='type.type', read_only=True)
    
    class Meta:
        model = Instruction
        fields = ['id', 'instruction', 'type_name', 'is_confirmed', 'created_at']


class InstructionCreateSerializer(serializers.ModelSerializer):
    """
    Serializer para crear instrucciones (sin campos de auditoría)
    """
    class Meta:
        model = Instruction
        fields = [
            'instruction', 'description', 'url_documentation', 
            'type', 'created_by'
        ]


class InstructionUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer para actualizar instrucciones
    """
    class Meta:
        model = Instruction
        fields = [
            'instruction', 'description', 'url_documentation', 
            'type', 'updated_by'
        ]


# Cataloge Serializers
class CatalogeSerializer(serializers.ModelSerializer):
    """
    Serializer para el modelo Cataloge
    """
    menu_name = serializers.CharField(source='menu.menu', read_only=True)
    group_name = serializers.CharField(source='group.group_name', read_only=True)
    category_name = serializers.CharField(source='category.category', read_only=True)
    type_name = serializers.CharField(source='type.type', read_only=True)
    
    class Meta:
        model = Cataloge
        fields = [
            'id', 'sku', 'menu', 'menu_name', 'group', 'group_name', 
            'category', 'category_name', 'type', 'type_name', 'restriction',
            'name', 'description', 'OBS', 'chef_recommendation', 
            'usage_instructions', 'base_gross_price', 'min_quantity_purchase',
            'rations_quantity', 'cover_image', 'secondary_image', 
            'complementary_image', 'image_gallery', 'configuration',
            'is_visible', 'is_deleted', 'is_confirmed', 'created_at', 
            'updated_at', 'confirmed_at', 'deleted_at', 'created_by',
            'confirmed_by', 'updated_by', 'deleted_by', 'LOG', 'version'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'confirmed_at', 'deleted_at']


class CatalogeListSerializer(serializers.ModelSerializer):
    """
    Serializer simplificado para listar catálogos
    """
    menu_name = serializers.CharField(source='menu.menu', read_only=True)
    group_name = serializers.CharField(source='group.group_name', read_only=True)
    category_name = serializers.CharField(source='category.category', read_only=True)
    type_name = serializers.CharField(source='type.type', read_only=True)
    
    class Meta:
        model = Cataloge
        fields = [
            'id', 'sku', 'name', 'menu_name', 'group_name', 'category_name', 
            'type_name', 'is_visible', 'is_confirmed', 'created_at',
            'cover_image', 'secondary_image', 'complementary_image', 'image_gallery'
        ]


class CatalogeCreateSerializer(serializers.ModelSerializer):
    """
    Serializer para crear catálogos (sin campos de auditoría)
    """
    class Meta:
        model = Cataloge
        fields = [
            'sku', 'menu', 'group', 'category', 'type', 'restriction',
            'name', 'description', 'OBS', 'chef_recommendation', 
            'usage_instructions', 'base_gross_price', 'min_quantity_purchase',
            'rations_quantity', 'cover_image', 'secondary_image', 
            'complementary_image', 'image_gallery', 'configuration',
            'is_visible', 'created_by', 'LOG'
        ]


class CatalogeUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer para actualizar catálogos
    """
    class Meta:
        model = Cataloge
        fields = [
            'sku', 'menu', 'group', 'category', 'type', 'restriction',
            'name', 'description', 'OBS', 'chef_recommendation', 
            'usage_instructions', 'base_gross_price', 'min_quantity_purchase',
            'rations_quantity', 'cover_image', 'secondary_image', 
            'complementary_image', 'image_gallery', 'configuration',
            'is_visible', 'updated_by', 'LOG'
        ]


# Restriction Serializers
class RestrictionSerializer(serializers.ModelSerializer):
    """
    Serializer para el modelo Restriction
    """
    class Meta:
        model = Restriction
        fields = [
            'id', 'restriction', 'description', 'is_deleted', 'is_confirmed',
            'created_at', 'updated_at', 'confirmed_at', 'deleted_at',
            'created_by', 'confirmed_by', 'updated_by', 'deleted_by',
            'LOG', 'version'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'confirmed_at', 'deleted_at']


class RestrictionListSerializer(serializers.ModelSerializer):
    """
    Serializer simplificado para listar restricciones
    """
    class Meta:
        model = Restriction
        fields = ['id', 'restriction', 'is_confirmed', 'created_at']


class RestrictionCreateSerializer(serializers.ModelSerializer):
    """
    Serializer para crear restricciones (sin campos de auditoría)
    """
    class Meta:
        model = Restriction
        fields = [
            'restriction', 'description', 'created_by', 'LOG'
        ]


class RestrictionUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer para actualizar restricciones
    """
    class Meta:
        model = Restriction
        fields = [
            'restriction', 'description', 'updated_by', 'LOG'
        ]


# BankAccountType Serializers
class BankAccountTypeSerializer(serializers.ModelSerializer):
    """
    Serializer para el modelo BankAccountType
    """
    class Meta:
        model = BankAccountType
        fields = ['id', 'type', 'description']
        read_only_fields = ['id']


class BankAccountTypeListSerializer(serializers.ModelSerializer):
    """
    Serializer simplificado para listar tipos de cuenta bancaria
    """
    class Meta:
        model = BankAccountType
        fields = ['id', 'type']


# Region Serializers
class RegionSerializer(serializers.ModelSerializer):
    """
    Serializer para el modelo Region
    """
    class Meta:
        model = Region
        fields = ['id', 'region', 'description']
        read_only_fields = ['id']


class RegionListSerializer(serializers.ModelSerializer):
    """
    Serializer simplificado para listar regiones
    """
    class Meta:
        model = Region
        fields = ['id', 'region']


# District Serializers
class DistrictSerializer(serializers.ModelSerializer):
    """
    Serializer para el modelo District
    """
    region_name = serializers.CharField(source='region.region', read_only=True)
    
    class Meta:
        model = District
        fields = ['id', 'district', 'region', 'region_name', 'description']
        read_only_fields = ['id']


class DistrictListSerializer(serializers.ModelSerializer):
    """
    Serializer simplificado para listar distritos
    """
    region_name = serializers.CharField(source='region.region', read_only=True)
    
    class Meta:
        model = District
        fields = ['id', 'district', 'region_name']


# Bank Serializers
class BankSerializer(serializers.ModelSerializer):
    """
    Serializer para el modelo Bank
    """
    class Meta:
        model = Bank
        fields = ['id', 'bank', 'description', 'created_at']
        read_only_fields = ['id', 'created_at']


class BankListSerializer(serializers.ModelSerializer):
    """
    Serializer simplificado para listar bancos
    """
    class Meta:
        model = Bank
        fields = ['id', 'bank']


# UserType Serializers
class UserTypeSerializer(serializers.ModelSerializer):
    """
    Serializer para el modelo UserType
    """
    class Meta:
        model = UserType
        fields = ['id', 'type', 'description', 'created_at']
        read_only_fields = ['id', 'created_at']


class UserTypeListSerializer(serializers.ModelSerializer):
    """
    Serializer simplificado para listar tipos de usuario
    """
    class Meta:
        model = UserType
        fields = ['id', 'type']


# User Serializers
class UserSerializer(serializers.ModelSerializer):
    """
    Serializer para el modelo User
    """
    type_name = serializers.CharField(source='type.type', read_only=True)
    
    class Meta:
        model = User
        fields = [
            'id', 'code', 'type', 'type_name', 'google_id', 'mail', 'phone',
            'name', 'last_name', 'is_active', 'is_deleted', 'is_confirmed',
            'created_at', 'updated_at', 'confirmed_at', 'deleted_at',
            'deleted_by', 'LOG', 'version'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'confirmed_at', 'deleted_at']


class UserListSerializer(serializers.ModelSerializer):
    """
    Serializer simplificado para listar usuarios
    """
    type_name = serializers.CharField(source='type.type', read_only=True)
    
    class Meta:
        model = User
        fields = ['id', 'code', 'name', 'last_name', 'mail', 'type_name', 'is_active']


# UserToken Serializers
class UserTokenSerializer(serializers.ModelSerializer):
    """
    Serializer para el modelo UserToken
    """
    user_name = serializers.CharField(source='user_id.name', read_only=True)
    
    class Meta:
        model = UserToken
        fields = [
            'id', 'user_id', 'user_name', 'token', 'ip_address', 'user_agent',
            'created_at', 'expires_at', 'revoked_at'
        ]
        read_only_fields = ['id', 'created_at']


class UserTokenListSerializer(serializers.ModelSerializer):
    """
    Serializer simplificado para listar tokens de usuario
    """
    user_name = serializers.CharField(source='user_id.name', read_only=True)
    
    class Meta:
        model = UserToken
        fields = ['id', 'user_name', 'ip_address', 'created_at', 'expires_at', 'revoked_at']


# Package Serializers
class PackageSerializer(serializers.ModelSerializer):
    """
    Serializer para el modelo Package
    """
    package_type_name = serializers.CharField(source='package_type.type', read_only=True)
    transport_type_name = serializers.CharField(source='transport_type.type', read_only=True)
    measure_unit_name = serializers.CharField(source='measure_unit.measure_unit', read_only=True)
    
    class Meta:
        model = Package
        fields = [
            'id', 'description', 'package_type', 'package_type_name',
            'transport_type', 'transport_type_name', 'size', 'weight',
            'measure_unit', 'measure_unit_name', 'quantity_unit',
            'storage_instructions', 'transport_instructions', 'is_deleted',
            'is_confirmed', 'created_at', 'updated_at', 'confirmed_at',
            'deleted_at', 'created_by', 'confirmed_by', 'updated_by', 'deleted_by'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'confirmed_at', 'deleted_at']


class PackageListSerializer(serializers.ModelSerializer):
    """
    Serializer simplificado para listar paquetes
    """
    package_type_name = serializers.CharField(source='package_type.type', read_only=True)
    transport_type_name = serializers.CharField(source='transport_type.type', read_only=True)
    
    class Meta:
        model = Package
        fields = [
            'id', 'description', 'package_type_name', 'transport_type_name',
            'size', 'weight', 'is_confirmed'
        ]


# ItemConfiguration Serializers
class ItemConfigurationSerializer(serializers.ModelSerializer):
    """
    Serializer para el modelo ItemConfiguration
    """
    package_description = serializers.CharField(source='package.description', read_only=True)
    
    class Meta:
        model = ItemConfiguration
        fields = [
            'id', 'code', 'configuration', 'description', 'package',
            'package_description', 'is_deleted', 'is_confirmed', 'created_at',
            'updated_at', 'confirmed_at', 'deleted_at', 'created_by',
            'confirmed_by', 'updated_by', 'deleted_by', 'LOG', 'version'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'confirmed_at', 'deleted_at']


class ItemConfigurationListSerializer(serializers.ModelSerializer):
    """
    Serializer simplificado para listar configuraciones de items
    """
    package_description = serializers.CharField(source='package.description', read_only=True)
    
    class Meta:
        model = ItemConfiguration
        fields = ['id', 'configuration', 'package_description', 'is_confirmed']


# ItemConfigurationDetail Serializers
class ItemConfigurationDetailSerializer(serializers.ModelSerializer):
    """
    Serializer para el modelo ItemConfigurationDetail
    """
    type_name = serializers.CharField(source='type.type', read_only=True)
    configuration_name = serializers.CharField(source='configuration.configuration', read_only=True)
    
    class Meta:
        model = ItemConfigurationDetail
        fields = [
            'id', 'code', 'detail', 'type', 'type_name', 'configuration',
            'configuration_name', 'id_item', 'is_deleted', 'is_confirmed',
            'created_at', 'updated_at', 'confirmed_at', 'deleted_at',
            'created_by', 'confirmed_by', 'updated_by', 'deleted_by'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'confirmed_at', 'deleted_at']


class ItemConfigurationDetailListSerializer(serializers.ModelSerializer):
    """
    Serializer simplificado para listar detalles de configuración
    """
    type_name = serializers.CharField(source='type.type', read_only=True)
    configuration_name = serializers.CharField(source='configuration.configuration', read_only=True)
    
    class Meta:
        model = ItemConfigurationDetail
        fields = ['id', 'detail', 'type_name', 'configuration_name', 'is_confirmed']


# Provider Serializers
class ProviderSerializer(serializers.ModelSerializer):
    """
    Serializer para el modelo Provider
    """
    type_name = serializers.CharField(source='type.type', read_only=True)
    company_bank_name = serializers.CharField(source='company_bank.bank', read_only=True)
    bank_account_type_name = serializers.CharField(source='bank_account_type.type', read_only=True)
    dispatch_district_name = serializers.CharField(source='dispatch_district.district', read_only=True)
    dispatch_region_name = serializers.CharField(source='dispatch_region.region', read_only=True)
    
    class Meta:
        model = Provider
        fields = [
            'id', 'code', 'provider', 'type', 'type_name', 'rating', 'OBS_provider',
            'contact_name', 'contact_mail', 'contact_phone', 'contact_phone2',
            'website_url', 'OBS_contact', 'company_name', 'company_rut',
            'company_activity', 'legal_representative', 'billing_address',
            'billing_mail', 'billing_phone', 'company_bank', 'company_bank_name',
            'bank_account_type', 'bank_account_type_name', 'bank_account_number',
            'bank_account_mail', 'dispatch_address', 'dispatch_maps_location',
            'OBS_dispatch', 'dispatch_district', 'dispatch_district_name',
            'dispatch_region', 'dispatch_region_name', 'is_active', 'is_deleted',
            'is_confirmed', 'created_at', 'updated_at', 'confirmed_at',
            'deleted_at', 'created_by', 'confirmed_by', 'updated_by', 'deleted_by',
            'LOG', 'version'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'confirmed_at', 'deleted_at']


class ProviderListSerializer(serializers.ModelSerializer):
    """
    Serializer simplificado para listar proveedores
    """
    type_name = serializers.CharField(source='type.type', read_only=True)
    
    class Meta:
        model = Provider
        fields = [
            'id', 'code', 'provider', 'type_name', 'rating', 'company_name',
            'contact_name', 'contact_mail', 'is_active', 'is_confirmed'
        ]


# Product Serializers
class ProductSerializer(serializers.ModelSerializer):
    """
    Serializer para el modelo Product
    """
    provider_name = serializers.CharField(source='provider.provider', read_only=True)
    type_name = serializers.CharField(source='type.type', read_only=True)
    group_name = serializers.CharField(source='group.group_name', read_only=True)
    category_name = serializers.CharField(source='category.category', read_only=True)
    package_description = serializers.CharField(source='package.description', read_only=True)
    
    class Meta:
        model = Product
        fields = [
            'id', 'code', 'sku', 'description', 'OBS', 'package_unit',
            'min_package_purchase', 'gross_price', 'provider', 'provider_name',
            'type', 'type_name', 'group', 'group_name', 'category', 'category_name',
            'url', 'package', 'package_description', 'is_active', 'is_deleted',
            'is_confirmed', 'created_at', 'updated_at', 'confirmed_at',
            'deleted_at', 'created_by', 'confirmed_by', 'updated_by', 'deleted_by',
            'LOG', 'version'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'confirmed_at', 'deleted_at']


class ProductListSerializer(serializers.ModelSerializer):
    """
    Serializer simplificado para listar productos
    """
    provider_name = serializers.CharField(source='provider.provider', read_only=True)
    type_name = serializers.CharField(source='type.type', read_only=True)
    
    class Meta:
        model = Product
        fields = [
            'id', 'code', 'sku', 'description', 'provider_name', 'type_name',
            'gross_price', 'is_active', 'is_confirmed'
        ]


# Material Serializers
class MaterialSerializer(serializers.ModelSerializer):
    """
    Serializer para el modelo Material
    """
    provider_name = serializers.CharField(source='provider.provider', read_only=True)
    type_name = serializers.CharField(source='type.type', read_only=True)
    group_name = serializers.CharField(source='group.group_name', read_only=True)
    category_name = serializers.CharField(source='category.category', read_only=True)
    package_description = serializers.CharField(source='package.description', read_only=True)
    
    class Meta:
        model = Material
        fields = [
            'id', 'code', 'sku', 'description', 'OBS', 'package_unit',
            'min_package_purchase', 'gross_price', 'provider', 'provider_name',
            'type', 'type_name', 'group', 'group_name', 'category', 'category_name',
            'url', 'package', 'package_description', 'is_active', 'is_deleted',
            'is_confirmed', 'created_at', 'updated_at', 'confirmed_at',
            'deleted_at', 'created_by', 'confirmed_by', 'updated_by', 'deleted_by',
            'LOG', 'version'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'confirmed_at', 'deleted_at']


class MaterialListSerializer(serializers.ModelSerializer):
    """
    Serializer simplificado para listar materiales
    """
    provider_name = serializers.CharField(source='provider.provider', read_only=True)
    type_name = serializers.CharField(source='type.type', read_only=True)
    
    class Meta:
        model = Material
        fields = [
            'id', 'code', 'sku', 'description', 'provider_name', 'type_name',
            'gross_price', 'is_active', 'is_confirmed'
        ]


# Service Serializers
class ServiceSerializer(serializers.ModelSerializer):
    """
    Serializer para el modelo Service
    """
    provider_name = serializers.CharField(source='provider.provider', read_only=True)
    type_name = serializers.CharField(source='type.type', read_only=True)
    group_name = serializers.CharField(source='group.group_name', read_only=True)
    category_name = serializers.CharField(source='category.category', read_only=True)
    
    class Meta:
        model = Service
        fields = [
            'id', 'code', 'sku', 'description', 'OBS', 'package_unit',
            'min_package_purchase', 'gross_price', 'provider', 'provider_name',
            'type', 'type_name', 'group', 'group_name', 'category', 'category_name',
            'url', 'is_active', 'is_deleted', 'is_confirmed', 'created_at',
            'updated_at', 'confirmed_at', 'deleted_at', 'created_by',
            'confirmed_by', 'updated_by', 'deleted_by', 'LOG', 'version'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'confirmed_at', 'deleted_at']


class ServiceListSerializer(serializers.ModelSerializer):
    """
    Serializer simplificado para listar servicios
    """
    provider_name = serializers.CharField(source='provider.provider', read_only=True)
    type_name = serializers.CharField(source='type.type', read_only=True)
    
    class Meta:
        model = Service
        fields = [
            'id', 'code', 'sku', 'description', 'provider_name', 'type_name',
            'gross_price', 'is_active', 'is_confirmed'
        ]


# PermissionType Serializers
class PermissionTypeSerializer(serializers.ModelSerializer):
    """
    Serializer para el modelo PermissionType
    """
    class Meta:
        model = PermissionType
        fields = ['id', 'name', 'description']
        read_only_fields = ['id']


class PermissionTypeListSerializer(serializers.ModelSerializer):
    """
    Serializer simplificado para listar tipos de permisos
    """
    class Meta:
        model = PermissionType
        fields = ['id', 'name']


# Permission Serializers
class PermissionSerializer(serializers.ModelSerializer):
    """
    Serializer para el modelo Permission
    """
    type_name = serializers.CharField(source='type.name', read_only=True)
    
    class Meta:
        model = Permission
        fields = [
            'id', 'permission', 'description', 'type', 'type_name', 'is_deleted',
            'is_confirmed', 'created_at', 'updated_at', 'confirmed_at',
            'deleted_at', 'created_by', 'updated_by', 'confirmed_by', 'deleted_by',
            'LOG', 'version'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'confirmed_at', 'deleted_at']


class PermissionListSerializer(serializers.ModelSerializer):
    """
    Serializer simplificado para listar permisos
    """
    type_name = serializers.CharField(source='type.name', read_only=True)
    
    class Meta:
        model = Permission
        fields = ['id', 'permission', 'type_name', 'is_confirmed']


# Role Serializers
class RoleSerializer(serializers.ModelSerializer):
    """
    Serializer para el modelo Role
    """
    class Meta:
        model = Role
        fields = [
            'id', 'role', 'description', 'is_deleted', 'is_confirmed',
            'created_at', 'updated_at', 'confirmed_at', 'deleted_at',
            'created_by', 'confirmed_by', 'updated_by', 'deleted_by',
            'LOG', 'version'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'confirmed_at', 'deleted_at']


class RoleListSerializer(serializers.ModelSerializer):
    """
    Serializer simplificado para listar roles
    """
    class Meta:
        model = Role
        fields = ['id', 'role', 'is_confirmed']


# RestrictionRoles Serializers
class RestrictionRolesSerializer(serializers.ModelSerializer):
    """
    Serializer para el modelo RestrictionRoles
    """
    restriction_name = serializers.CharField(source='restriction.restriction', read_only=True)
    role_name = serializers.CharField(source='role.role', read_only=True)
    
    class Meta:
        model = RestrictionRoles
        fields = [
            'id', 'restriction', 'restriction_name', 'role', 'role_name',
            'is_deleted', 'is_confirmed', 'created_at', 'updated_at',
            'confirmed_at', 'deleted_at', 'created_by', 'confirmed_by',
            'updated_by', 'deleted_by'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'confirmed_at', 'deleted_at']


class RestrictionRolesListSerializer(serializers.ModelSerializer):
    """
    Serializer simplificado para listar restricciones-roles
    """
    restriction_name = serializers.CharField(source='restriction.restriction', read_only=True)
    role_name = serializers.CharField(source='role.role', read_only=True)
    
    class Meta:
        model = RestrictionRoles
        fields = ['id', 'restriction_name', 'role_name', 'is_confirmed']


# RolePermissions Serializers
class RolePermissionsSerializer(serializers.ModelSerializer):
    """
    Serializer para el modelo RolePermissions
    """
    role_name = serializers.CharField(source='role.role', read_only=True)
    permission_name = serializers.CharField(source='permission.permission', read_only=True)
    
    class Meta:
        model = RolePermissions
        fields = [
            'id', 'role', 'role_name', 'permission', 'permission_name',
            'is_deleted', 'is_confirmed', 'created_at', 'updated_at',
            'confirmed_at', 'deleted_at', 'created_by', 'confirmed_by',
            'updated_by', 'deleted_by'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'confirmed_at', 'deleted_at']


class RolePermissionsListSerializer(serializers.ModelSerializer):
    """
    Serializer simplificado para listar roles-permisos
    """
    role_name = serializers.CharField(source='role.role', read_only=True)
    permission_name = serializers.CharField(source='permission.permission', read_only=True)
    
    class Meta:
        model = RolePermissions
        fields = ['id', 'role_name', 'permission_name', 'is_confirmed']


# PackageType Serializers
class PackageTypeSerializer(serializers.ModelSerializer):
    """
    Serializer para el modelo PackageType
    """
    class Meta:
        model = PackageType
        fields = ['id', 'type', 'description']
        read_only_fields = ['id']


class PackageTypeListSerializer(serializers.ModelSerializer):
    """
    Serializer simplificado para listar tipos de paquetes
    """
    class Meta:
        model = PackageType
        fields = ['id', 'type']


# TransportType Serializers
class TransportTypeSerializer(serializers.ModelSerializer):
    """
    Serializer para el modelo TransportType
    """
    class Meta:
        model = TransportType
        fields = ['id', 'type', 'description']
        read_only_fields = ['id']


class TransportTypeListSerializer(serializers.ModelSerializer):
    """
    Serializer simplificado para listar tipos de transporte
    """
    class Meta:
        model = TransportType
        fields = ['id', 'type']


# MeasureUnit Serializers
class MeasureUnitSerializer(serializers.ModelSerializer):
    """
    Serializer para el modelo MeasureUnit
    """
    class Meta:
        model = MeasureUnit
        fields = ['id', 'measure_unit', 'description']
        read_only_fields = ['id']


class MeasureUnitListSerializer(serializers.ModelSerializer):
    """
    Serializer simplificado para listar unidades de medida
    """
    class Meta:
        model = MeasureUnit
        fields = ['id', 'measure_unit']


# ProviderType Serializers
class ProviderTypeSerializer(serializers.ModelSerializer):
    """
    Serializer para el modelo ProviderType
    """
    class Meta:
        model = ProviderType
        fields = ['id', 'type', 'description']
        read_only_fields = ['id']


class ProviderTypeListSerializer(serializers.ModelSerializer):
    """
    Serializer simplificado para listar tipos de proveedores
    """
    class Meta:
        model = ProviderType
        fields = ['id', 'type'] 